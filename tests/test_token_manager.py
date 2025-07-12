"""
Test coverage for token manager single responsibility functions.

This test suite targets the extracted token management functions from services.token_manager
to ensure they are thoroughly tested and covered.
"""

import uuid
from unittest.mock import Mock

from services.token_manager import (
    TokenGenerator,
    AssignmentStorage,
    EmailBatchSender,
    MessageFormatter,
    TokenManager,
    UrlGenerator,
    AssignmentProcessor,
)


class TestTokenGenerator:
    """Test token generator functions."""

    def test_generate_uuid_token(self):
        """Test UUID token generation."""
        token = TokenGenerator.generate_uuid_token()

        assert len(token) == 36
        assert token.count("-") == 4
        # Validate it's a proper UUID
        uuid.UUID(token)

    def test_validate_token_format_valid(self):
        """Test valid token format validation."""
        token = str(uuid.uuid4())
        is_valid = TokenGenerator.validate_token_format(token)
        assert is_valid is True

    def test_validate_token_format_invalid(self):
        """Test invalid token format validation."""
        is_valid = TokenGenerator.validate_token_format("invalid-token")
        assert is_valid is False

    def test_validate_token_format_empty(self):
        """Test empty string token format validation."""
        is_valid = TokenGenerator.validate_token_format("")
        assert is_valid is False


class TestAssignmentStorage:
    """Test assignment storage functions."""

    def test_store_and_retrieve_assignment(self):
        """Test assignment storage and retrieval."""
        storage_dict = {}
        storage = AssignmentStorage(storage_dict)

        token = "test-token"
        assignments = {"Alice": "Bob", "Bob": "Charlie"}

        storage.store_assignment(token, assignments)
        retrieved = storage.retrieve_assignment(token)

        assert retrieved == assignments

    def test_remove_assignment(self):
        """Test assignment removal."""
        storage_dict = {"token1": {"Alice": "Bob"}}
        storage = AssignmentStorage(storage_dict)

        removed = storage.remove_assignment("token1")
        assert removed == {"Alice": "Bob"}
        assert "token1" not in storage_dict

    def test_token_exists(self):
        """Test token existence check."""
        storage_dict = {"token1": {"Alice": "Bob"}}
        storage = AssignmentStorage(storage_dict)

        assert storage.token_exists("token1") is True
        assert storage.token_exists("nonexistent") is False

    def test_clear_all(self):
        """Test clearing all assignments."""
        storage_dict = {"token1": {"Alice": "Bob"}, "token2": {"Charlie": "David"}}
        storage = AssignmentStorage(storage_dict)

        storage.clear_all()
        assert len(storage_dict) == 0

    def test_get_count(self):
        """Test assignment count."""
        storage_dict = {"token1": {"Alice": "Bob"}, "token2": {"Charlie": "David"}}
        storage = AssignmentStorage(storage_dict)

        assert storage.get_count() == 2


class TestEmailBatchSender:
    """Test email batch sender functions."""

    def test_send_assignment_batch_success(self):
        """Test successful batch email sending."""
        mock_email_service = Mock()
        mock_email_service.send_assignment_email.return_value = True

        batch_sender = EmailBatchSender(mock_email_service)
        assignments = {"Alice": "Bob", "Bob": "Charlie"}
        participant_emails = {"Alice": "alice@example.com", "Bob": "bob@example.com"}

        successful, total, failed = batch_sender.send_assignment_batch(
            assignments, participant_emails
        )

        assert successful == 2
        assert total == 2
        assert len(failed) == 0

    def test_send_assignment_batch_partial_failure(self):
        """Test partial failure in batch email sending."""
        mock_email_service = Mock()
        mock_email_service.send_assignment_email.side_effect = [True, False]

        batch_sender = EmailBatchSender(mock_email_service)
        assignments = {"Alice": "Bob", "Bob": "Charlie"}
        participant_emails = {"Alice": "alice@example.com", "Bob": "bob@example.com"}

        successful, total, failed = batch_sender.send_assignment_batch(
            assignments, participant_emails
        )

        assert successful == 1
        assert total == 2
        assert failed == ["Bob"]

    def test_send_assignment_batch_missing_emails(self):
        """Test batch sending with missing participant emails."""
        mock_email_service = Mock()
        mock_email_service.send_assignment_email.return_value = True

        batch_sender = EmailBatchSender(mock_email_service)
        assignments = {"Alice": "Bob", "Bob": "Charlie"}
        participant_emails = {"Alice": "alice@example.com"}  # Missing Bob's email

        successful, total, failed = batch_sender.send_assignment_batch(
            assignments, participant_emails
        )

        assert successful == 1  # Alice has email and succeeds
        assert total == 1  # Only Alice has an email, so only 1 attempt
        assert len(failed) == 0  # Alice succeeded, Bob wasn't attempted


