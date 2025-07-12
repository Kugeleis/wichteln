"""
Business logic validators for the Secret Santa application.

This module provides reusable validation functions for business rules
and constraints specific to the Secret Santa game.
"""

from typing import Dict, List, Any, Tuple


class SecretSantaValidator:
    """Validator for Secret Santa business rules."""

    @staticmethod
    def validate_minimum_participants(
        participants: List[Dict[str, Any]], minimum: int = 2
    ) -> Tuple[bool, str]:
        """Validate that there are enough participants for the game.

        Args:
            participants: List of participant dictionaries
            minimum: Minimum number of participants required

        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(participants) < minimum:
            return (
                False,
                f"Need at least {minimum} participants to assign Secret Santas.",
            )
        return True, ""

    @staticmethod
    def validate_participant_exists(
        name: str, participant_emails: Dict[str, str]
    ) -> Tuple[bool, str]:
        """Validate that a participant exists in the game.

        Args:
            name: Name of the participant to check
            participant_emails: Dictionary mapping names to emails

        Returns:
            Tuple of (exists, error_message)
        """
        if not name:
            return False, "Name is required."

        if name not in participant_emails:
            return False, f"Participant '{name}' not found."

        return True, ""

    @staticmethod
    def validate_unique_participant(
        name: str, email: str, participant_emails: Dict[str, str]
    ) -> Tuple[bool, str]:
        """Validate that a participant name and email are unique.

        Args:
            name: Name to check for uniqueness
            email: Email to check for uniqueness
            participant_emails: Current participant mapping

        Returns:
            Tuple of (is_unique, error_message)
        """
        if not name or not email:
            return False, "Name and email are required."

        # Check for duplicate name
        if name in participant_emails:
            return False, f"A participant with the name '{name}' was already added."

        # Check for duplicate email
        if email in participant_emails.values():
            return False, f"A participant with the email '{email}' was already added."

        return True, ""

    @staticmethod
    def validate_admin_permissions(
        participant_name: str, participants: List[Dict[str, Any]]
    ) -> Tuple[bool, str]:
        """Validate if a participant has admin permissions (is the first participant).

        Args:
            participant_name: Name of the participant to check
            participants: List of all participants

        Returns:
            Tuple of (is_admin, error_message)
        """
        if not participants:
            return False, "No participants found."

        admin_participant = participants[0]
        if str(admin_participant["name"]) == participant_name:
            return False, "Cannot remove the admin participant."

        return True, ""

    @staticmethod
    def validate_confirmation_token(token: str) -> Tuple[bool, str]:
        """Validate a confirmation token format.

        Args:
            token: The token to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not token:
            return False, "Token is required."

        # Basic UUID format validation (can be enhanced)
        if len(token) != 36 or token.count("-") != 4:
            return False, "Invalid token format."

        return True, ""


class MailServiceValidator:
    """Validator for mail service related operations."""

    @staticmethod
    def validate_development_mode_access(
        mail_service_status: Dict[str, Any],
    ) -> Tuple[bool, str]:
        """Validate that development features are accessible.

        Args:
            mail_service_status: Status dictionary from mail service

        Returns:
            Tuple of (is_allowed, error_message)
        """
        if mail_service_status.get("type") != "development":
            return False, "This route is only available in development mode"

        return True, ""

    @staticmethod
    def validate_email_recipient(email: str) -> Tuple[bool, str]:
        """Validate an email recipient address.

        Args:
            email: Email address to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return False, "Email address is required."

        if "@" not in email:
            return False, "Invalid email format."

        return True, ""


class RecaptchaValidator:
    """Validator for reCAPTCHA related operations."""

    # Development mode placeholder - not a real secret
    DEFAULT_PLACEHOLDER_KEY = "YOUR_RECAPTCHA_SECRET_KEY"  # nosec B105

    @staticmethod
    def should_skip_recaptcha(secret_key: str) -> bool:
        """Check if reCAPTCHA validation should be skipped.

        Args:
            secret_key: The configured reCAPTCHA secret key

        Returns:
            True if validation should be skipped
        """
        return secret_key == RecaptchaValidator.DEFAULT_PLACEHOLDER_KEY

    @staticmethod
    def validate_recaptcha_response(
        response_data: Dict[str, Any], score_threshold: float = 0.5
    ) -> bool:
        """Validate reCAPTCHA response data.

        Args:
            response_data: Response from Google's reCAPTCHA API
            score_threshold: Minimum score required for validation

        Returns:
            True if validation passes
        """
        return (
            response_data.get("success", False)
            and response_data.get("score", 0) > score_threshold
        )
