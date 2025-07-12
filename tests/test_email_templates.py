"""
Test coverage for email template single responsibility functions.

This test suite targets the extracted template functions from services.email_templates
to ensure they are thoroughly tested and covered.
"""

from services.email_templates import EmailTemplateService, EmailAddressValidator


class TestEmailTemplateService:
    """Test email template service functions."""

    def test_create_confirmation_email_content(self):
        """Test confirmation email content generation."""
        link = "http://example.com/confirm/123"
        subject, body = EmailTemplateService.create_confirmation_email_content(link)

        assert "Confirm Secret Santa Assignments" in subject
        assert link in body
        assert "click the following link" in body

    def test_create_assignment_email_content(self):
        """Test assignment email content generation."""
        subject, body = EmailTemplateService.create_assignment_email_content(
            "Alice", "Bob"
        )

        assert "Your Secret Santa Assignment!" in subject
        assert "Alice" in body
        assert "Bob" in body
        assert "Secret Santa for:" in body

    def test_create_test_email_content(self):
        """Test test email content generation."""
        status = {"service": "Mock", "type": "development", "status_message": "Active"}
        subject, body = EmailTemplateService.create_test_email_content(status)

        assert "Test Email" in subject
        assert "Mock" in body
        assert "development" in body
        assert "Active" in body

    def test_create_test_email_response_success(self):
        """Test successful test email response."""
        response = EmailTemplateService.create_test_email_response(True, "Test Subject")

        assert "Test Email Sent Successfully" in response
        assert "Test Subject" in response
        assert "http://localhost:8025" in response

    def test_create_test_email_response_failure(self):
        """Test failed test email response."""
        response = EmailTemplateService.create_test_email_response(
            False, "Test Subject"
        )

        assert "Email Test Failed" in response
        assert "Make sure Mailpit is running" in response


class TestEmailAddressValidator:
    """Test email address validator functions."""

    def test_get_creator_email_with_participants(self):
        """Test creator email extraction with participants."""
        participants = [{"email": "creator@example.com"}, {"email": "user@example.com"}]
        creator_email = EmailAddressValidator.get_creator_email(participants)
        assert creator_email == "creator@example.com"

    def test_get_creator_email_without_participants(self):
        """Test creator email extraction without participants."""
        creator_email = EmailAddressValidator.get_creator_email([])
        assert creator_email == "admin@example.com"

    def test_get_creator_email_with_fallback(self):
        """Test creator email extraction with custom fallback."""
        creator_email = EmailAddressValidator.get_creator_email(
            [], "custom@example.com"
        )
        assert creator_email == "custom@example.com"

    def test_extract_participant_emails(self):
        """Test participant email extraction."""
        participants = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"},
        ]
        emails = EmailAddressValidator.extract_participant_emails(participants)

        assert emails == {"Alice": "alice@example.com", "Bob": "bob@example.com"}
