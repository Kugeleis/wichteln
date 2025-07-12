"""
Participant management routes for the Secret Santa application.
"""

from flask import Blueprint, request, redirect, url_for, flash
from werkzeug.wrappers import Response
from src.wichteln.forms import (
    ParticipantForm,
    ParticipantRemoveForm,
    validate_form_data,
)
from typing import cast


def create_participant_routes(game, recaptcha_service) -> Blueprint:
    """Create blueprint for participant management routes."""

    participant_bp = Blueprint("participant", __name__)

    @participant_bp.route("/add", methods=["POST"])
    def add_participant() -> Response:
        """
        Adds a participant to the game after form validation and reCAPTCHA verification.

        Retrieves and validates participant data from the form submission using Pydantic.
        If validation or reCAPTCHA verification fails, appropriate flash messages are displayed.

        Returns:
            Response: A redirect to the index page.
        """
        try:
            # Create form data dict from request
            form_data = {
                "name": request.form.get("name", ""),
                "email": request.form.get("email", ""),
                "recaptcha_token": request.form.get("g-recaptcha-response"),
            }

            # Validate with Pydantic
            participant_data, validation_errors = validate_form_data(
                ParticipantForm, form_data
            )

            if validation_errors:
                flash(f"Invalid input: {'; '.join(validation_errors)}", "error")
                return redirect(url_for("main.index"))

            # participant_data is guaranteed to be ParticipantForm instance here
            if participant_data is None:
                flash("An unexpected error occurred. Please try again.", "error")
                return redirect(url_for("main.index"))

            participant_form = cast(ParticipantForm, participant_data)

            # Verify reCAPTCHA
            if not recaptcha_service.verify_recaptcha(participant_form.recaptcha_token):
                flash("CAPTCHA verification failed. Please try again.", "error")
                return redirect(url_for("main.index"))

            # Add participant (now guaranteed to have valid data)
            success, message = game.add_participant(
                participant_form.name, str(participant_form.email)
            )

            if success:
                print(
                    f"DEBUG: Added participant {participant_form.name} ({participant_form.email})"
                )
                print(f"DEBUG: Total participants now: {len(game.participants)}")
                flash(message, "success")
            else:
                flash(message, "error")

        except Exception as e:
            flash("An unexpected error occurred. Please try again.", "error")
            print(f"Error in add_participant: {e}")

        return redirect(url_for("main.index"))

    @participant_bp.route("/remove", methods=["POST"])
    def remove_participant() -> Response:
        """
        Removes a participant from the game after form validation.

        Retrieves and validates participant name from the form submission using Pydantic.
        If validation fails, appropriate flash messages are displayed.

        Returns:
            Response: A redirect to the index page.
        """
        try:
            form_data = {
                "name": request.form.get("name", "").strip(),
            }

            # Validate with Pydantic
            participant_data, validation_errors = validate_form_data(
                ParticipantRemoveForm, form_data
            )

            if validation_errors:
                flash(f"Invalid input: {'; '.join(validation_errors)}", "error")
                return redirect(url_for("main.index"))

            # participant_data is guaranteed to be ParticipantRemoveForm instance here
            if participant_data is None:
                flash("An unexpected error occurred. Please try again.", "error")
                return redirect(url_for("main.index"))

            participant_form = cast(ParticipantRemoveForm, participant_data)

            # Remove participant
            success, message = game.remove_participant(participant_form.name)

            if success:
                print(f"DEBUG: Removed participant {participant_form.name}")
                print(f"DEBUG: Total participants now: {len(game.participants)}")
                flash(message, "success")
            else:
                flash(message, "error")

        except Exception as e:
            flash("An unexpected error occurred. Please try again.", "error")
            print(f"Error in remove_participant: {e}")

        return redirect(url_for("main.index"))

    return participant_bp
