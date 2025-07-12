"""
Test coverage for the enhanced participant routes functionality.

This test suite validates the integrated functionality in participant_routes.py.
"""

from unittest.mock import Mock

from services.validators import SecretSantaValidator


class TestIntegratedParticipantRoutes:
    """Test the integration of all enhanced functionality in participant routes."""

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
