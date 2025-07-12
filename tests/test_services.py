"""
Tests for the email and recaptcha services.
"""

from unittest.mock import Mock, patch
from flask import Flask
from services.email_service import EmailService
from services.recaptcha_service import RecaptchaService


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


class TestRecaptchaService:
    """Test the RecaptchaService class."""

    def test_recaptcha_service_initialization(self):
        """Test RecaptchaService initialization."""
        app = Flask(__name__)
        app.config["RECAPTCHA_SECRET_KEY"] = "test-secret-key"

        recaptcha_service = RecaptchaService(app)

        assert recaptcha_service.app.config["RECAPTCHA_SECRET_KEY"] == "test-secret-key"

    def test_recaptcha_service_no_secret_key(self):
        """Test RecaptchaService with no secret key."""
        app = Flask(__name__)

        recaptcha_service = RecaptchaService(app)

        assert recaptcha_service.app.config.get("RECAPTCHA_SECRET_KEY") is None

    @patch("requests.post")
    def test_verify_recaptcha_success(self, mock_post):
        """Test successful reCAPTCHA verification."""
        app = Flask(__name__)
        app.config["RECAPTCHA_SECRET_KEY"] = "test-secret-key"

        # Mock successful response with high score
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "score": 0.8}
        mock_post.return_value = mock_response

        recaptcha_service = RecaptchaService(app)

        result = recaptcha_service.verify_recaptcha("test-token")

        assert result is True
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_verify_recaptcha_failure(self, mock_post):
        """Test failed reCAPTCHA verification."""
        app = Flask(__name__)
        app.config["RECAPTCHA_SECRET_KEY"] = "test-secret-key"

        # Mock failed response
        mock_response = Mock()
        mock_response.json.return_value = {"success": False}
        mock_post.return_value = mock_response

        recaptcha_service = RecaptchaService(app)

        result = recaptcha_service.verify_recaptcha("test-token")

        assert result is False

    def test_verify_recaptcha_no_secret_key(self):
        """Test reCAPTCHA verification with no secret key."""
        app = Flask(__name__)
        app.config["RECAPTCHA_SECRET_KEY"] = (
            "YOUR_RECAPTCHA_SECRET_KEY"  # Development mode
        )

        recaptcha_service = RecaptchaService(app)

        result = recaptcha_service.verify_recaptcha("test-token")

        # Should return True when no secret key is configured (development mode)
        assert result is True

    @patch("requests.post")
    def test_verify_recaptcha_request_exception(self, mock_post):
        """Test reCAPTCHA verification with request exception."""
        app = Flask(__name__)
        app.config["RECAPTCHA_SECRET_KEY"] = "test-secret-key"

        # Mock request exception
        mock_post.side_effect = Exception("Connection error")

        recaptcha_service = RecaptchaService(app)

        result = recaptcha_service.verify_recaptcha("test-token")

        assert result is False
