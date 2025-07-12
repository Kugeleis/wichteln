"""
Debug logging utilities for the Secret Santa application.

This module provides centralized debug logging functionality
to help with development and troubleshooting.
"""

from typing import Any, Dict, List


class DebugLogger:
    """Centralized debug logging for development."""

    @staticmethod
    def log_participant_added(name: str, email: str, total_count: int) -> None:
        """Log when a participant is added.

        Args:
            name: Name of the added participant
            email: Email of the added participant
            total_count: Total number of participants after addition
        """
        print(f"DEBUG: Added participant {name} ({email})")
        print(f"DEBUG: Total participants now: {total_count}")

    @staticmethod
    def log_participant_removed(name: str, total_count: int) -> None:
        """Log when a participant is removed.

        Args:
            name: Name of the removed participant
            total_count: Total number of participants after removal
        """
        print(f"DEBUG: Removed participant {name}")
        print(f"DEBUG: Total participants now: {total_count}")

    @staticmethod
    def log_participants_list(participants: List[Dict[str, Any]]) -> None:
        """Log the current list of participants.

        Args:
            participants: List of participant dictionaries
        """
        print(f"DEBUG: Rendering index with {len(participants)} participants")
        for i, participant in enumerate(participants):
            print(
                f"DEBUG: Participant {i + 1}: {participant['name']} ({participant['email']})"
            )

    @staticmethod
    def log_assignments_created(assignments: Dict[str, str]) -> None:
        """Log when Secret Santa assignments are created.

        Args:
            assignments: Dictionary mapping givers to receivers
        """
        print(f"DEBUG: Created {len(assignments)} Secret Santa assignments")
        for giver, receiver in assignments.items():
            print(f"DEBUG: {giver} -> {receiver}")

    @staticmethod
    def log_email_sent(recipient: str, subject: str, success: bool) -> None:
        """Log email sending attempts.

        Args:
            recipient: Email recipient
            subject: Email subject
            success: Whether the email was sent successfully
        """
        status = "SUCCESS" if success else "FAILED"
        print(f"DEBUG: Email {status} - To: {recipient}, Subject: {subject}")

    @staticmethod
    def log_recaptcha_verification(token: str | None, success: bool) -> None:
        """Log reCAPTCHA verification attempts.

        Args:
            token: The reCAPTCHA token (truncated for security)
            success: Whether verification was successful
        """
        token_display = f"{token[:8]}..." if token and len(token) > 8 else "None"
        status = "SUCCESS" if success else "FAILED"
        print(f"DEBUG: reCAPTCHA verification {status} - Token: {token_display}")

    @staticmethod
    def log_operation_context(operation: str, context: Dict[str, Any]) -> None:
        """Log general operation context for debugging.

        Args:
            operation: Description of the operation
            context: Additional context information
        """
        print(f"DEBUG: {operation}")
        for key, value in context.items():
            print(f"DEBUG:   {key}: {value}")

    @staticmethod
    def log_error(error: Exception, context: str = "") -> None:
        """Log errors with context.

        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
        """
        context_str = f" in {context}" if context else ""
        print(f"ERROR{context_str}: {type(error).__name__}: {error}")


def debug_context(**kwargs: Any) -> Dict[str, Any]:
    """Helper function to create debug context dictionaries.

    Args:
        **kwargs: Key-value pairs for context

    Returns:
        Dictionary of context information
    """
    return kwargs