class TestMessageFormatter:
    """Test message formatter functions."""

    def test_format_confirmation_success_message(self):
        """Test confirmation success message formatting."""
        message = MessageFormatter.format_confirmation_success_message(
            "test@example.com"
        )
        assert "test@example.com" in message
        assert "check your inbox" in message

    def test_format_confirmation_failure_message(self):
        """Test confirmation failure message formatting."""
        message = MessageFormatter.format_confirmation_failure_message()
        assert "Failed to send" in message
        assert "mail server configuration" in message

    def test_format_assignment_success_message(self):
        """Test assignment success message formatting."""
        message = MessageFormatter.format_assignment_success_message()
        assert "assignments have been sent" in message

    def test_format_assignment_partial_success_message(self):
        """Test partial success message formatting."""
        message = MessageFormatter.format_assignment_partial_success_message(2, 3)
        assert "2/3" in message
        assert "Partially successful" in message

    def test_format_invalid_token_message(self):
        """Test invalid token message formatting."""
        message = MessageFormatter.format_invalid_token_message()
        assert "Invalid or expired" in message


class TestUrlGenerator:
    """Test URL generator functions."""

    def test_create_confirmation_url(self):
        """Test confirmation URL generation."""

        def mock_url_for(endpoint, **kwargs):
            token = kwargs.get("token", "")
            external = kwargs.get("_external", False)
            base = "http://localhost:5000" if external else ""
            return f"{base}/confirm/{token}"

        url = UrlGenerator.create_confirmation_url(mock_url_for, "test-token")
        assert "test-token" in url
        assert "http://localhost:5000" in url
        assert "/confirm/" in url


class TestTokenManager:
    """Test TokenManager integration with single responsibility components."""

    def test_generate_and_retrieve_assignments(self):
        """Test TokenManager using single responsibility components."""
        pending_assignments = {}
        token_manager = TokenManager(pending_assignments)

        assignments = {"Alice": "Bob", "Bob": "Charlie"}
        token = token_manager.generate_confirmation_token(assignments)

        assert token_manager.validate_token_exists(token)
        assert token_manager.validate_token_format(token)

        retrieved = token_manager.retrieve_assignments(token)
        assert retrieved == assignments
        assert not token_manager.validate_token_exists(token)  # Should be removed


class TestAssignmentProcessor:
    """Test AssignmentProcessor workflow functions."""

    def test_assignment_processor_workflow(self):
        """Test AssignmentProcessor using single responsibility functions."""
        mock_email_service = Mock()
        mock_email_service.send_confirmation_email.return_value = True
        mock_email_service.send_assignment_email.return_value = True

        pending_assignments = {}
        token_manager = TokenManager(pending_assignments)
        processor = AssignmentProcessor(token_manager, mock_email_service)

        # Create pending assignment
        assignments = {"Alice": "Bob", "Bob": "Charlie"}
        token = processor.create_pending_assignment(assignments)

        # Send confirmation email
        success, message = processor.send_confirmation_email(
            "creator@example.com", "http://test.com"
        )
        assert success is True
        assert "Confirmation email sent" in message

        # Process confirmation
        participant_emails = {"Alice": "alice@example.com", "Bob": "bob@example.com"}
        success, message, sent_assignments = processor.process_confirmation(
            token, participant_emails
        )

        assert success is True
        assert "assignments have been sent" in message
        assert sent_assignments == assignments
