"""
Test coverage for the enhanced debug logger functionality.

This test suite validates the DebugLogger class in debug_logger.py.
"""

from unittest.mock import patch

from services.debug_logger import DebugLogger


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
