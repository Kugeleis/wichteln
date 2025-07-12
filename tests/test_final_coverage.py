"""
Additional targeted tests to achieve 100% code coverage.

This module provides specific tests for the remaining uncovered lines identified
in the coverage analysis.
"""

from unittest.mock import Mock, patch
import pytest
from flask import Flask

from src.mail_service import (
    MailServiceFactory,
    EmailMessage,
    SMTPMailService,
)
from src.mail_service.protocol import MailProtocol


class TestProtocolAbstractMethodCoverage:
    """Test abstract methods in protocol to get coverage."""

    def test_abstract_method_definitions(self) -> None:
        """Test abstract method definitions in the protocol."""

        # Create a mock implementation to test abstract methods
        class MockImplementation(MailProtocol):
            def send_email(self, message: EmailMessage) -> bool:
                return True

            def is_available(self) -> bool:
                return True

            def get_status(self) -> dict:
                return {"status": "mock"}

            def get_service_info(self) -> dict:
                return {"name": "mock"}

        # Test that we can create an implementation
        impl = MockImplementation()
        assert impl.send_email(EmailMessage("test", "test@example.com", "body"))
        assert impl.is_available()
        assert impl.get_status()["status"] == "mock"
        assert impl.get_service_info()["name"] == "mock"


class TestFactoryRemainingLines:
    """Test the remaining uncovered lines in factory.py."""

    def test_factory_print_statements_in_start_mailpit(self) -> None:
        """Test the print statements in start_mailpit method."""
        with (
            patch("os.path.exists", return_value=True),
            patch("subprocess.Popen"),
            patch.object(MailServiceFactory, "_create_mailpit_service") as mock_create,
            patch("time.sleep"),
            patch("builtins.print") as mock_print,
        ):
            # Mock service that will fail after startup
            mock_service = Mock()
            mock_service.is_available.side_effect = [
                False,
                False,
            ]  # Never becomes available
            mock_create.return_value = mock_service

            result = MailServiceFactory.start_mailpit()
            assert result is False

            # Check that the "failed to start" message was printed (lines 230-231)
            mock_print.assert_any_call("❌ Mailpit failed to start")

    def test_factory_exception_handling_in_start_mailpit(self) -> None:
        """Test exception handling in start_mailpit."""
        with (
            patch("os.path.exists", return_value=True),
            patch("subprocess.Popen", side_effect=FileNotFoundError("File not found")),
            patch.object(MailServiceFactory, "_create_mailpit_service") as mock_create,
            patch("builtins.print") as mock_print,
        ):
            mock_service = Mock()
            mock_service.is_available.return_value = False
            mock_create.return_value = mock_service

            result = MailServiceFactory.start_mailpit()
            assert result is False

            # Check that the exception message was printed
            mock_print.assert_any_call("❌ Failed to start Mailpit: File not found")


class TestSMTPRemainingLines:
    """Test the remaining uncovered lines in smtp.py."""

    def test_smtp_service_exception_in_send_email(self) -> None:
        """Test SMTP service exception handling in send_email (line 133)."""
        app = Flask(__name__)
        service = SMTPMailService(app=app, server="smtp.example.com", port=587)

        # Mock the mail.send to raise a specific exception
        with patch.object(service.mail, "send", side_effect=Exception("Network error")):
            message = EmailMessage(
                subject="Test", recipient="test@example.com", body="Test body"
            )

            result = service.send_email(message)
            assert result is False


class TestFormsRemainingLines:
    """Test the remaining uncovered lines in forms.py."""

    def test_forms_validate_form_data_error_formatting(self) -> None:
        """Test error formatting in validate_form_data (lines 69-70)."""
        from src.wichteln.forms import validate_form_data, ParticipantForm

        # Create form data that will cause validation errors
        form_data = {
            "name": "",  # Empty name will cause validation error
            "email": "invalid-email",  # Invalid email format
            "recaptcha_token": "test-token",
        }

        validated_data, errors = validate_form_data(ParticipantForm, form_data)
        assert validated_data is None
        assert len(errors) > 0

        # Check that errors are properly formatted as "Field: message"
        for error in errors:
            assert isinstance(error, str)
            assert ":" in error  # Should have "Field: message" format


if __name__ == "__main__":
    pytest.main([__file__])
