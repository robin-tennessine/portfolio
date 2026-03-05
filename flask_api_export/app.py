"""
Flask API for Secure Data Export with PDPA Compliance
Provides masked transaction data for Power BI with email export functionality
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime
import logging
from functools import wraps
import ipaddress

# Import local modules
import config
from data_masking import PDPAMasker
from email_service import EmailExportService

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Configure CORS for Power BI
CORS(app, resources={
    r"/api/*": {
        "origins": config.ALLOWED_ORIGINS
    }
})

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize services
masker = PDPAMasker()
email_service = EmailExportService(config)

# Create exports folder if it doesn't exist
os.makedirs(config.EXPORT_FOLDER, exist_ok=True)

# Load sample data (in production, this would query a database)
DATA_FILE = 'sample_transactions.csv'
try:
    df_transactions = pd.read_csv(DATA_FILE)
    logger.info(f"Loaded {len(df_transactions)} transactions from {DATA_FILE}")
except FileNotFoundError:
    logger.warning(f"{DATA_FILE} not found. Creating empty DataFrame.")
    df_transactions = pd.DataFrame()


def check_network_access(f):
    """Decorator to check if request comes from allowed network (VPN/internal)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get client IP
        client_ip = request.remote_addr

        # In development, allow localhost
        if client_ip in ['127.0.0.1', 'localhost', '::1']:
            return f(*args, **kwargs)

        # Check if IP is in allowed networks
        try:
            client_ip_obj = ipaddress.ip_address(client_ip)
            for network_str in config.ALLOWED_NETWORKS:
                network = ipaddress.ip_network(network_str, strict=False)
                if client_ip_obj in network:
                    logger.info(f"Access granted from {client_ip}")
                    return f(*args, **kwargs)

            logger.warning(f"Access denied from {client_ip} - not in allowed networks")
            return jsonify({
                'error': 'Access denied',
                'message': 'This service is only accessible from company network or VPN'
            }), 403

        except Exception as e:
            logger.error(f"Error checking network access: {str(e)}")
            return jsonify({'error': 'Access check failed'}), 500

    return decorated_function


@app.route('/')
def index():
    """API information endpoint"""
    return jsonify({
        'service': 'Data Export API',
        'version': '1.0.0',
        'description': 'PDPA-compliant transaction data API for Power BI',
        'endpoints': {
            '/api/transactions': 'GET - Fetch masked transaction data with filters',
            '/api/export': 'POST - Trigger data export and send via email',
            '/api/health': 'GET - Health check'
        },
        'security': 'VPN/Company network access required',
        'compliance': 'Thailand PDPA - All personal data is masked'
    })


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'data_loaded': len(df_transactions) > 0,
        'record_count': len(df_transactions)
    })


@app.route('/api/transactions', methods=['GET'])
@check_network_access
def get_transactions():
    """
    Get masked transaction data with optional filters
    Query parameters:
        - date_from: Start date (YYYY-MM-DD)
        - date_to: End date (YYYY-MM-DD)
        - business_unit: Filter by business unit
        - store_location: Filter by store
        - product_category: Filter by category
        - limit: Max rows to return (default: 1000)
    """
    try:
        if df_transactions.empty:
            return jsonify({
                'error': 'No data available',
                'data': [],
                'count': 0
            }), 404

        # Start with full dataset
        filtered_df = df_transactions.copy()

        # Apply filters
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        business_unit = request.args.get('business_unit')
        store_location = request.args.get('store_location')
        product_category = request.args.get('product_category')
        limit = int(request.args.get('limit', 1000))

        # Date filtering
        if date_from:
            filtered_df = filtered_df[filtered_df['transaction_date'] >= date_from]
        if date_to:
            filtered_df = filtered_df[filtered_df['transaction_date'] <= date_to]

        # Business unit filtering
        if business_unit and business_unit != 'All':
            filtered_df = filtered_df[filtered_df['business_unit'] == business_unit]

        # Store location filtering
        if store_location and store_location != 'All':
            filtered_df = filtered_df[filtered_df['store_location'] == store_location]

        # Product category filtering
        if product_category and product_category != 'All':
            filtered_df = filtered_df[filtered_df['product_category'] == product_category]

        # Apply limit
        if limit > 0:
            filtered_df = filtered_df.head(min(limit, config.MAX_EXPORT_ROWS))

        # Mask sensitive data
        masked_data = []
        for _, row in filtered_df.iterrows():
            masked_row = masker.mask_transaction_data(row.to_dict())
            masked_data.append(masked_row)

        logger.info(f"Returned {len(masked_data)} masked transactions")

        return jsonify({
            'success': True,
            'count': len(masked_data),
            'filters_applied': {
                'date_from': date_from,
                'date_to': date_to,
                'business_unit': business_unit,
                'store_location': store_location,
                'product_category': product_category
            },
            'data': masked_data,
            'pdpa_notice': 'All personal data has been masked for compliance'
        })

    except Exception as e:
        logger.error(f"Error fetching transactions: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch transactions',
            'message': str(e)
        }), 500


