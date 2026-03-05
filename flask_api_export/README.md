# Flask API for Secure Data Export with PDPA Compliance

A production-ready Flask API that provides PDPA-compliant transaction data for Power BI dashboards with secure email export functionality. Built for Business Unit support at Jaymart Holding (Jaymart Mobile & Casa Lapin).

## 🎯 Project Overview

This project demonstrates a real-world solution for providing masked transaction data to Power BI while maintaining Thailand's Personal Data Protection Act (PDPA) compliance. The API is deployed on Windows Server and accessible only through company VPN for security.

### Key Features

- **PDPA Compliance**: Automatic masking of sensitive personal data (names, ID cards, emails, phone numbers)
- **Power BI Integration**: RESTful API endpoints designed for Power BI data refresh
- **Secure Email Export**: Users can export filtered data and receive via email with SMTP configuration
- **Network Security**: VPN-only access with IP whitelisting
- **Data Filtering**: Dynamic slicers for business unit, date range, location, and product category
- **Audit Logging**: Comprehensive logging of all data access and exports

## 🔒 Security & Compliance

### PDPA Data Masking

All sensitive personal data is automatically masked before transmission:

| Data Type | Example Original | Masked Output |
|-----------|-----------------|---------------|
| Name | Somchai Phonpakdee | S****** P********* |
| ID Card (13 digits) | 1234567890123 | 1-2***-*****-**-3 |
| Passport | AB1234567 | AB****567 |
| Email | somchai@example.com | s******@e******.com |
| Phone | 0812345678 | 08****5678 |
| Customer ID | CUST001 | ANON_4A8B3C2D |

### Network Security

- **VPN Required**: API only accessible from company network or VPN connection
- **IP Whitelisting**: Configurable allowed network ranges
- **CORS Protection**: Restricted to Power BI and internal domains
- **HTTPS Enforced**: SSL/TLS encryption in production

### Configuration Security

- Sensitive credentials stored in `config.py` (gitignored)
- SMTP passwords and database credentials never committed to Git
- Template file (`config.example.py`) provided for setup

## 📊 Use Case: Power BI Integration

### Workflow

1. **Power BI Dashboard**: Users apply filters (date range, business unit, store, category)
2. **API Request**: Power BI queries `/api/transactions` with filter parameters
3. **Data Masking**: API masks all sensitive data per PDPA requirements
4. **Display**: Power BI displays masked transaction data to users
5. **Export Button**: Users click export button in Power BI
6. **Trigger Page**: Redirects to export confirmation page (VPN-only)
7. **Email Delivery**: Upon confirmation, masked data sent to user's email
8. **File Cleanup**: Temporary export files automatically deleted

### Power BI Setup

```powerquery
let
    Source = Json.Document(Web.Contents(
        "http://your-server:5000/api/transactions",
        [
            Query=[
                date_from="2024-01-01",
                date_to="2024-12-31",
                business_unit="Jaymart Mobile",
                limit="10000"
            ]
        ]
    )),
    Data = Source[data],
    ToTable = Table.FromList(Data, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    ExpandColumn = Table.ExpandRecordColumn(ToTable, "Column1",
        {"transaction_id", "transaction_date", "customer_name",
         "product_name", "total_amount", "business_unit"})
in
    ExpandColumn
```

## 🚀 Setup & Installation

### Prerequisites

- Python 3.8+
- Windows Server (for production) or any OS for development
- VPN access to company network (for production)
- SMTP email account (Gmail, Outlook, or company mail server)

### Installation Steps

```bash
# 1. Clone or download this folder
cd flask_api_export

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure settings
cp config.example.py config.py
# Edit config.py with your credentials

# 6. Generate sample data (for testing)
python generate_sample_data.py

# 7. Run the API
python app.py
```

### Configuration

Edit `config.py` with your settings:

```python
# Email Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@company.com'
SENDER_PASSWORD = 'your-app-password'  # Use app-specific password

# Network Security
ALLOWED_NETWORKS = [
    '192.168.1.0/24',  # Company network
    '10.0.0.0/8',      # VPN range
]

# Database (if connecting to real database)
DB_HOST = 'your-database-server'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
```

**Important**: Never commit `config.py` to Git!

## 📡 API Endpoints

### GET /api/transactions

Fetch masked transaction data with filters.

**Query Parameters:**
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)
- `business_unit` (optional): Filter by business unit
- `store_location` (optional): Filter by store
- `product_category` (optional): Filter by category
- `limit` (optional): Max rows (default: 1000, max: 100000)

**Example Request:**
```bash
curl "http://localhost:5000/api/transactions?date_from=2024-01-01&business_unit=Jaymart Mobile&limit=100"
```

**Response:**
```json
{
  "success": true,
  "count": 100,
  "filters_applied": {
    "date_from": "2024-01-01",
    "business_unit": "Jaymart Mobile"
  },
  "data": [
    {
      "transaction_id": "TXN00000001",
      "transaction_date": "2024-01-15",
      "customer_name": "S****** P*********",
      "email": "s******@g****.com",
      "phone": "08****5678",
      "product_name": "iPhone 15 Pro",
      "total_amount": 35000.00,
      "business_unit": "Jaymart Mobile"
    }
  ],
  "pdpa_notice": "All personal data has been masked for compliance"
}
```

### POST /api/export

Trigger data export and send via email.

