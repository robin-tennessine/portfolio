"""
Email Service for Secure Data Export
Sends masked transaction data via email with authentication
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailExportService:
    """Handles secure email sending for data exports"""

    def __init__(self, config):
        """
        Initialize email service with configuration

        Args:
            config: Configuration object with email settings
        """
        self.smtp_server = config.SMTP_SERVER
        self.smtp_port = config.SMTP_PORT
        self.sender_email = config.SENDER_EMAIL
        self.sender_password = config.SENDER_PASSWORD
        self.use_tls = config.USE_TLS

    def send_export(self, recipient_email, file_path, file_name, export_params):
        """
        Send exported data file via email

        Args:
            recipient_email: Recipient's email address
            file_path: Path to the file to send
            file_name: Name of the file attachment
            export_params: Dictionary of export parameters (filters, date range, etc.)

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"Data Export - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

            # Create email body
            body = self._create_email_body(export_params)
            msg.attach(MIMEText(body, 'html'))

            # Attach file
            if os.path.exists(file_path):
                with open(file_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {file_name}'
                    )
                    msg.attach(part)
            else:
                logger.error(f"File not found: {file_path}")
                return False, f"File not found: {file_path}"

            # Send email
            logger.info(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")

            if self.use_tls:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)

            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient_email, text)
            server.quit()

            logger.info(f"Export sent successfully to {recipient_email}")
            return True, f"Export sent successfully to {recipient_email}"

        except smtplib.SMTPAuthenticationError:
            error_msg = "SMTP authentication failed. Check email credentials."
            logger.error(error_msg)
            return False, error_msg

        except smtplib.SMTPException as e:
            error_msg = f"SMTP error occurred: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def _create_email_body(self, export_params):
        """
        Create HTML email body with export details

        Args:
            export_params: Dictionary of export parameters

        Returns:
            str: HTML formatted email body
        """
        # Extract parameters
        date_from = export_params.get('date_from', 'N/A')
        date_to = export_params.get('date_to', 'N/A')
        business_unit = export_params.get('business_unit', 'All')
        product_category = export_params.get('product_category', 'All')
        record_count = export_params.get('record_count', 0)

        html = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .header {{
                        background-color: #2563eb;
                        color: white;
                        padding: 20px;
                        border-radius: 5px 5px 0 0;
                    }}
                    .content {{
                        background-color: #f8f9fa;
                        padding: 20px;
                        border: 1px solid #e5e7eb;
                    }}
                    .info-table {{
                        width: 100%;
                        margin: 15px 0;
                        border-collapse: collapse;
                    }}
                    .info-table td {{
                        padding: 8px;
                        border-bottom: 1px solid #ddd;
                    }}
                    .info-table td:first-child {{
                        font-weight: bold;
                        width: 40%;
                    }}
                    .warning {{
                        background-color: #fff3cd;
                        border-left: 4px solid #ffc107;
                        padding: 15px;
                        margin: 15px 0;
                    }}
                    .footer {{
                        margin-top: 20px;
                        padding-top: 15px;
                        border-top: 1px solid #ddd;
                        font-size: 12px;
                        color: #666;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>Data Export Notification</h2>
                    </div>
                    <div class="content">
                        <p>Your requested data export has been completed and is attached to this email.</p>

                        <table class="info-table">
                            <tr>
                                <td>Export Date:</td>
                                <td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                            </tr>
                            <tr>
                                <td>Date Range:</td>
                                <td>{date_from} to {date_to}</td>
                            </tr>
                            <tr>
                                <td>Business Unit:</td>
                                <td>{business_unit}</td>
                            </tr>
                            <tr>
                                <td>Product Category:</td>
                                <td>{product_category}</td>
                            </tr>
                            <tr>
                                <td>Total Records:</td>
                                <td>{record_count:,}</td>
                            </tr>
                        </table>

                        <div class="warning">
                            <strong>⚠️ PDPA Notice:</strong><br>
                            All personal data in this export has been masked in compliance with Thailand's
                            Personal Data Protection Act (PDPA). This file contains:
                            <ul>
                                <li>Masked names (first character only)</li>
                                <li>Masked ID card numbers</li>
                                <li>Masked email addresses</li>
                                <li>Masked phone numbers</li>
                                <li>Anonymous customer IDs</li>
                            </ul>
                        </div>

                        <p><strong>Security Reminder:</strong></p>
                        <ul>
                            <li>This email is confidential and intended only for the authorized recipient</li>
                            <li>Do not forward this data to unauthorized parties</li>
                            <li>Delete this email and attachment after use</li>
                            <li>Report any security concerns immediately</li>
                        </ul>
                    </div>
                    <div class="footer">
                        <p>
                            This is an automated message from the Data Export System.<br>
                            Generated by Flask API Export Service<br>
                            For support, contact your IT administrator.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """

        return html


# Example usage
if __name__ == "__main__":
    # This is just for testing the email body generation
    class MockConfig:
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        SENDER_EMAIL = "noreply@example.com"
        SENDER_PASSWORD = "hidden"
        USE_TLS = True

    service = EmailExportService(MockConfig())

    # Test parameters
    test_params = {
        'date_from': '2024-01-01',
        'date_to': '2024-12-31',
        'business_unit': 'Jaymart Mobile',
        'product_category': 'Smartphones',
        'record_count': 1523
    }

    # Generate and print email body (for testing)
    body = service._create_email_body(test_params)
    print("Email body generated successfully")
    print(f"Body length: {len(body)} characters")
