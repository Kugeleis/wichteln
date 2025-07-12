"""
Assignment and confirmation routes for the Secret Santa application.

Routes refactored to use single responsibility functions for better maintainability.
"""

from flask import Blueprint, redirect, url_for, flash
from werkzeug.wrappers import Response
from src.wichteln.forms import AssignmentConfirmForm, validate_form_data
from services.validators import SecretSantaValidator
from services.token_manager import TokenManager, UrlGenerator, AssignmentProcessor
from services.email_templates import EmailAddressValidator


def create_assignment_routes(game, email_service, pending_assignments) -> Blueprint:
    """Create blueprint for assignment and confirmation routes using single responsibility functions."""

    assignment_bp = Blueprint("assignment", __name__)

    # Initialize single responsibility components
    token_manager = TokenManager(pending_assignments)
    assignment_processor = AssignmentProcessor(token_manager, email_service)

    @assignment_bp.route("/assign", methods=["POST"])
    def assign_and_send_confirmation() -> Response:
        """
        Assigns Secret Santas using extracted single responsibility functions.

        Uses validator functions, token management utilities, and email processors
        to handle the assignment workflow with clear separation of concerns.

        Returns:
            Response: A redirect to the index page.
        """
        # Validation using single responsibility function
        is_valid, error_msg = SecretSantaValidator.validate_minimum_participants(
            game.participants
        )
        if not is_valid:
            flash(error_msg, "error")
            return redirect(url_for("main.index"))

        # Generate assignments
        game.assign_santas()

        # Create pending assignment using single responsibility function
        token = assignment_processor.create_pending_assignment(game.assignments)

        # Get creator email using single responsibility function
        creator_email = EmailAddressValidator.get_creator_email(game.participants)

        # Generate confirmation URL using single responsibility function
        confirmation_url = UrlGenerator.create_confirmation_url(url_for, token)

        # Send confirmation email using single responsibility function
        success, message = assignment_processor.send_confirmation_email(
            creator_email, confirmation_url
        )

        flash(message, "info" if success else "error")
        return redirect(url_for("main.index"))

    @assignment_bp.route("/confirm/<token>")
    def confirm_assignments(token: str) -> Response:
        """
        Confirms the Secret Santa assignments using single responsibility functions.

        Uses validation functions and assignment processors to handle
        the confirmation workflow with clear separation of concerns.

        Args:
            token: The unique token received from the confirmation email.

        Returns:
            Response: A redirect to the index page.
        """
        # Validate token format using single responsibility function
        token_data, validation_errors = validate_form_data(
            AssignmentConfirmForm, {"token": token}
        )

        if validation_errors:
            flash("Invalid or expired confirmation link.", "error")
            return redirect(url_for("main.index"))

        # Process confirmation using single responsibility function
        success, message, assignments_sent = assignment_processor.process_confirmation(
            token, game.participant_emails
        )

        if success and assignments_sent:
            # Update game state
            game.assignments = assignments_sent
            # Clear participants for secrecy
            game.clear_participants()
            flash(message, "success")
        else:
            flash(message, "error")

        return redirect(url_for("main.index"))

    @assignment_bp.route("/reset", methods=["POST"])
    def reset() -> Response:
        """
        Resets the game using single responsibility functions.

        Returns:
            Response: A redirect to the index page.
        """
        game.reset()
        token_manager.clear_all_tokens()  # Clear pending assignments using single responsibility function
        flash("Game has been reset.", "info")
        return redirect(url_for("main.index"))

    return assignment_bp