**Request Body:**
```json
{
  "recipient_email": "user@company.com",
  "date_from": "2024-01-01",
  "date_to": "2024-12-31",
  "business_unit": "Jaymart Mobile",
  "product_category": "Electronics",
  "format": "excel"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Export sent successfully to user@company.com",
  "export_details": {
    "rows_exported": 1523,
    "format": "excel",
    "sent_to": "user@company.com",
    "timestamp": "2024-12-15T14:30:00"
  }
}
```

### GET /api/filters

Get available filter options for Power BI slicers.

**Response:**
```json
{
  "success": true,
  "filters": {
    "business_units": ["Casa Lapin", "Jaymart Mobile"],
    "store_locations": ["Bangkok - Siam", "Chiang Mai Central"],
    "product_categories": ["Electronics", "F&B"],
    "date_range": {
      "min": "2024-01-01",
      "max": "2024-12-31"
    }
  }
}
```

### GET /api/health

Health check endpoint.

## 🏗️ Architecture

```
Power BI Dashboard
       ↓
    [Filters Applied]
       ↓
   Company VPN
       ↓
Windows Server (Flask API)
       ↓
   [IP Whitelist Check]
       ↓
   [PDPA Masking]
       ↓
   [Return Masked Data]
       ↓
Export Button Clicked?
   Yes → Email Service
       ↓
   [Generate Excel/CSV]
       ↓
   [Send via SMTP]
       ↓
   [Clean up files]
```

## 📁 Project Structure

```
flask_api_export/
├── app.py                      # Main Flask application
├── data_masking.py             # PDPA masking utilities
├── email_service.py            # Email sending service
├── generate_sample_data.py     # Sample data generator
├── config.py                   # Configuration (gitignored)
├── config.example.py           # Configuration template
├── requirements.txt            # Python dependencies
├── sample_transactions.csv     # Sample data (5000 records)
├── exports/                    # Temporary export files
├── api_export.log              # Application logs
└── README.md                   # This file
```

## 🧪 Testing

### Test Data Masking

```bash
python data_masking.py
```

Output shows before/after examples of masked data.

### Test API Locally

```bash
# 1. Start the API
python app.py

# 2. Test health check
curl http://localhost:5000/api/health

# 3. Test transactions endpoint
curl "http://localhost:5000/api/transactions?limit=10"

# 4. Test export (requires valid email config)
curl -X POST http://localhost:5000/api/export \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_email": "your-email@example.com",
    "date_from": "2024-01-01",
    "date_to": "2024-12-31",
    "format": "csv"
  }'
```

## 🎓 Skills Demonstrated

### Technical Skills
- **Python**: Flask web framework, pandas data manipulation
- **API Development**: RESTful API design, JSON responses
- **Data Security**: PDPA compliance, data masking algorithms
- **Email Integration**: SMTP configuration, HTML emails, file attachments
- **Network Security**: IP whitelisting, VPN requirements, CORS
- **Error Handling**: Comprehensive logging and error responses
- **Documentation**: Clear API documentation and code comments

### Business Skills
- **Regulatory Compliance**: Understanding of Thailand's PDPA requirements
- **Stakeholder Support**: Supporting business units with data needs
- **User Experience**: Simple export workflow for non-technical users
- **Data Governance**: Implementing data access controls

## 🔧 Production Deployment

### Windows Server Setup

1. **Install Python**: Download from python.org
2. **Configure IIS** (optional): Set up reverse proxy
3. **Windows Service**: Use NSSM to run as service
   ```bash
   nssm install FlaskAPIExport "C:\path\to\venv\Scripts\python.exe" "C:\path\to\app.py"
   ```
4. **Firewall**: Allow port 5000 (or your chosen port)
5. **VPN Configuration**: Ensure server is behind VPN

### Environment Variables (Alternative to config.py)

```bash
# Set via environment variables instead of config.py
set SMTP_SERVER=smtp.company.com
set SMTP_PORT=587
set SENDER_EMAIL=noreply@company.com
set SENDER_PASSWORD=your-password
```

## 📈 Performance & Scalability

- **Current**: Handles 5000 transactions efficiently
- **Optimizations**:
  - Implements row limits to prevent memory issues
  - Temporary file cleanup after email sending
  - Efficient pandas operations for data filtering
- **Future Enhancements**:
  - Database connection pooling
  - Caching frequently accessed filters
  - Async email sending with queue system

## 🐛 Troubleshooting

**Email not sending:**
- Check SMTP credentials in `config.py`
- For Gmail: Use app-specific password (not regular password)
- Check firewall allows outbound SMTP connection

**VPN access denied:**
- Verify your IP is in `ALLOWED_NETWORKS` in config.py
- Check VPN connection is active
- For testing locally, use localhost

**No data returned:**
- Verify `sample_transactions.csv` exists
- Check date range filters aren't excluding all data
- Review logs in `api_export.log`

## 📝 License

This is a portfolio project demonstrating real-world API development skills. Feel free to use as reference or template for your own projects.

## 👤 Author

**Robin Phonpakdee**
Junior Data Analyst | Cube Analytics Consulting → Jaymart Holding

- Portfolio: https://robin-tennessine.github.io/portfolio/website/
- GitHub: https://github.com/robin-tennessine
- LinkedIn: https://linkedin.com/in/robin-phonpakdee-4a4782251
- Email: robint.phonpakdee@gmail.com

---

**Note**: This project uses synthetic data for demonstration purposes. All data shown is randomly generated and does not represent real customer information.