@app.route('/api/export', methods=['POST'])
@check_network_access
def export_data():
    """
    Export filtered data and send via email
    Request body (JSON):
    {
        "recipient_email": "user@example.com",
        "date_from": "2024-01-01",
        "date_to": "2024-12-31",
        "business_unit": "Jaymart Mobile",
        "product_category": "Electronics",
        "format": "csv" or "excel"
    }
    """
    try:
        # Get request data
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        recipient_email = data.get('recipient_email')
        if not recipient_email:
            return jsonify({'error': 'recipient_email is required'}), 400

        # Extract filters
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        business_unit = data.get('business_unit', 'All')
        product_category = data.get('product_category', 'All')
        export_format = data.get('format', 'csv')

        # Filter data (same logic as get_transactions)
        filtered_df = df_transactions.copy()

        if date_from:
            filtered_df = filtered_df[filtered_df['transaction_date'] >= date_from]
        if date_to:
            filtered_df = filtered_df[filtered_df['transaction_date'] <= date_to]
        if business_unit and business_unit != 'All':
            filtered_df = filtered_df[filtered_df['business_unit'] == business_unit]
        if product_category and product_category != 'All':
            filtered_df = filtered_df[filtered_df['product_category'] == product_category]

        # Apply max rows limit
        if len(filtered_df) > config.MAX_EXPORT_ROWS:
            filtered_df = filtered_df.head(config.MAX_EXPORT_ROWS)

        # Mask all sensitive data
        masked_data = []
        for _, row in filtered_df.iterrows():
            masked_row = masker.mask_transaction_data(row.to_dict())
            masked_data.append(masked_row)

        masked_df = pd.DataFrame(masked_data)

        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"export_{timestamp}.{export_format}"
        filepath = os.path.join(config.EXPORT_FOLDER, filename)

        # Save file
        if export_format == 'excel':
            masked_df.to_excel(filepath, index=False, engine='openpyxl')
        else:  # csv
            masked_df.to_csv(filepath, index=False)

        logger.info(f"Created export file: {filepath} ({len(masked_df)} rows)")

        # Prepare export parameters for email
        export_params = {
            'date_from': date_from or 'N/A',
            'date_to': date_to or 'N/A',
            'business_unit': business_unit,
            'product_category': product_category,
            'record_count': len(masked_df)
        }

        # Send email
        success, message = email_service.send_export(
            recipient_email=recipient_email,
            file_path=filepath,
            file_name=filename,
            export_params=export_params
        )

        # Clean up file after sending
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"Cleaned up export file: {filepath}")

        if success:
            return jsonify({
                'success': True,
                'message': message,
                'export_details': {
                    'rows_exported': len(masked_df),
                    'format': export_format,
                    'sent_to': recipient_email,
                    'timestamp': datetime.now().isoformat()
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send export',
                'message': message
            }), 500

    except Exception as e:
        logger.error(f"Error in export: {str(e)}")
        return jsonify({
            'error': 'Export failed',
            'message': str(e)
        }), 500


@app.route('/api/filters', methods=['GET'])
@check_network_access
def get_filter_options():
    """Get available filter options for Power BI slicers"""
    try:
        if df_transactions.empty:
            return jsonify({'error': 'No data available'}), 404

        filters = {
            'business_units': sorted(df_transactions['business_unit'].unique().tolist()),
            'store_locations': sorted(df_transactions['store_location'].unique().tolist()),
            'product_categories': sorted(df_transactions['product_category'].unique().tolist()),
            'date_range': {
                'min': df_transactions['transaction_date'].min(),
                'max': df_transactions['transaction_date'].max()
            },
            'payment_methods': sorted(df_transactions['payment_method'].unique().tolist())
        }

        return jsonify({
            'success': True,
            'filters': filters
        })

    except Exception as e:
        logger.error(f"Error getting filter options: {str(e)}")
        return jsonify({
            'error': 'Failed to get filters',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    logger.info("Starting Flask API Export Service")
    logger.info(f"PDPA masking: {'ENABLED' if config.MASK_SENSITIVE_DATA else 'DISABLED'}")
    logger.info(f"Allowed networks: {config.ALLOWED_NETWORKS}")

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
