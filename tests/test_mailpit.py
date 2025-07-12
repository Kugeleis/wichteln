"""
Tests for src/mail_service/mailpit.py.

This module provides comprehensive tests for the MailpitMailService class,
including email sending, status checking, and service availability.
"""

from unittest.mock import Mock, patch
import pytest

from src.mail_service import EmailMessage, MailpitMailService


class TestMailpitMailService:
    """Test MailpitMailService class."""

    @pytest.fixture
    def mailpit_service(self) -> MailpitMailService:
        """Create a MailpitMailService instance for testing."""
        return MailpitMailService(host="localhost", port=1025, web_ui_port=8025)

    @pytest.fixture
    def sample_email(self) -> EmailMessage:
        """Create a sample email message for testing."""
        return EmailMessage(
            recipient="test@example.com",
            subject="Test Subject",
            body="Test Body",
            sender="sender@example.com",
        )

    @patch("smtplib.SMTP")
    def test_send_email_success(
        self,
        mock_smtp_class: Mock,
        mailpit_service: MailpitMailService,
        sample_email: EmailMessage,
    ) -> None:
        """Test successful email sending."""
        mock_smtp = Mock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp

        with patch("builtins.print"):  # Suppress print statements
            result = mailpit_service.send_email(sample_email)

        assert result is True
        mock_smtp.sendmail.assert_called_once()

    @patch("smtplib.SMTP")
    def test_send_email_failure(
        self,
        mock_smtp_class: Mock,
        mailpit_service: MailpitMailService,
        sample_email: EmailMessage,
    ) -> None:
        """Test email sending failure."""
        mock_smtp_class.side_effect = Exception("SMTP Error")

        result = mailpit_service.send_email(sample_email)

        assert result is False

    @patch("socket.create_connection")
    def test_is_available_success(
        self, mock_connection: Mock, mailpit_service: MailpitMailService
    ) -> None:
        """Test service availability check when service is available."""
        mock_connection.return_value.__enter__.return_value = Mock()

        result = mailpit_service.is_available()

        assert result is True
        mock_connection.assert_called_once_with(("localhost", 1025), timeout=5)

    @patch("socket.create_connection")
    def test_is_available_failure(
        self, mock_connection: Mock, mailpit_service: MailpitMailService
    ) -> None:
        """Test service availability check when service is not available."""
        mock_connection.side_effect = ConnectionRefusedError("Connection failed")

        result = mailpit_service.is_available()

        assert result is False

    def test_get_status(self, mailpit_service: MailpitMailService) -> None:
        """Test getting service status information."""
        with patch.object(mailpit_service, "is_available", return_value=True):
            status = mailpit_service.get_status()

            assert status["host"] == "localhost"
            assert status["smtp_port"] == 1025
            assert status["web_ui"] == "http://localhost:8025"
            assert status["service"] == "Mailpit"


if __name__ == "__main__":
    pytest.main([__file__])
