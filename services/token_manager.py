"""
Token management utilities for the Secret Santa application.

This module provides utilities for generating, storing, and managing
confirmation tokens for assignment operations. Each class has a single
responsibility following the SRP principle.
"""

import uuid
from typing import Dict, Any, Optional, Tuple, Protocol


class EmailServiceProtocol(Protocol):
    """Protocol for email service implementations."""

    def send_confirmation_email(
        self, creator_email: str, confirmation_url: str
    ) -> bool:
        """Send confirmation email to creator."""
        ...

    def send_assignment_email(
        self, giver_email: str, giver_name: str, receiver_name: str
    ) -> bool:
        """Send assignment email to participant."""
        ...


class TokenGenerator:
    """Single responsibility: Generate unique tokens."""

    @staticmethod
    def generate_uuid_token() -> str:
        """Generate a unique UUID token.

        Single responsibility: Token generation only.

        Returns:
            Unique UUID string
        """
        return str(uuid.uuid4())

    @staticmethod
    def validate_token_format(token: str) -> bool:
        """Validate that a token has correct UUID format.

        Single responsibility: Token format validation.

        Args:
            token: Token string to validate

        Returns:
            True if token is valid UUID format
        """
        try:
            uuid.UUID(token)
            return len(token) == 36 and token.count("-") == 4
        except (ValueError, AttributeError):
            return False


class AssignmentStorage:
    """Single responsibility: Store and retrieve assignments by token."""

    def __init__(self, storage: Dict[str, Dict[str, str]]):
        """Initialize with storage dictionary.

        Args:
            storage: Dictionary to store assignments by token
        """
        self._storage = storage

    def store_assignment(self, token: str, assignments: Dict[str, str]) -> None:
        """Store assignments with token.

        Single responsibility: Assignment storage only.

        Args:
            token: Token to associate with assignments
            assignments: Dictionary of giver -> receiver assignments
        """
        self._storage[token] = assignments

    def retrieve_assignment(self, token: str) -> Optional[Dict[str, str]]:
        """Retrieve assignments by token without removing.

        Single responsibility: Assignment retrieval only.

        Args:
            token: Token to look up

        Returns:
            Assignments dictionary or None if not found
        """
        return self._storage.get(token)

    def remove_assignment(self, token: str) -> Optional[Dict[str, str]]:
        """Remove and return assignments by token.

        Single responsibility: Assignment removal only.

        Args:
            token: Token to remove

        Returns:
            Removed assignments or None if not found
        """
        return self._storage.pop(token, None)

    def token_exists(self, token: str) -> bool:
        """Check if token exists in storage.

        Single responsibility: Token existence check only.

        Args:
            token: Token to check

        Returns:
            True if token exists
        """
        return token in self._storage

    def clear_all(self) -> None:
        """Clear all stored assignments.

        Single responsibility: Storage cleanup only.
        """
        self._storage.clear()

    def get_count(self) -> int:
        """Get number of stored assignments.

        Single responsibility: Count retrieval only.

        Returns:
            Number of stored assignments
        """
        return len(self._storage)


class TokenManager:
    """Manages confirmation tokens for Secret Santa assignments.

    Composed of single responsibility components for better maintainability.
    """

    def __init__(self, pending_assignments: Dict[str, Dict[str, str]]):
        """Initialize token manager with storage and components.

        Args:
            pending_assignments: Dictionary to store pending assignments by token
        """
        self.storage = AssignmentStorage(pending_assignments)
        self.generator = TokenGenerator()

    def generate_confirmation_token(self, assignments: Dict[str, str]) -> str:
        """Generate a unique confirmation token and store assignments.

        Orchestrates token generation and storage operations.

        Args:
            assignments: Dictionary mapping giver names to receiver names

        Returns:
            Unique token string
        """
        token = self.generator.generate_uuid_token()
        self.storage.store_assignment(token, assignments)
        return token

    def retrieve_assignments(self, token: str) -> Optional[Dict[str, str]]:
        """Retrieve and remove assignments for a given token.

        Args:
            token: The confirmation token

        Returns:
            Dictionary of assignments if token is valid, None otherwise
        """
        return self.storage.remove_assignment(token)

    def validate_token_exists(self, token: str) -> bool:
        """Check if a token exists in pending assignments.

        Args:
            token: The token to check

        Returns:
            True if token exists, False otherwise
        """
        return self.storage.token_exists(token)

    def validate_token_format(self, token: str) -> bool:
        """Validate token format.

        Args:
            token: Token to validate

        Returns:
            True if token has valid format
        """
        return self.generator.validate_token_format(token)

    def clear_all_tokens(self) -> None:
        """Clear all pending assignment tokens."""
        self.storage.clear_all()

    def get_pending_count(self) -> int:
        """Get the number of pending assignment tokens.

        Returns:
            Number of pending tokens
        """
        return self.storage.get_count()


