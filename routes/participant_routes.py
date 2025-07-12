"""
Participant management routes for the Secret Santa application.

Refactored to use single responsibility functions for better maintainability.
"""

from flask import Blueprint
from werkzeug.wrappers import Response
from src.wichteln.forms import (
    ParticipantForm,
    ParticipantRemoveForm,
)
from services.validators import SecretSantaValidator
from services.debug_logger import DebugLogger
from services.request_handler import process_form_request


def create_participant_routes(game, recaptcha_service) -> Blueprint:
    """Create blueprint for participant management routes."""

    participant_bp = Blueprint("participant", __name__)

    @participant_bp.route("/add", methods=["POST"])
    def add_participant() -> Response:
        """
        Add a participant to the game using single responsibility functions.

        Uses extracted validation, logging, and form processing functions
        for better separation of concerns and maintainability.

        Returns:
            Response: A redirect to the index page.
        """

        def business_logic(participant_form: ParticipantForm) -> tuple[bool, str]:
            """Business logic for adding a participant with single responsibility validation."""
            # Verify reCAPTCHA
            if not recaptcha_service.verify_recaptcha(participant_form.recaptcha_token):
                return False, "CAPTCHA verification failed. Please try again."

            # Validate uniqueness using single responsibility function
            is_unique, error_msg = SecretSantaValidator.validate_unique_participant(
                participant_form.name,
                str(participant_form.email),
                game.participant_emails,
            )
            if not is_unique:
                return False, error_msg

            # Add participant
            success, message = game.add_participant(
                participant_form.name, str(participant_form.email)
            )

            if success:
                # Use structured debug logging
                DebugLogger.log_participant_added(
                    participant_form.name,
                    str(participant_form.email),
                    len(game.participants),
                )

            return success, message

        # Use generic form processor for clean request handling
        return process_form_request(
            form_class=ParticipantForm,
            field_mapping={
                "name": "name",
                "email": "email",
                "recaptcha_token": "g-recaptcha-response",
            },
            business_logic=business_logic,
            debug_context="add_participant",
        )

    @participant_bp.route("/remove", methods=["POST"])
    def remove_participant() -> Response:
        """
        Remove a participant from the game using single responsibility functions.

        Uses extracted validation, logging, and form processing functions
        for better separation of concerns and maintainability.

        Returns:
            Response: A redirect to the index page.
        """

        def business_logic(participant_form: ParticipantRemoveForm) -> tuple[bool, str]:
            """Business logic for removing a participant with single responsibility validation."""
            # Validate participant exists using single responsibility function
            exists, error_msg = SecretSantaValidator.validate_participant_exists(
                participant_form.name, game.participant_emails
            )
            if not exists:
                return False, error_msg

            # Validate admin permissions using single responsibility function
            is_allowed, admin_error = SecretSantaValidator.validate_admin_permissions(
                participant_form.name, game.participants
            )
            if not is_allowed:
                return False, admin_error

            # Remove participant
            success, message = game.remove_participant(participant_form.name)

            if success:
                # Use structured debug logging
                DebugLogger.log_participant_removed(
                    participant_form.name, len(game.participants)
                )

            return success, message

        # Use generic form processor for clean request handling
        return process_form_request(
            form_class=ParticipantRemoveForm,
            field_mapping={"name": "name"},
            business_logic=business_logic,
            debug_context="remove_participant",
        )

    return participant_bp
