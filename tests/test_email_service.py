"""
Tests for the EmailService class.
"""

from unittest.mock import Mock
from services.email_service import EmailService


class TestEmailService:
    """Test the EmailService class."""

    def test_email_service_initialization(self):
        """Test EmailService initialization."""
        mock_mail_service = Mock()
        email_service = EmailService(mock_mail_service)

        assert email_service.mail_service == mock_mail_service

    def test_send_email_calls_mail_service(self):
        """Test that send_email calls the underlying mail service."""
        mock_mail_service = Mock()
        mock_mail_service.send_email.return_value = (True, "Email sent")

        email_service = EmailService(mock_mail_service)

        result = email_service.send_email(
            "test@example.com", "Test Subject", "Test Body"
        )

        assert result == (True, "Email sent")
        mock_mail_service.send_email.assert_called_once()

    def test_send_confirmation_email(self):
        """Test send_confirmation_email method."""
        mock_mail_service = Mock()
        mock_mail_service.send_email.return_value = (True, "Email sent")

        email_service = EmailService(mock_mail_service)

        result = email_service.send_confirmation_email(
            "test@example.com", "test-token-123"
        )

        assert result == (True, "Email sent")
        mock_mail_service.send_email.assert_called_once()

        # Check that the email contains the token
        call_args = mock_mail_service.send_email.call_args
        message = call_args[0][0]  # First positional argument is the EmailMessage
        assert "test-token-123" in message.body

    def test_send_assignment_email(self):
        """Test send_assignment_email method."""
        mock_mail_service = Mock()
        mock_mail_service.send_email.return_value = (True, "Email sent")

        email_service = EmailService(mock_mail_service)

        result = email_service.send_assignment_email(
            "test@example.com", "John Doe", "jane@example.com"
        )

        assert result == (True, "Email sent")
        mock_mail_service.send_email.assert_called_once()

        # Check that the email contains the assignment details
        call_args = mock_mail_service.send_email.call_args
        message = call_args[0][0]  # First positional argument is the EmailMessage
        assert "John Doe" in message.body
        assert "jane@example.com" in message.body
