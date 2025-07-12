"""
Tests for src/mail_service/factory.py.

This module provides comprehensive tests for the MailServiceFactory class,
including service creation, Mailpit management, and environment detection.
"""

from unittest.mock import Mock, patch
import pytest

from src.mail_service import (
    MailServiceFactory,
    MailpitMailService,
    SMTPMailService,
)


class TestMailServiceFactory:
    """Test MailServiceFactory class."""

    @pytest.fixture
    def mock_flask_app(self) -> Mock:
        """Create a mock Flask application."""
        app = Mock()
        app.config = {}
        app.debug = False
        app.testing = False
        app.extensions = {}  # Add extensions attribute for Flask-Mail
        return app

    def test_create_mail_service_defaults_to_mailpit_in_development(
        self, mock_flask_app: Mock
    ) -> None:
        """Test that factory creates Mailpit service by default in development."""
        with (
            patch.dict("os.environ", {"FLASK_ENV": "development"}),
            patch.object(MailpitMailService, "is_available", return_value=True),
        ):
            service = MailServiceFactory.create_mail_service(app=mock_flask_app)

            assert isinstance(service, MailpitMailService)

    def test_create_mail_service_with_force_type_smtp(
        self, mock_flask_app: Mock
    ) -> None:
        """Test that factory creates SMTP service when forced."""
        service = MailServiceFactory.create_mail_service(
            app=mock_flask_app, force_type="smtp"
        )

        assert isinstance(service, SMTPMailService)

    def test_create_mail_service_with_force_type_mailpit(self) -> None:
        """Test that factory creates Mailpit service when forced."""
        service = MailServiceFactory.create_mail_service(force_type="mailpit")

        assert isinstance(service, MailpitMailService)

    def test_get_service_creates_factory_and_returns_service(self) -> None:
        """Test that get_service method works as expected."""
        factory = MailServiceFactory()

        with patch.object(MailServiceFactory, "create_mail_service") as mock_create:
            mock_service = Mock()
            mock_create.return_value = mock_service

            result = factory.get_service()

            assert result == mock_service
            mock_create.assert_called_once()

    def test_get_available_services_returns_service_info(self) -> None:
        """Test that get_available_services returns proper service information."""
        services = MailServiceFactory.get_available_services()

        assert "mailpit" in services
        assert "smtp" in services
        assert services["mailpit"]["name"] == "Mailpit"
        assert services["smtp"]["name"] == "SMTP Server"

    @patch("os.path.exists")
    @patch("subprocess.Popen")
    @patch("time.sleep")
    def test_start_mailpit_with_existing_executable_succeeds(
        self, mock_sleep: Mock, mock_popen: Mock, mock_exists: Mock
    ) -> None:
        """Test that start_mailpit succeeds when executable exists."""
        # Setup mocks
        mock_exists.return_value = True
        mock_service = Mock()
        mock_service.is_available.side_effect = [
            False,
            True,
        ]  # First check fails, then succeeds after start
        mock_service.get_status.return_value = {
            "host": "localhost",
            "smtp_port": 1025,
            "web_ui": "http://localhost:8025",
        }

        with (
            patch.object(
                MailServiceFactory, "_create_mailpit_service", return_value=mock_service
            ),
            patch("builtins.print"),
        ):
            result = MailServiceFactory.start_mailpit()

            assert result is True
            mock_popen.assert_called_once()

    @patch("os.path.exists")
    def test_start_mailpit_with_missing_executable_fails(
        self, mock_exists: Mock
    ) -> None:
        """Test that start_mailpit fails when executable is missing."""
        mock_exists.return_value = False

        result = MailServiceFactory.start_mailpit()

        assert result is False

    # Coverage improvement tests from test_final_coverage.py and test_coverage_improvements.py
    def test_create_mailpit_service_when_mailpit_not_available(self) -> None:
        """Test factory behavior when Mailpit is not available."""
        with (
            patch.dict("os.environ", {"FLASK_ENV": "development"}),
            patch.object(MailpitMailService, "is_available", return_value=False),
        ):
            service = MailServiceFactory.create_mail_service()
            # Should fall back to SMTP when Mailpit not available
            assert isinstance(service, SMTPMailService)

    def test_create_mailpit_service_when_available(self) -> None:
        """Test factory creates Mailpit service when available."""
        with (
            patch.dict("os.environ", {"FLASK_ENV": "development"}),
            patch.object(MailpitMailService, "is_available", return_value=True),
        ):
            service = MailServiceFactory.create_mail_service()
            assert isinstance(service, MailpitMailService)

    def test_start_mailpit_invalid_port_numbers(self) -> None:
        """Test start_mailpit with invalid port numbers."""
        with (
            patch.dict(
                "os.environ", {"MAILPIT_PORT": "invalid", "MAILPIT_WEB_PORT": "8025"}
            ),
            patch("os.path.exists", return_value=True),
            patch("builtins.print") as mock_print,
            patch.object(MailServiceFactory, "_create_mailpit_service") as mock_create,
        ):
            # Mock the service creation to avoid the int() error in _create_mailpit_service
            mock_service = Mock()
            mock_service.is_available.return_value = False
            mock_create.return_value = mock_service

            result = MailServiceFactory.start_mailpit()
            assert result is False
            mock_print.assert_any_call(
                "❌ Invalid port numbers in environment variables"
            )

    def test_start_mailpit_web_port_invalid(self) -> None:
        """Test start_mailpit with invalid web port number."""
        with (
            patch.dict(
                "os.environ", {"MAILPIT_PORT": "1025", "MAILPIT_WEB_PORT": "invalid"}
            ),
            patch("os.path.exists", return_value=True),
            patch("builtins.print") as mock_print,
            patch.object(MailServiceFactory, "_create_mailpit_service") as mock_create,
        ):
            # Mock the service creation to avoid the int() error in _create_mailpit_service
            mock_service = Mock()
            mock_service.is_available.return_value = False
            mock_create.return_value = mock_service

            result = MailServiceFactory.start_mailpit()
            assert result is False
            mock_print.assert_any_call(
                "❌ Invalid port numbers in environment variables"
            )

    def test_start_mailpit_executable_not_found(self) -> None:
        """Test start_mailpit when executable doesn't exist."""
        with patch("os.path.exists", return_value=False):
            result = MailServiceFactory.start_mailpit("./nonexistent/mailpit.exe")
            assert result is False

    def test_start_mailpit_subprocess_fails(self) -> None:
        """Test start_mailpit when subprocess.Popen fails."""
        with (
            patch("os.path.exists", return_value=True),
            patch("subprocess.Popen", side_effect=OSError("Failed to start process")),
            patch.object(MailServiceFactory, "_create_mailpit_service") as mock_create,
        ):
            mock_service = Mock()
            mock_service.is_available.return_value = False
            mock_create.return_value = mock_service

            result = MailServiceFactory.start_mailpit()
            assert result is False

    def test_start_mailpit_with_custom_ports(self) -> None:
        """Test start_mailpit with custom port configuration."""
        with (
            patch.dict(
                "os.environ", {"MAILPIT_PORT": "2525", "MAILPIT_WEB_PORT": "9025"}
            ),
            patch("os.path.exists", return_value=True),
            patch("subprocess.Popen") as mock_popen,
            patch.object(MailServiceFactory, "_create_mailpit_service") as mock_create,
            patch("builtins.print"),
            patch("time.sleep"),
        ):
            # Mock service to be unavailable first (to trigger startup), then available
            mock_service = Mock()
            mock_service.is_available.side_effect = [False, True]
            mock_service.get_status.return_value = {
                "host": "localhost",
                "smtp_port": 2525,
                "web_ui": "http://localhost:9025",
            }
            mock_create.return_value = mock_service

            result = MailServiceFactory.start_mailpit()
            assert result is True

            # Verify the command includes custom ports
            call_args = mock_popen.call_args[0][0]
            assert "--smtp" in call_args
            assert "localhost:2525" in call_args
            assert "--listen" in call_args
            assert "localhost:9025" in call_args

    def test_start_mailpit_already_running(self) -> None:
        """Test start_mailpit when Mailpit is already running."""
        with (
            patch("os.path.exists", return_value=True),
            patch.object(MailServiceFactory, "_create_mailpit_service") as mock_create,
        ):
            mock_service = Mock()
            mock_service.is_available.return_value = True
            mock_create.return_value = mock_service

            result = MailServiceFactory.start_mailpit()
            assert result is True

    def test_factory_print_statements_in_start_mailpit(self) -> None:
        """Test the print statements in start_mailpit method."""
        with (
            patch("os.path.exists", return_value=True),
            patch("subprocess.Popen"),
            patch.object(MailServiceFactory, "_create_mailpit_service") as mock_create,
            patch("time.sleep"),
            patch("builtins.print") as mock_print,
        ):
            # Mock service that will fail after startup
            mock_service = Mock()
            mock_service.is_available.side_effect = [
                False,
                False,
            ]  # Never becomes available
            mock_create.return_value = mock_service

            result = MailServiceFactory.start_mailpit()
            assert result is False

            # Check that the "failed to start" message was printed (lines 230-231)
            mock_print.assert_any_call("❌ Mailpit failed to start")

    def test_factory_exception_handling_in_start_mailpit(self) -> None:
        """Test exception handling in start_mailpit."""
        with (
            patch("os.path.exists", return_value=True),
            patch("subprocess.Popen", side_effect=FileNotFoundError("File not found")),
            patch.object(MailServiceFactory, "_create_mailpit_service") as mock_create,
            patch("builtins.print") as mock_print,
        ):
            mock_service = Mock()
            mock_service.is_available.return_value = False
            mock_create.return_value = mock_service

            result = MailServiceFactory.start_mailpit()
            assert result is False

            # Check that the exception message was printed
            mock_print.assert_any_call("❌ Failed to start Mailpit: File not found")

    def test_get_available_services_coverage(self) -> None:
        """Test get_available_services method coverage."""
        services = MailServiceFactory.get_available_services()

        # Verify the returned structure
        assert isinstance(services, dict)
        assert "mailpit" in services
        assert "smtp" in services

    def test_factory_with_different_environments(self) -> None:
        """Test factory behavior in different environment configurations."""
        test_cases = [
            ({"FLASK_ENV": "production"}, SMTPMailService),
            ({}, SMTPMailService),  # Default case
        ]

        for env_vars, expected_type in test_cases:
            with patch.dict("os.environ", env_vars, clear=True):
                with patch.object(
                    MailpitMailService, "is_available", return_value=False
                ):
                    service = MailServiceFactory.create_mail_service()
                    assert isinstance(service, expected_type)

    def test_factory_get_service_method(self) -> None:
        """Test the instance method get_service."""
        factory = MailServiceFactory()

        with patch.object(MailServiceFactory, "create_mail_service") as mock_create:
            mock_service = Mock()
            mock_create.return_value = mock_service

            result = factory.get_service(force_type="mailpit")

            mock_create.assert_called_once_with(app=None, force_type="mailpit")
            assert result == mock_service


if __name__ == "__main__":
    pytest.main([__file__])
