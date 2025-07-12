"""
Application factory and service initialization for the Secret Santa application.
"""

import os
from flask import Flask
from src.wichteln.main import SecretSanta
from src.mail_service import MailServiceFactory, MailpitMailService

from services.email_service import EmailService
from services.recaptcha_service import RecaptchaService
from routes.main_routes import create_main_routes
from routes.participant_routes import create_participant_routes
from routes.assignment_routes import create_assignment_routes


def create_app() -> Flask:
    """Create and configure the Flask application."""
    # Get the directory one level up from this file (project root)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_folder = os.path.join(project_root, "templates")
    static_folder = os.path.join(project_root, "static")

    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    # Configuration
    app.config["RECAPTCHA_SECRET_KEY"] = os.environ.get(
        "RECAPTCHA_SECRET_KEY", "YOUR_RECAPTCHA_SECRET_KEY"
    )
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "a_very_secret_key")

    return app


def initialize_services(app: Flask) -> tuple:
    """Initialize all services and return them."""
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

    # Initialize service classes
    email_service = EmailService(mail_service)
    recaptcha_service = RecaptchaService(app)

    # Pending assignments storage
    pending_assignments: dict[str, dict[str, str]] = {}

    return game, email_service, recaptcha_service, pending_assignments


def register_blueprints(
    app: Flask, game, email_service, recaptcha_service, pending_assignments
):
    """Register all blueprints with the app."""
    # Create and register blueprints
    main_bp = create_main_routes(game, email_service)
    participant_bp = create_participant_routes(game, recaptcha_service)
    assignment_bp = create_assignment_routes(game, email_service, pending_assignments)

    app.register_blueprint(main_bp)
    app.register_blueprint(participant_bp)
    app.register_blueprint(assignment_bp)


def create_complete_app() -> Flask:
    """Create a fully configured Flask application with all services and routes."""
    # Create the app
    app = create_app()

    # Initialize services
    game, email_service, recaptcha_service, pending_assignments = initialize_services(
        app
    )

    # Register blueprints
    register_blueprints(
        app, game, email_service, recaptcha_service, pending_assignments
    )

    return app
