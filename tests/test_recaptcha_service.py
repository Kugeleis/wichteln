"""
Tests for the RecaptchaService class.
"""

from unittest.mock import Mock, patch
from flask import Flask
from services.recaptcha_service import RecaptchaService


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
