"""
Configuration Template for Flask API Export Service

IMPORTANT: Copy this file to config.py and fill in your actual credentials
DO NOT commit config.py to version control - it contains sensitive information
"""

# Flask Configuration
DEBUG = False  # Set to True for development only
SECRET_KEY = 'your-secret-key-here-change-this'  # Change this to a random secret key
HOST = '0.0.0.0'  # Listen on all interfaces (for Windows Server)
PORT = 5000

# Email (SMTP) Configuration
SMTP_SERVER = 'smtp.gmail.com'  # Your SMTP server
SMTP_PORT = 587  # Usually 587 for TLS, 465 for SSL
SENDER_EMAIL = 'your-email@example.com'  # Email address to send from
SENDER_PASSWORD = 'your-app-password'  # Email password or app-specific password
USE_TLS = True  # Use TLS encryption

# Security Configuration
ALLOWED_NETWORKS = [
    '192.168.1.0/24',  # Example: Company internal network
    '10.0.0.0/8',      # Example: VPN network
]

# CORS (Cross-Origin Resource Sharing)
# Only allow requests from Power BI service and internal network
ALLOWED_ORIGINS = [
    'https://app.powerbi.com',
    'http://localhost:*',  # For development
    'http://192.168.*',    # Internal network
]

# Export Configuration
MAX_EXPORT_ROWS = 100000  # Maximum rows per export
EXPORT_FOLDER = './exports'  # Temporary folder for export files
EXPORT_FORMATS = ['csv', 'excel']  # Allowed export formats

# Database Configuration (if connecting to database)
DB_HOST = 'your-database-server'
DB_PORT = 3306  # MySQL/MariaDB default port (5432 for PostgreSQL)
DB_NAME = 'your_database_name'
DB_USER = 'your_database_user'
DB_PASSWORD = 'your_database_password'

# Logging Configuration
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = 'api_export.log'

# PDPA Configuration
MASK_SENSITIVE_DATA = True  # Always mask sensitive data
RETENTION_DAYS = 7  # How long to keep export files before deletion

# Rate Limiting
RATE_LIMIT = '100 per hour'  # Maximum requests per user per hour

# Notes:
# - Change SECRET_KEY to a random string
# - Use app-specific passwords for Gmail (not your actual password)
# - Update ALLOWED_NETWORKS to match your VPN/company network
# - Never commit config.py to Git - it's automatically ignored
