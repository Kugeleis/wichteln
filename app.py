"""
This module contains the Flask application for the Secret Santa web interface.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.wrappers import Response
from src.wichteln.main import SecretSanta
from src.wichteln.forms import (
    ParticipantForm,
    AssignmentConfirmForm,
    validate_form_data,
)
from src.mail_service import MailServiceFactory, EmailMessage, MailpitMailService
from typing import cast
import uuid
import os
import requests

app = Flask(__name__)

# Google reCAPTCHA v3 configuration
app.config["RECAPTCHA_SECRET_KEY"] = os.environ.get(
    "RECAPTCHA_SECRET_KEY", "YOUR_RECAPTCHA_SECRET_KEY"
)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "a_very_secret_key")

# Initialize mail service using the factory
mail_service = MailServiceFactory.create_mail_service(app)

# Initialize game
game = SecretSanta()

# Print mail service status
status = mail_service.get_status()
print(f"📧 Mail Service: {status['service']} ({status['type']})")
print(f"   Status: {status['status_message']}")
if status.get("web_ui"):
    print(f"   🌐 Web UI: {status['web_ui']}")

# Try to start Mailpit if in development and using SMTP fallback
if MailServiceFactory._is_development_mode() and not isinstance(
    mail_service, MailpitMailService
):
    print("🚀 Attempting to start Mailpit...")
    if MailServiceFactory.start_mailpit("./mailpit/mailpit.exe"):
        # Recreate mail service to use Mailpit now that it's running
        print("🔄 Switching to Mailpit service...")
        mail_service = MailServiceFactory.create_mail_service(app)
        status = mail_service.get_status()
        print(f"📧 Mail Service: {status['service']} ({status['type']})")
        print(f"   Status: {status['status_message']}")
        if status.get("web_ui"):
            print(f"   🌐 Web UI: {status['web_ui']}")

pending_assignments: dict[str, dict[str, str]] = {}


def send_email(recipient_email: str, subject: str, body: str) -> bool:
    """
    Sends an email to the specified recipient using the configured mail service.

    Args:
        recipient_email (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        message = EmailMessage(recipient=recipient_email, subject=subject, body=body)
        return mail_service.send_email(message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def verify_recaptcha(token: str | None) -> bool:
    """
    Verifies the reCAPTCHA token with Google's reCAPTCHA service.

    Args:
        token (str | None): The reCAPTCHA token received from the frontend.

    Returns:
        bool: True if the reCAPTCHA verification is successful and the score is above the threshold, False otherwise.
    """
    if not token:
        return False

    if app.config["RECAPTCHA_SECRET_KEY"] == "YOUR_RECAPTCHA_SECRET_KEY":
        print("WARNING: reCAPTCHA secret key not configured. Skipping verification.")
        return True  # Skip verification if key is not set

    payload = {"secret": app.config["RECAPTCHA_SECRET_KEY"], "response": token}
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=payload, timeout=10
    )
    result = response.json()
    return (
        result.get("success", False) and result.get("score", 0) > 0.5
    )  # Adjust score threshold as needed


@app.route("/")
def index() -> str:
    """
    Renders the main page of the Secret Santa application.

    Returns:
        str: The rendered HTML content of the index page.
    """
    print(f"DEBUG: Rendering index with {len(game.participants)} participants")
    for i, p in enumerate(game.participants):
        print(f"DEBUG: Participant {i + 1}: {p['name']} ({p['email']})")
    return render_template("index.html", participants=game.participants)


@app.route("/dev/test-email")
def test_email():
    """Development route to test email functionality with Mailpit."""
    # Check if we're in development mode or using Mailpit
    status = mail_service.get_status()
    if status["type"] != "development":
        return "This route is only available in development mode", 404

    try:
        subject = "🎄 Test Email from Wichteln App"
        body = f"""Hello from your Wichteln application!

This is a test email to verify that email integration is working correctly.

Configuration:
- Mail Service: {status["service"]} ({status["type"]})
- Status: {status["status_message"]}
- Timestamp: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

If you can see this email in Mailpit at http://localhost:8025,
your email configuration is working perfectly!

Happy Secret Santa organizing! 🎅
"""

        success = send_email("test@example.com", subject, body)

        if success:
            return f"""
            <h2>✅ Test Email Sent Successfully!</h2>
            <p>Check your emails in Mailpit: <a href="http://localhost:8025" target="_blank">http://localhost:8025</a></p>
            <p>Email sent to: test@example.com</p>
            <p>Subject: {subject}</p>
            <hr>
            <p><a href="/">← Back to Wichteln</a></p>
            """
        else:
            return """
            <h2>❌ Email Test Failed</h2>
            <p>Could not send test email. Check the console for error details.</p>
            <p>Make sure Mailpit is running on localhost:1025</p>
            <hr>
            <p><a href="/">← Back to Wichteln</a></p>
            """
    except Exception as e:
        return f"""
        <h2>❌ Email Test Error</h2>
        <p>Error: {str(e)}</p>
        <p>Make sure Mailpit is running and accessible.</p>
        <hr>
        <p><a href="/">← Back to Wichteln</a></p>
        """


@app.route("/add", methods=["POST"])
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
            return redirect(url_for("index"))

        # participant_data is guaranteed to be ParticipantForm instance here
        if participant_data is None:
            flash("An unexpected error occurred. Please try again.", "error")
            return redirect(url_for("index"))

        participant_form = cast(ParticipantForm, participant_data)

        # Verify reCAPTCHA
        if not verify_recaptcha(participant_form.recaptcha_token):
            flash("CAPTCHA verification failed. Please try again.", "error")
            return redirect(url_for("index"))

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

    return redirect(url_for("index"))


@app.route("/assign", methods=["POST"])
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
        return redirect(url_for("index"))

    game.assign_santas()

    # Generate a unique token for confirmation
    token = str(uuid.uuid4())
    pending_assignments[token] = game.assignments  # Store assignments temporarily

    # Assuming the first participant added is the creator for now.
    # In a real app, you'd have a dedicated creator input.
    creator_email = (
        game.participants[0]["email"]
        if game.participants
        else app.config["MAIL_DEFAULT_SENDER"]
    )

    confirmation_link = url_for("confirm_assignments", token=token, _external=True)
    subject = "Confirm Secret Santa Assignments"
    body = f"""Hello,

Please click the following link to confirm and send out the Secret Santa assignments: {confirmation_link}

This link will expire after one use or if the game is reset."""

    if send_email(creator_email, subject, body):
        flash(
            f"Confirmation email sent to {creator_email}. Please check your inbox to finalize assignments.",
            "info",
        )
    else:
        flash(
            "Failed to send confirmation email. Please check your mail server configuration.",
            "error",
        )

    return redirect(url_for("index"))


@app.route("/confirm/<token>")
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
        return redirect(url_for("index"))

    assignments_to_send = pending_assignments.pop(token, None)  # Retrieve and remove

    if assignments_to_send:
        for giver, receiver in assignments_to_send.items():
            giver_email = game.participant_emails.get(giver)
            if giver_email:
                subject = "Your Secret Santa Assignment!"
                body = f"""Hello {giver},

You are the Secret Santa for: {receiver}!"""
                send_email(giver_email, subject, body)
        flash("Secret Santa assignments have been sent!", "success")
        game.assignments = (
            assignments_to_send  # Update game's assignments after sending
        )
        # Clear participants list after successful assignment sending to maintain secrecy
        game.clear_participants()
    else:
        flash("Invalid or expired confirmation link.", "error")

    return redirect(url_for("index"))


@app.route("/reset", methods=["POST"])
def reset() -> Response:
    """
    Resets the game to its initial state, clearing all participants, assignments, and pending assignments.

    Returns:
        str: A redirect to the index page.
    """
    game.reset()
    pending_assignments.clear()  # Clear pending assignments on reset
    flash("Game has been reset.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Only enable debug mode in development environment
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "on", "1"]
    app.run(debug=debug_mode)
# This is a test comment for automated versioning.
