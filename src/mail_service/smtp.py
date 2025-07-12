"""
SMTP mail service implementation.

This module provides a mail service implementation that uses real SMTP servers
for production email sending. Supports popular providers like Gmail, Outlook, etc.
"""

import os
from typing import Any, Optional
from flask import Flask
from flask_mail import Mail, Message
from .protocol import MailProtocol, EmailMessage


class SMTPMailService(MailProtocol):
    """
    Mail service implementation for real SMTP servers.

    This implementation uses Flask-Mail to send emails via real SMTP servers
    such as Gmail, Outlook, SendGrid, etc. Suitable for production use.
    """

    def __init__(self, app: Optional[Flask] = None, **config: Any) -> None:
        """
        Initialize SMTP mail service.

        Args:
            app: Flask application instance (optional)
            **config: Mail configuration parameters:
                - server: SMTP server hostname
                - port: SMTP server port
                - use_tls: Whether to use TLS
                - use_ssl: Whether to use SSL
                - username: SMTP username
                - password: SMTP password
                - default_sender: Default sender email
        """
        self.app = app
        self.mail: Optional[Mail] = None
        self.config = self._get_config(**config)

        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize the mail service with Flask app.

        Args:
            app: Flask application instance
        """
        self.app = app

        # Configure Flask-Mail
        for key, value in self.config.items():
            app.config[key] = value

        self.mail = Mail(app)

    def _get_config(self, **config: Any) -> dict[str, Any]:
        """
        Get mail configuration from environment variables or provided config.

        Args:
            **config: Override configuration

        Returns:
            Dict containing mail configuration
        """
        return {
            "MAIL_SERVER": config.get("server")
            or os.environ.get("MAIL_SERVER", "smtp.gmail.com"),
            "MAIL_PORT": config.get("port") or int(os.environ.get("MAIL_PORT", 587)),
            "MAIL_USE_TLS": config.get("use_tls", True)
            if "use_tls" in config
            else os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "1", "on"],
            "MAIL_USE_SSL": config.get("use_ssl", False)
            if "use_ssl" in config
            else os.environ.get("MAIL_USE_SSL", "false").lower() in ["true", "1", "on"],
            "MAIL_USERNAME": config.get("username") or os.environ.get("MAIL_USERNAME"),
            "MAIL_PASSWORD": config.get("password") or os.environ.get("MAIL_PASSWORD"),
            "MAIL_DEFAULT_SENDER": config.get("default_sender")
            or os.environ.get("MAIL_DEFAULT_SENDER", "noreply@example.com"),
        }

    def send_email(self, message: EmailMessage) -> bool:
        """
        Send email via real SMTP server.

        Args:
            message: EmailMessage object

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.mail:
            print("❌ SMTP mail service not initialized with Flask app")
            return False

        try:
            # Create Flask-Mail message
            msg = Message(
                subject=message.subject,
                recipients=[message.recipient],
                body=message.body,
                html=message.html_body,
                sender=message.sender or self.config["MAIL_DEFAULT_SENDER"],
            )

            # Send email
            self.mail.send(msg)
            print(
                f"📧 Email sent via {self.config['MAIL_SERVER']}: {message.recipient} - {message.subject}"
            )
            return True

        except Exception as e:
            print(f"❌ Failed to send email via {self.config['MAIL_SERVER']}: {e}")
            return False

    def is_available(self) -> bool:
        """
        Check if SMTP mail service is properly configured.

        Returns:
            bool: True if mail service appears to be configured
        """
        required_fields = ["MAIL_SERVER", "MAIL_PORT"]

        # Check if required configuration is present
        for field in required_fields:
            if not self.config.get(field):
                return False

        # For services requiring authentication, check credentials
        if self.config.get("MAIL_USE_TLS") or self.config.get("MAIL_USE_SSL"):
            if not self.config.get("MAIL_USERNAME") or not self.config.get(
                "MAIL_PASSWORD"
            ):
                return False

        return self.mail is not None

    def get_status(self) -> dict[str, Any]:
        """
        Get SMTP mail service status.

        Returns:
            Dict containing status information
        """
        available = self.is_available()

        status_msg = "Ready to send emails"
        if not available:
            if not self.mail:
                status_msg = "Not initialized with Flask app"
            elif not self.config.get("MAIL_USERNAME"):
                status_msg = "Missing authentication credentials"
            else:
                status_msg = "Configuration incomplete"

        return {
            "service": "SMTP Server",
            "type": "production",
            "available": available,
            "server": self.config.get("MAIL_SERVER", "Not configured"),
            "port": self.config.get("MAIL_PORT", "Not configured"),
            "use_tls": self.config.get("MAIL_USE_TLS", False),
            "use_ssl": self.config.get("MAIL_USE_SSL", False),
            "username": self.config.get("MAIL_USERNAME", "Not configured"),
            "default_sender": self.config.get("MAIL_DEFAULT_SENDER", "Not configured"),
            "requires_auth": bool(self.config.get("MAIL_USERNAME")),
            "status_message": status_msg,
            "description": "Production SMTP email service",
        }

    def get_service_info(self) -> dict[str, Any]:
        """
        Get basic SMTP service information.

        Returns:
            Dict containing basic service info
        """
        return {
            "name": "SMTP Server",
            "type": "production",
            "description": "Production email service using real SMTP servers",
            "supports": ["Gmail", "Outlook", "SendGrid", "Custom SMTP"],
        }
