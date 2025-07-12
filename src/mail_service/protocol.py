"""
Mail protocol definitions and interfaces.

This module defines the abstract protocol and data structures for email functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class EmailMessage:
    """
    Represents an email message.

    Attributes:
        recipient: Email address of the recipient
        subject: Subject line of the email
        body: Body content of the email (plain text)
        sender: Optional sender email address (uses default if not provided)
        html_body: Optional HTML version of the email body
    """

    recipient: str
    subject: str
    body: str
    sender: Optional[str] = None
    html_body: Optional[str] = None


class MailProtocol(ABC):
    """
    Abstract protocol for mail functionality.

    This defines the interface that all mail service implementations must follow.
    """

    @abstractmethod
    def send_email(self, message: EmailMessage) -> bool:
        """
        Send an email message.

        Args:
            message: EmailMessage object containing recipient, subject, and body

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the mail service is available and properly configured.

        Returns:
            bool: True if mail service is available, False otherwise
        """
        pass

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Get detailed status information about the mail service.

        Returns:
            Dict containing status information including:
            - service: Name of the service
            - type: "development" or "production"
            - available: Whether the service is available
            - status_message: Human-readable status description
            - Additional service-specific information
        """
        pass

    @abstractmethod
    def get_service_info(self) -> dict[str, Any]:
        """
        Get basic service information.

        Returns:
            Dict containing basic service info:
            - name: Service name
            - type: Service type
            - description: Service description
        """
        pass
