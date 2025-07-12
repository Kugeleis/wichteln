"""
Test coverage for email service single responsibility functions.

This test suite targets the email service integration with single responsibility functions
from services.email_service to ensure they are thoroughly tested and covered.
"""

from unittest.mock import Mock

from services.email_service import EmailService


class TestEmailServiceIntegration:
    """Test EmailService using single responsibility functions."""

    def test_email_service_with_single_responsibility_functions(self):
        """Test EmailService using single responsibility functions."""
        mock_mail_service = Mock()
        mock_mail_service.send_email.return_value = True
        mock_mail_service.get_status.return_value = {
            "service": "Mock",
            "type": "development",
            "status_message": "Active",
        }

        email_service = EmailService(mock_mail_service)

        # Test basic email sending with validation
        success = email_service.send_email("test@example.com", "Subject", "Body")
        assert success is True

        # Test confirmation email with template service
        success = email_service.send_confirmation_email(
            "creator@example.com", "http://test.com"
        )
        assert success is True

        # Test assignment email with template service
        success = email_service.send_assignment_email(
            "alice@example.com", "Alice", "Bob"
        )
        assert success is True

        # Test test email with all single responsibility functions
        success, response = email_service.send_test_email()
        assert success is True
        assert "Test Email Sent Successfully" in response

    def test_email_service_with_failed_email_sending(self):
        """Test EmailService behavior when email sending fails."""
        mock_mail_service = Mock()
        mock_mail_service.send_email.return_value = False
        mock_mail_service.get_status.return_value = {
            "service": "Mock",
            "type": "development",
            "status_message": "Active",
        }

        email_service = EmailService(mock_mail_service)

        # Test failed email sending
        success = email_service.send_email("test@example.com", "Subject", "Body")
        assert success is False

        # Test failed confirmation email
        success = email_service.send_confirmation_email(
            "creator@example.com", "http://test.com"
        )
        assert success is False

        # Test failed assignment email
        success = email_service.send_assignment_email(
            "alice@example.com", "Alice", "Bob"
        )
        assert success is False

        # Test failed test email
        success, response = email_service.send_test_email()
        assert success is False
        assert "Email Test Failed" in response

    def test_email_service_with_invalid_email_addresses(self):
        """Test EmailService validation with invalid email addresses."""
        mock_mail_service = Mock()
        mock_mail_service.send_email.return_value = True

        email_service = EmailService(mock_mail_service)

        # Test with invalid email format
        success = email_service.send_email("invalid-email", "Subject", "Body")
        assert success is False

        # Test with empty email
        success = email_service.send_email("", "Subject", "Body")
        assert success is False

    def test_email_service_test_email_in_production_mode(self):
        """Test that test email fails in production mode."""
        mock_mail_service = Mock()
        mock_mail_service.get_status.return_value = {
            "service": "SMTP",
            "type": "production",
            "status_message": "Active",
        }

        email_service = EmailService(mock_mail_service)

        # Test email should fail in production mode
        success, response = email_service.send_test_email()
        assert success is False
        assert "only available in development mode" in response
