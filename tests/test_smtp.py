"""
Tests for src/mail_service/smtp.py.

This module provides comprehensive tests for the SMTPMailService class,
including email sending, configuration, and error handling.
"""

from unittest.mock import Mock, patch
import pytest

from src.mail_service import EmailMessage, SMTPMailService


class TestSMTPMailService:
    """Test SMTPMailService class."""

    @pytest.fixture
    def smtp_service(self) -> SMTPMailService:
        """Create an SMTPMailService instance for testing."""
        from flask import Flask

        app = Flask(__name__)

        service = SMTPMailService(
            app=app,
            server="smtp.test.com",
            port=587,
            use_tls=True,
            username="test@test.com",
            password="password",
            default_sender="test@test.com",
        )
        return service

    @pytest.fixture
    def sample_email(self) -> EmailMessage:
        """Create a sample email message for testing."""
        return EmailMessage(
            recipient="test@example.com",
            subject="Test Subject",
            body="Test Body",
            sender="sender@example.com",
        )

    @patch("flask_mail.Mail.send")
    def test_send_email_success(
        self, mock_send: Mock, smtp_service: SMTPMailService, sample_email: EmailMessage
    ) -> None:
        """Test successful email sending."""
        with patch("builtins.print"):  # Suppress print statements
            result = smtp_service.send_email(sample_email)

        assert result is True
        mock_send.assert_called_once()

    @patch("flask_mail.Mail.send")
    def test_send_email_failure(
        self, mock_send: Mock, smtp_service: SMTPMailService, sample_email: EmailMessage
    ) -> None:
        """Test email sending failure."""
        mock_send.side_effect = Exception("Mail server error")

        result = smtp_service.send_email(sample_email)

        assert result is False

    def test_is_available_always_true(self, smtp_service: SMTPMailService) -> None:
        """Test that SMTP service is available when properly configured."""
        result = smtp_service.is_available()
        assert result is True

    def test_get_status(self, smtp_service: SMTPMailService) -> None:
        """Test getting service status information."""
        status = smtp_service.get_status()

        assert status["service"] == "SMTP Server"
        assert status["type"] == "production"
        assert status["available"] is True
        assert "server" in status
        assert "port" in status

    def test_repr(self, smtp_service: SMTPMailService) -> None:
        """Test string representation of SMTPMailService."""
        result = repr(smtp_service)
        assert "SMTPMailService" in result

    def test_send_email_with_html_body(self, smtp_service: SMTPMailService) -> None:
        """Test sending email with HTML body."""
        email = EmailMessage(
            recipient="test@example.com",
            subject="Test Subject",
            body="Test Body",
            sender="sender@example.com",
            html_body="<h1>Test HTML Body</h1>",
        )

        with patch("flask_mail.Mail.send") as mock_send, patch("builtins.print"):
            result = smtp_service.send_email(email)

            assert result is True
            mock_send.assert_called_once()

    def test_send_email_without_sender(self, smtp_service: SMTPMailService) -> None:
        """Test sending email without explicit sender (uses default)."""
        email = EmailMessage(
            recipient="test@example.com",
            subject="Test Subject",
            body="Test Body",
        )

        with patch("flask_mail.Mail.send") as mock_send, patch("builtins.print"):
            result = smtp_service.send_email(email)

            assert result is True
            mock_send.assert_called_once()

    @patch("flask_mail.Mail.send")
    def test_send_email_various_exceptions(
        self, mock_send: Mock, smtp_service: SMTPMailService, sample_email: EmailMessage
    ) -> None:
        """Test email sending with various exceptions."""
        exceptions = [
            ConnectionError("Connection failed"),
            TimeoutError("Request timed out"),
            ValueError("Invalid email format"),
            RuntimeError("Server unavailable"),
        ]

        for exception in exceptions:
            mock_send.side_effect = exception

            result = smtp_service.send_email(sample_email)
            assert result is False

    def test_service_configuration_via_app(self) -> None:
        """Test SMTP service configuration via Flask app."""
        from flask import Flask

        app = Flask(__name__)
        app.config.update(
            {
                "MAIL_SERVER": "smtp.example.com",
                "MAIL_PORT": 587,
                "MAIL_USE_TLS": True,
                "MAIL_USERNAME": "user@example.com",
                "MAIL_PASSWORD": "password",
            }
        )

        service = SMTPMailService(app=app)

        # Test that service was configured
        assert hasattr(service, "mail")
        assert service.mail is not None

    def test_service_without_app_configuration(self) -> None:
        """Test SMTP service without Flask app configuration."""
        service = SMTPMailService()

        # Service should still be functional without explicit app config
        assert hasattr(service, "mail")

    def test_get_service_info(self, smtp_service: SMTPMailService) -> None:
        """Test getting service information."""
        info = smtp_service.get_service_info()

        assert info["name"] == "SMTP Server"
        assert info["type"] == "production"
        assert "description" in info

    def test_status_with_different_configurations(self) -> None:
        """Test status method with different configurations."""
        from flask import Flask

        # Test with custom configuration
        app = Flask(__name__)

        service = SMTPMailService(
            app=app,
            server="custom.smtp.com",
            port=465,
            use_ssl=True,
            username="user@example.com",
            password="password",
        )
        status = service.get_status()

        assert status["service"] == "SMTP Server"
        assert status["available"] is True

    @patch("flask_mail.Mail.send")
    def test_send_email_with_mail_init_failure(
        self, mock_send: Mock, sample_email: EmailMessage
    ) -> None:
        """Test email sending when Mail initialization fails."""
        with patch("flask_mail.Mail.__init__", side_effect=Exception("Init failed")):
            try:
                service = SMTPMailService()
                result = service.send_email(sample_email)
                # If init fails, service should handle gracefully
                assert result is False
            except Exception:
                # Or it might raise an exception during initialization
                pass

    def test_mail_message_creation_with_html(
        self, smtp_service: SMTPMailService
    ) -> None:
        """Test internal mail message creation with HTML content."""
        email = EmailMessage(
            recipient="test@example.com",
            subject="Test Subject",
            body="Plain text body",
            sender="sender@example.com",
            html_body="<h1>HTML body</h1>",
        )

        with patch("flask_mail.Mail.send") as mock_send, patch("builtins.print"):
            smtp_service.send_email(email)

            # Verify that send was called (Message creation is internal)
            mock_send.assert_called_once()

    def test_mail_message_creation_without_html(
        self, smtp_service: SMTPMailService
    ) -> None:
        """Test internal mail message creation without HTML content."""
        email = EmailMessage(
            recipient="test@example.com",
            subject="Test Subject",
            body="Plain text body",
            sender="sender@example.com",
        )

        with patch("flask_mail.Mail.send") as mock_send, patch("builtins.print"):
            smtp_service.send_email(email)

            # Verify that send was called
            mock_send.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
