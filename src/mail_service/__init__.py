"""
Mail Service Module - A self-contained email abstraction layer.

This module provides a clean, protocol-based architecture for email functionality
with support for both development (Mailpit) and production (real SMTP) environments.

Usage:
    from src.mail_service import MailServiceFactory, EmailMessage

    # Auto-detect environment and create appropriate service
    mail_service = MailServiceFactory.create_mail_service()

    # Send an email
    message = EmailMessage(
        recipient="user@example.com",
        subject="Test Email",
        body="Hello World!"
    )
    success = mail_service.send_email(message)

For Flask integration:
    from src.mail_service import MailServiceFactory

    # Initialize with Flask app
    mail_service = MailServiceFactory.create_mail_service(app)

    # Or force a specific service type
    mail_service = MailServiceFactory.create_mail_service(app, force_type="mailpit")
"""

from .protocol import MailProtocol, EmailMessage
from .mailpit import MailpitMailService
from .smtp import SMTPMailService
from .factory import MailServiceFactory

__version__ = "1.0.0"

__all__ = [
    "MailProtocol",
    "EmailMessage",
    "MailpitMailService",
    "SMTPMailService",
    "MailServiceFactory",
]
