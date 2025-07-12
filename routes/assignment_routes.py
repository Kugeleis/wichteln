"""
Assignment and confirmation routes for the Secret Santa application.
"""

from flask import Blueprint, redirect, url_for, flash
from werkzeug.wrappers import Response
from src.wichteln.forms import AssignmentConfirmForm, validate_form_data
import uuid


def create_assignment_routes(game, email_service, pending_assignments) -> Blueprint:
    """Create blueprint for assignment and confirmation routes."""

    assignment_bp = Blueprint("assignment", __name__)

    @assignment_bp.route("/assign", methods=["POST"])
    def assign_and_send_confirmation() -> Response:
        """
        Assigns Secret Santas, stores the assignments temporarily, and sends a confirmation email to the creator.

        If there are fewer than two participants, a flash message is displayed.
        A unique token is generated and associated with the assignments.
        A confirmation email with a link containing this token is sent to the creator.

        Returns:
            str: A redirect to the index page.
        """
        if len(game.participants) < 2:
            flash("Need at least two participants to assign Secret Santas.", "error")
            return redirect(url_for("main.index"))

        game.assign_santas()

        # Generate a unique token for confirmation
        token = str(uuid.uuid4())
        pending_assignments[token] = game.assignments  # Store assignments temporarily

        # Assuming the first participant added is the creator for now.
        # In a real app, you'd have a dedicated creator input.
        creator_email = (
            str(game.participants[0]["email"])
            if game.participants
            else "admin@example.com"  # fallback email
        )

        confirmation_link = url_for(
            "assignment.confirm_assignments", token=token, _external=True
        )

        if email_service.send_confirmation_email(creator_email, confirmation_link):
            flash(
                f"Confirmation email sent to {creator_email}. Please check your inbox to finalize assignments.",
                "info",
            )
        else:
            flash(
                "Failed to send confirmation email. Please check your mail server configuration.",
                "error",
            )

        return redirect(url_for("main.index"))

    @assignment_bp.route("/confirm/<token>")
    def confirm_assignments(token: str) -> Response:
        """
        Confirms the Secret Santa assignments and sends out the assignment emails to participants.

        Args:
            token (str): The unique token received from the confirmation email.

        Retrieves the pending assignments using the token.
        If the token is valid, assignment emails are sent to each participant.
        Flash messages indicate success or failure.

        Returns:
            str: A redirect to the index page.
        """
        # Validate token format first
        token_data, validation_errors = validate_form_data(
            AssignmentConfirmForm, {"token": token}
        )

        if validation_errors:
            flash("Invalid or expired confirmation link.", "error")
            return redirect(url_for("main.index"))

        assignments_to_send = pending_assignments.pop(
            token, None
        )  # Retrieve and remove

        if assignments_to_send:
            for giver, receiver in assignments_to_send.items():
                giver_email = game.participant_emails.get(giver)
                if giver_email:
                    email_service.send_assignment_email(
                        str(giver_email), giver, receiver
                    )

            flash("Secret Santa assignments have been sent!", "success")
            game.assignments = (
                assignments_to_send  # Update game's assignments after sending
            )
            # Clear participants list after successful assignment sending to maintain secrecy
            game.clear_participants()
        else:
            flash("Invalid or expired confirmation link.", "error")

        return redirect(url_for("main.index"))

    @assignment_bp.route("/reset", methods=["POST"])
    def reset() -> Response:
        """
        Resets the game to its initial state, clearing all participants, assignments, and pending assignments.

        Returns:
            str: A redirect to the index page.
        """
        game.reset()
        pending_assignments.clear()  # Clear pending assignments on reset
        flash("Game has been reset.", "info")
        return redirect(url_for("main.index"))

    return assignment_bp
