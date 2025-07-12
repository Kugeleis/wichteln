"""
Mailpit mail service implementation.

This module provides a mail service implementation that uses Mailpit for local
development and testing. Mailpit captures emails instead of sending them to
real recipients, and provides a web interface for viewing captured emails.

Website: https://github.com/axllent/mailpit
"""

import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any, Union
from .protocol import MailProtocol, EmailMessage


class MailpitMailService(MailProtocol):
    """
    Mail service implementation for Mailpit (local testing).

    Mailpit is a modern email testing tool that captures emails during development
    and provides a web interface to view them. Perfect for testing email functionality
    without sending real emails.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 1025,
        web_ui_port: int = 8025,
        default_sender: str = "noreply@localhost",
    ):
        """
        Initialize Mailpit mail service.

        Args:
            host: Mailpit SMTP host (default: localhost)
            port: Mailpit SMTP port (default: 1025)
            web_ui_port: Mailpit web interface port (default: 8025)
            default_sender: Default sender email address
        """
        self.host = host
        self.port = port
        self.web_ui_port = web_ui_port
        self.default_sender = default_sender

    def send_email(self, message: EmailMessage) -> bool:
        """
        Send email via Mailpit SMTP server.

        Args:
            message: EmailMessage object

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create MIME message with proper type annotation
            email_msg: Union[MIMEMultipart, MIMEText]

            if message.html_body:
                email_msg = MIMEMultipart("alternative")
                email_msg["From"] = message.sender or self.default_sender
                email_msg["To"] = message.recipient
                email_msg["Subject"] = message.subject

                # Add plain text part
                email_msg.attach(MIMEText(message.body, "plain", "utf-8"))

                # Add HTML part
                email_msg.attach(MIMEText(message.html_body, "html", "utf-8"))
            else:
                email_msg = MIMEText(message.body, "plain", "utf-8")
                email_msg["From"] = message.sender or self.default_sender
                email_msg["To"] = message.recipient
                email_msg["Subject"] = message.subject

            # Connect to Mailpit SMTP server
            with smtplib.SMTP(self.host, self.port) as server:
                # Mailpit doesn't require authentication or TLS
                server.sendmail(
                    message.sender or self.default_sender,
                    [message.recipient],
                    email_msg.as_string(),
                )

            print(
                f"📧 Email captured by Mailpit: {message.recipient} - {message.subject}"
            )
            print(f"   🌐 View at: http://{self.host}:{self.web_ui_port}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email via Mailpit: {e}")
            return False

    def is_available(self) -> bool:
        """
        Check if Mailpit is running and accessible.

        Returns:
            bool: True if Mailpit is available
        """
        try:
            # Try to connect to Mailpit SMTP port
            with socket.create_connection((self.host, self.port), timeout=5):
                return True
        except (socket.error, ConnectionRefusedError, OSError):
            return False

    def get_status(self) -> dict[str, Any]:
        """
        Get Mailpit service status.

        Returns:
            Dict containing status information
        """
        available = self.is_available()

        return {
            "service": "Mailpit",
            "type": "development",
            "available": available,
            "host": self.host,
            "smtp_port": self.port,
            "web_ui": f"http://{self.host}:{self.web_ui_port}",
            "web_ui_port": self.web_ui_port,
            "requires_auth": False,
            "supports_tls": False,
            "default_sender": self.default_sender,
            "status_message": "Ready for email capture"
            if available
            else "Mailpit not running",
            "description": "Local email testing with web interface",
        }

    def get_service_info(self) -> dict[str, Any]:
        """
        Get basic Mailpit service information.

        Returns:
            Dict containing basic service info
        """
        return {
            "name": "Mailpit",
            "type": "development",
            "description": "Local email testing tool with web interface",
            "website": "https://github.com/axllent/mailpit",
        }
