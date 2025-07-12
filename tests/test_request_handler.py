"""
Test coverage for the enhanced request handler functionality.

This test suite validates the process_form_request function in request_handler.py.
"""

from unittest.mock import patch
from flask import Flask

from services.request_handler import process_form_request
from src.wichteln.forms import ParticipantForm


class TestEnhancedFormProcessing:
    """Test the enhanced form processing functionality."""

    def test_process_form_request_success(self):
        """Test successful form request processing."""
        # Mock the Flask app context and request
        app = Flask(__name__)

        with app.test_request_context(
            "/test",
            method="POST",
            data={
                "name": "Alice",
                "email": "alice@example.com",
                "g-recaptcha-response": "valid-token",
            },
        ):

            def mock_business_logic(form: ParticipantForm) -> tuple[bool, str]:
                assert form.name == "Alice"
                assert form.email == "alice@example.com"
                return True, "Participant added successfully!"

            # Mock flash and redirect
            with (
                patch("services.request_handler.flash") as mock_flash,
                patch("services.request_handler.redirect") as mock_redirect,
                patch("services.request_handler.url_for") as mock_url_for,
            ):
                mock_url_for.return_value = "/test"
                mock_redirect.return_value = "redirect_response"

                result = process_form_request(
                    form_class=ParticipantForm,
                    field_mapping={
                        "name": "name",
                        "email": "email",
                        "recaptcha_token": "g-recaptcha-response",
                    },
                    business_logic=mock_business_logic,
                    debug_context="test_add",
                )

                mock_flash.assert_called_once_with(
                    "Participant added successfully!", "success"
                )
                assert result == "redirect_response"

    def test_process_form_request_validation_failure(self):
        """Test form request processing with validation errors."""
        app = Flask(__name__)

        with app.test_request_context(
            "/test",
            method="POST",
            data={
                "name": "",  # Invalid: empty name
                "email": "invalid-email",  # Invalid: bad email format
            },
        ):

            def mock_business_logic(form: ParticipantForm) -> tuple[bool, str]:
                return True, "Should not be called"

            with (
                patch("services.request_handler.flash") as mock_flash,
                patch("services.request_handler.redirect") as mock_redirect,
                patch("services.request_handler.url_for") as mock_url_for,
            ):
                mock_url_for.return_value = "/test"
                mock_redirect.return_value = "redirect_response"

                result = process_form_request(
                    form_class=ParticipantForm,
                    field_mapping={
                        "name": "name",
                        "email": "email",
                        "recaptcha_token": "g-recaptcha-response",
                    },
                    business_logic=mock_business_logic,
                    debug_context="test_add",
                )

                # Should flash validation errors
                mock_flash.assert_called_once()
                args = mock_flash.call_args[0]
                assert "Invalid input:" in args[0]
                assert args[1] == "error"
                assert result == "redirect_response"

    def test_process_form_request_business_logic_failure(self):
        """Test form request processing when business logic fails."""
        app = Flask(__name__)

        with app.test_request_context(
            "/test",
            method="POST",
            data={
                "name": "Alice",
                "email": "alice@example.com",
                "g-recaptcha-response": "valid-token",
            },
        ):

            def mock_business_logic(form: ParticipantForm) -> tuple[bool, str]:
                return False, "Business logic failed!"

            with (
                patch("services.request_handler.flash") as mock_flash,
                patch("services.request_handler.redirect") as mock_redirect,
                patch("services.request_handler.url_for") as mock_url_for,
            ):
                mock_url_for.return_value = "/test"
                mock_redirect.return_value = "redirect_response"

                result = process_form_request(
                    form_class=ParticipantForm,
                    field_mapping={
                        "name": "name",
                        "email": "email",
                        "recaptcha_token": "g-recaptcha-response",
                    },
                    business_logic=mock_business_logic,
                    debug_context="test_add",
                )

                mock_flash.assert_called_once_with("Business logic failed!", "error")
                assert result == "redirect_response"
