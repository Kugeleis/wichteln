"""
Helper functions and fixtures for testing.
"""

from services.app_factory import create_app, register_blueprints
from services.email_service import EmailService
from services.recaptcha_service import RecaptchaService
from src.mail_service import MailServiceFactory
from src.wichteln.main import SecretSanta


def create_test_app(game_instance=None, pending_assignments_instance=None):
    """Create a Flask app for testing with custom instances."""
    # Create the base app
    app = create_app()
    app.config["TESTING"] = True
    app.config["MAIL_SUPPRESS_SEND"] = True

    # Use provided instances or create new ones
    game = game_instance if game_instance is not None else SecretSanta()
    pending_assignments = (
        pending_assignments_instance if pending_assignments_instance is not None else {}
    )

    # Initialize services (using minimal setup for testing)
    mail_service = MailServiceFactory.create_mail_service(app)
    email_service = EmailService(mail_service)
    recaptcha_service = RecaptchaService(app)

    # Register blueprints with the test instances
    register_blueprints(
        app, game, email_service, recaptcha_service, pending_assignments
    )

    return app
