"""
Main routes for the Secret Santa application.
"""

from flask import Blueprint, render_template


def create_main_routes(game, email_service) -> Blueprint:
    """Create blueprint for main routes."""

    main_bp = Blueprint("main", __name__)

    @main_bp.route("/")
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

    @main_bp.route("/dev/test-email")
    def test_email():
        """Development route to test email functionality with Mailpit."""
        # Check if we're in development mode or using Mailpit
        status = email_service.mail_service.get_status()
        if status["type"] != "development":
            return "This route is only available in development mode", 404

        try:
            success, response = email_service.send_test_email()
            return response
        except Exception as e:
            return f"""
            <h2>❌ Email Test Error</h2>
            <p>Error: {str(e)}</p>
            <p>Make sure Mailpit is running and accessible.</p>
            <hr>
            <p><a href="/">← Back to Wichteln</a></p>
            """

    return main_bp
