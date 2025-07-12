"""
Test coverage for validator single responsibility functions.

This test suite targets the extracted validator functions from services.validators
to ensure they are thoroughly tested and covered.
"""

import uuid

from services.validators import (
    SecretSantaValidator,
    MailServiceValidator,
    RecaptchaValidator,
)


class TestSecretSantaValidator:
    """Test single responsibility validator functions."""

    def test_validate_minimum_participants_success(self):
        """Test successful participant validation."""
        participants = [{"name": "Alice"}, {"name": "Bob"}]
        is_valid, message = SecretSantaValidator.validate_minimum_participants(
            participants
        )
        assert is_valid is True
        assert message == ""

    def test_validate_minimum_participants_failure(self):
        """Test failed participant validation."""
        participants = [{"name": "Alice"}]
        is_valid, message = SecretSantaValidator.validate_minimum_participants(
            participants
        )
        assert is_valid is False
        assert "Need at least 2 participants" in message

    def test_validate_minimum_participants_custom_minimum(self):
        """Test custom minimum participant count."""
        participants = [{"name": "Alice"}, {"name": "Bob"}]
        is_valid, message = SecretSantaValidator.validate_minimum_participants(
            participants, minimum=3
        )
        assert is_valid is False
        assert "Need at least 3 participants" in message

    def test_validate_participant_exists_success(self):
        """Test successful participant existence check."""
        participant_emails = {"Alice": "alice@example.com", "Bob": "bob@example.com"}
        exists, message = SecretSantaValidator.validate_participant_exists(
            "Alice", participant_emails
        )
        assert exists is True
        assert message == ""

    def test_validate_participant_exists_failure(self):
        """Test failed participant existence check."""
        participant_emails = {"Alice": "alice@example.com"}
        exists, message = SecretSantaValidator.validate_participant_exists(
            "Bob", participant_emails
        )
        assert exists is False
        assert "not found" in message

    def test_validate_participant_exists_empty_name(self):
        """Test participant existence check with empty name."""
        participant_emails = {"Alice": "alice@example.com"}
        exists, message = SecretSantaValidator.validate_participant_exists(
            "", participant_emails
        )
        assert exists is False
        assert "required" in message

    def test_validate_unique_participant_success(self):
        """Test successful unique participant validation."""
        participant_emails = {"Alice": "alice@example.com"}
        is_unique, message = SecretSantaValidator.validate_unique_participant(
            "Bob", "bob@example.com", participant_emails
        )
        assert is_unique is True
        assert message == ""

    def test_validate_unique_participant_duplicate_name(self):
        """Test duplicate name validation."""
        participant_emails = {"Alice": "alice@example.com"}
        is_unique, message = SecretSantaValidator.validate_unique_participant(
            "Alice", "alice2@example.com", participant_emails
        )
        assert is_unique is False
        assert "already added" in message

    def test_validate_unique_participant_duplicate_email(self):
        """Test duplicate email validation."""
        participant_emails = {"Alice": "alice@example.com"}
        is_unique, message = SecretSantaValidator.validate_unique_participant(
            "Bob", "alice@example.com", participant_emails
        )
        assert is_unique is False
        assert "already added" in message

    def test_validate_admin_permissions_success(self):
        """Test admin permission validation success."""
        participants = [{"name": "Alice"}, {"name": "Bob"}]
        is_admin, message = SecretSantaValidator.validate_admin_permissions(
            "Bob", participants
        )
        assert is_admin is True
        assert message == ""

    def test_validate_admin_permissions_admin_removal(self):
        """Test admin permission validation for admin removal."""
        participants = [{"name": "Alice"}, {"name": "Bob"}]
        is_admin, message = SecretSantaValidator.validate_admin_permissions(
            "Alice", participants
        )
        assert is_admin is False
        assert "Cannot remove the admin" in message

    def test_validate_confirmation_token_success(self):
        """Test valid confirmation token."""
        token = str(uuid.uuid4())
        is_valid, message = SecretSantaValidator.validate_confirmation_token(token)
        assert is_valid is True
        assert message == ""

    def test_validate_confirmation_token_invalid_format(self):
        """Test invalid token format."""
        is_valid, message = SecretSantaValidator.validate_confirmation_token(
            "invalid-token"
        )
        assert is_valid is False
        assert "Invalid token format" in message


class TestMailServiceValidator:
    """Test mail service validator functions."""

    def test_validate_development_mode_access_success(self):
        """Test successful development mode validation."""
        status = {"type": "development"}
        is_allowed, message = MailServiceValidator.validate_development_mode_access(
            status
        )
        assert is_allowed is True
        assert message == ""

    def test_validate_development_mode_access_failure(self):
        """Test failed development mode validation."""
        status = {"type": "production"}
        is_allowed, message = MailServiceValidator.validate_development_mode_access(
            status
        )
        assert is_allowed is False
        assert "only available in development mode" in message

    def test_validate_email_recipient_success(self):
        """Test successful email validation."""
        is_valid, message = MailServiceValidator.validate_email_recipient(
            "test@example.com"
        )
        assert is_valid is True
        assert message == ""

    def test_validate_email_recipient_empty(self):
        """Test empty email validation."""
        is_valid, message = MailServiceValidator.validate_email_recipient("")
        assert is_valid is False
        assert "required" in message

    def test_validate_email_recipient_invalid_format(self):
        """Test invalid email format."""
        is_valid, message = MailServiceValidator.validate_email_recipient(
            "invalid-email"
        )
        assert is_valid is False
        assert "Invalid email format" in message


class TestRecaptchaValidator:
    """Test reCAPTCHA validator functions."""

    def test_should_skip_recaptcha_default_key(self):
        """Test reCAPTCHA skip for default key."""
        should_skip = RecaptchaValidator.should_skip_recaptcha(
            "YOUR_RECAPTCHA_SECRET_KEY"
        )
        assert should_skip is True

    def test_should_skip_recaptcha_real_key(self):
        """Test reCAPTCHA validation for real key."""
        should_skip = RecaptchaValidator.should_skip_recaptcha("real-secret-key")
        assert should_skip is False

    def test_validate_recaptcha_response_success(self):
        """Test successful reCAPTCHA validation."""
        response_data = {"success": True, "score": 0.8}
        is_valid = RecaptchaValidator.validate_recaptcha_response(response_data)
        assert is_valid is True

    def test_validate_recaptcha_response_low_score(self):
        """Test reCAPTCHA validation with low score."""
        response_data = {"success": True, "score": 0.3}
        is_valid = RecaptchaValidator.validate_recaptcha_response(response_data)
        assert is_valid is False

    def test_validate_recaptcha_response_failure(self):
        """Test failed reCAPTCHA validation."""
        response_data = {"success": False, "score": 0.8}
        is_valid = RecaptchaValidator.validate_recaptcha_response(response_data)
        assert is_valid is False
