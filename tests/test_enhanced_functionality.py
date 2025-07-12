"""
Test coverage for the enhanced participant routes and email batch processor.

This test suite validates the newly incorporated functionality from the examples.
"""

from unittest.mock import Mock, patch
from flask import Flask

from services.email_service import EmailBatchProcessor
from services.debug_logger import DebugLogger
from services.request_handler import process_form_request
from src.wichteln.forms import ParticipantForm


class TestEmailBatchProcessor:
    """Test the new EmailBatchProcessor functionality."""

    def test_send_assignment_batch_success(self):
        """Test successful batch email sending."""
        mock_email_service = Mock()
        mock_email_service.send_assignment_email.return_value = True

        batch_processor = EmailBatchProcessor(mock_email_service)
        assignments = {"Alice": "Bob", "Bob": "Charlie"}
        participant_emails = {"Alice": "alice@example.com", "Bob": "bob@example.com"}

        successful, total, failed = batch_processor.send_assignment_batch(
            assignments, participant_emails
        )

        assert successful == 2
        assert total == 2
        assert len(failed) == 0

        # Verify calls were made correctly
        assert mock_email_service.send_assignment_email.call_count == 2
        mock_email_service.send_assignment_email.assert_any_call(
            "alice@example.com", "Alice", "Bob"
        )
        mock_email_service.send_assignment_email.assert_any_call(
            "bob@example.com", "Bob", "Charlie"
        )

    def test_send_assignment_batch_partial_failure(self):
        """Test batch processing with some failures."""
        mock_email_service = Mock()
        mock_email_service.send_assignment_email.side_effect = [True, False]

        batch_processor = EmailBatchProcessor(mock_email_service)
        assignments = {"Alice": "Bob", "Bob": "Charlie"}
        participant_emails = {"Alice": "alice@example.com", "Bob": "bob@example.com"}

        successful, total, failed = batch_processor.send_assignment_batch(
            assignments, participant_emails
        )

        assert successful == 1
        assert total == 2
        assert failed == ["Bob"]

    def test_send_assignment_batch_missing_emails(self):
        """Test batch processing with missing participant emails."""
        mock_email_service = Mock()
        mock_email_service.send_assignment_email.return_value = True

        batch_processor = EmailBatchProcessor(mock_email_service)
        assignments = {"Alice": "Bob", "Bob": "Charlie"}
        participant_emails = {"Alice": "alice@example.com"}  # Missing Bob

        successful, total, failed = batch_processor.send_assignment_batch(
            assignments, participant_emails
        )

        assert successful == 1  # Alice has email and succeeds
        assert total == 1  # Only Alice has email, so only 1 attempt
        assert len(failed) == 0  # Alice succeeded, Bob wasn't attempted


class TestDebugLogger:
    """Test the debug logging functionality."""

    @patch("builtins.print")
    def test_log_participant_added(self, mock_print):
        """Test participant addition logging."""
        DebugLogger.log_participant_added("Alice", "alice@example.com", 3)

        assert mock_print.call_count == 2
        mock_print.assert_any_call("DEBUG: Added participant Alice (alice@example.com)")
        mock_print.assert_any_call("DEBUG: Total participants now: 3")

    @patch("builtins.print")
    def test_log_participant_removed(self, mock_print):
        """Test participant removal logging."""
        DebugLogger.log_participant_removed("Bob", 2)

        assert mock_print.call_count == 2
        mock_print.assert_any_call("DEBUG: Removed participant Bob")
        mock_print.assert_any_call("DEBUG: Total participants now: 2")


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


class TestIntegratedFunctionality:
    """Test the integration of all enhanced functionality."""

    def test_enhanced_participant_workflow(self):
        """Test the complete enhanced participant management workflow."""
        # Mock all dependencies
        mock_game = Mock()
        mock_game.participant_emails = {"Alice": "alice@example.com"}
        mock_game.participants = [{"name": "Alice"}, {"name": "Bob"}]
        mock_game.add_participant.return_value = (True, "Participant added!")

        mock_recaptcha = Mock()
        mock_recaptcha.verify_recaptcha.return_value = True

        # Test that validators would be called in the new workflow
        from services.validators import SecretSantaValidator

        # Test unique participant validation
        is_unique, msg = SecretSantaValidator.validate_unique_participant(
            "Charlie", "charlie@example.com", mock_game.participant_emails
        )
        assert is_unique is True
        assert msg == ""

        # Test duplicate participant validation
        is_unique, msg = SecretSantaValidator.validate_unique_participant(
            "Alice", "alice@example.com", mock_game.participant_emails
        )
        assert is_unique is False
        assert "already added" in msg

        # Test participant existence validation
        exists, msg = SecretSantaValidator.validate_participant_exists(
            "Alice", mock_game.participant_emails
        )
        assert exists is True
        assert msg == ""

        # Test admin permissions validation
        is_allowed, msg = SecretSantaValidator.validate_admin_permissions(
            "Bob", mock_game.participants
        )
        assert is_allowed is True
        assert msg == ""

        # Test admin cannot be removed
        is_allowed, msg = SecretSantaValidator.validate_admin_permissions(
            "Alice", mock_game.participants
        )
        assert is_allowed is False
        assert "Cannot remove the admin" in msg
