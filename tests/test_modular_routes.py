"""
Tests for the modular route structure.
"""

import pytest
from unittest.mock import Mock
from flask import Flask
from src.wichteln.main import SecretSanta
from routes.main_routes import create_main_routes
from routes.participant_routes import create_participant_routes
from routes.assignment_routes import create_assignment_routes
from services.email_service import EmailService
from services.recaptcha_service import RecaptchaService


class TestMainRoutes:
    """Test the main routes blueprint."""

    def test_create_main_routes_blueprint(self):
        """Test that the main routes blueprint is created correctly."""
        game = SecretSanta()
        email_service = Mock(spec=EmailService)

        blueprint = create_main_routes(game, email_service)

        assert blueprint.name == "main"
        assert len(blueprint.deferred_functions) >= 2  # index and test-email routes


class TestParticipantRoutes:
    """Test the participant routes blueprint."""

    def test_create_participant_routes_blueprint(self):
        """Test that the participant routes blueprint is created correctly."""
        game = SecretSanta()
        recaptcha_service = Mock(spec=RecaptchaService)

        blueprint = create_participant_routes(game, recaptcha_service)

        assert blueprint.name == "participant"
        assert len(blueprint.deferred_functions) >= 2  # add and remove routes


class TestAssignmentRoutes:
    """Test the assignment routes blueprint."""

    def test_create_assignment_routes_blueprint(self):
        """Test that the assignment routes blueprint is created correctly."""
        game = SecretSanta()
        email_service = Mock(spec=EmailService)
        pending_assignments = {}

        blueprint = create_assignment_routes(game, email_service, pending_assignments)

        assert blueprint.name == "assignment"
        assert len(blueprint.deferred_functions) >= 3  # assign, confirm, reset routes


class TestRouteFunctionality:
    """Test the actual route functionality."""

    @pytest.fixture
    def app(self):
        """Create a test Flask app with all routes registered."""
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret"

        # Create services
        game = SecretSanta()
        email_service = Mock(spec=EmailService)
        recaptcha_service = Mock(spec=RecaptchaService)
        pending_assignments = {}

        # Register blueprints
        app.register_blueprint(create_main_routes(game, email_service))
        app.register_blueprint(create_participant_routes(game, recaptcha_service))
        app.register_blueprint(
            create_assignment_routes(game, email_service, pending_assignments)
        )

        return app

    def test_assign_route_exists(self, app):
        """Test that the assign route exists."""
        with app.test_client() as client:
            response = client.post("/assign")
            # Should return some response (might be error due to no participants)
            assert response.status_code in [200, 302]

    def test_reset_route_exists(self, app):
        """Test that the reset route exists."""
        with app.test_client() as client:
            response = client.post("/reset")
            assert response.status_code in [200, 302]


class TestServiceIntegration:
    """Test service integration with routes."""

    def test_email_service_called_in_routes(self):
        """Test that email service methods can be called."""
        mock_mail_service = Mock()
        email_service = EmailService(mock_mail_service)

        # Test that the service has the expected methods
        assert hasattr(email_service, "send_email")
        assert hasattr(email_service, "send_confirmation_email")
        assert hasattr(email_service, "send_assignment_email")

    def test_recaptcha_service_called_in_routes(self):
        """Test that recaptcha service methods can be called."""
        app = Flask(__name__)
        app.config["RECAPTCHA_SECRET_KEY"] = "test-key"

        recaptcha_service = RecaptchaService(app)

        # Test that the service has the expected methods
        assert hasattr(recaptcha_service, "verify_recaptcha")