class UrlGenerator:
    """Utility for generating URLs with tokens."""

    @staticmethod
    def create_confirmation_url(url_for_func: Any, token: str) -> str:
        """Create a confirmation URL with the given token.

        Args:
            url_for_func: Flask's url_for function
            token: The confirmation token

        Returns:
            Full confirmation URL
        """
        return url_for_func(
            "assignment.confirm_assignments", token=token, _external=True
        )


class AssignmentProcessor:
    """Processes assignment confirmations and email sending."""

    def __init__(self, token_manager: TokenManager, email_service: Any):
        """Initialize the assignment processor.

        Args:
            token_manager: Token manager instance
            email_service: Email service for sending notifications
        """
        self.token_manager = token_manager
        self.email_service = email_service

    def create_pending_assignment(self, assignments: Dict[str, str]) -> str:
        """Create a pending assignment with confirmation token.

        Args:
            assignments: Dictionary of Secret Santa assignments

        Returns:
            Confirmation token
        """
        return self.token_manager.generate_confirmation_token(assignments)

    def process_confirmation(
        self, token: str, participant_emails: Dict[str, str]
    ) -> Tuple[bool, str, Optional[Dict[str, str]]]:
        """Process assignment confirmation and send emails.

        Args:
            token: Confirmation token
            participant_emails: Mapping of participant names to emails

        Returns:
            Tuple of (success, message, assignments_sent)
        """
        assignments = self.token_manager.retrieve_assignments(token)

        if not assignments:
            return False, "Invalid or expired confirmation link.", None

        # Send assignment emails
        email_sender = EmailBatchSender(self.email_service)
        successful, total, failed_participants = email_sender.send_assignment_batch(
            assignments, participant_emails
        )

        if successful == total:
            return (
                True,
                MessageFormatter.format_assignment_success_message(),
                assignments,
            )
        else:
            return (
                False,
                MessageFormatter.format_assignment_partial_success_message(
                    successful, total
                ),
                assignments,
            )

    def send_confirmation_email(
        self, creator_email: str, confirmation_url: str
    ) -> Tuple[bool, str]:
        """Send confirmation email to the game creator.

        Args:
            creator_email: Email address of the game creator
            confirmation_url: URL for confirming assignments

        Returns:
            Tuple of (success, message)
        """
        success = self.email_service.send_confirmation_email(
            creator_email, confirmation_url
        )

        if success:
            return True, MessageFormatter.format_confirmation_success_message(
                creator_email
            )
        else:
            return False, MessageFormatter.format_confirmation_failure_message()


class EmailBatchSender:
    """Single responsibility: Send multiple assignment emails efficiently."""

    def __init__(self, email_service: EmailServiceProtocol):
        """Initialize with email service.

        Args:
            email_service: Email service implementation
        """
        self.email_service = email_service

    def send_assignment_batch(
        self, assignments: Dict[str, str], participant_emails: Dict[str, str]
    ) -> Tuple[int, int, list[str]]:
        """Send assignment emails to all participants.

        Single responsibility: Batch email sending only.

        Args:
            assignments: Dictionary mapping giver names to receiver names
            participant_emails: Dictionary mapping names to email addresses

        Returns:
            Tuple of (successful_sends, total_attempts, failed_participants)
        """
        successful = 0
        total = 0
        failed_participants = []

        for giver, receiver in assignments.items():
            giver_email = participant_emails.get(giver)
            if giver_email:
                total += 1
                success = self.email_service.send_assignment_email(
                    str(giver_email), giver, receiver
                )
                if success:
                    successful += 1
                else:
                    failed_participants.append(giver)

        return successful, total, failed_participants


class MessageFormatter:
    """Single responsibility: Format status and response messages."""

    @staticmethod
    def format_confirmation_success_message(creator_email: str) -> str:
        """Format success message for confirmation email.

        Single responsibility: Success message formatting only.

        Args:
            creator_email: Email address where confirmation was sent

        Returns:
            Formatted success message
        """
        return f"Confirmation email sent to {creator_email}. Please check your inbox to finalize assignments."

    @staticmethod
    def format_confirmation_failure_message() -> str:
        """Format failure message for confirmation email.

        Single responsibility: Failure message formatting only.

        Returns:
            Formatted failure message
        """
        return "Failed to send confirmation email. Please check your mail server configuration."

    @staticmethod
    def format_assignment_success_message() -> str:
        """Format success message for assignment completion.

        Single responsibility: Assignment success message formatting only.

        Returns:
            Formatted success message
        """
        return "Secret Santa assignments have been sent!"

    @staticmethod
    def format_assignment_partial_success_message(successful: int, total: int) -> str:
        """Format partial success message for assignment emails.

        Single responsibility: Partial success message formatting only.

        Args:
            successful: Number of successful sends
            total: Total number of attempts

        Returns:
            Formatted partial success message
        """
        return f"Partially successful: {successful}/{total} assignment emails sent."

    @staticmethod
    def format_invalid_token_message() -> str:
        """Format message for invalid or expired tokens.

        Single responsibility: Invalid token message formatting only.

        Returns:
            Formatted invalid token message
        """
        return "Invalid or expired confirmation link."
