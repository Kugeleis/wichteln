"""
Test coverage for the enhanced EmailBatchProcessor functionality.

This test suite validates the EmailBatchProcessor class added to email_service.py.
"""

from unittest.mock import Mock

from services.email_service import EmailBatchProcessor


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
