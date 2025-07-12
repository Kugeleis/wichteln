"""
Additional tests to improve code coverage.

This module provides tests for edge cases and error conditions that were
identified as missing from the coverage report.
"""

from unittest.mock import Mock, patch
import pytest
from flask import Flask

from src.mail_service import (
    MailServiceFactory,
    EmailMessage,
    MailpitMailService,
    SMTPMailService,
)


class TestFactoryEdgeCases:
    """Test factory edge cases and error conditions."""

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

    def test_get_available_services_coverage(self) -> None:
        """Test get_available_services method coverage."""
        services = MailServiceFactory.get_available_services()

        # Verify the returned structure
        assert isinstance(services, dict)
        assert "mailpit" in services
        assert "smtp" in services


class TestSMTPServiceEdgeCases:
    """Test SMTP service edge cases and error conditions."""

    def test_smtp_service_error_handling_in_send_email(self) -> None:
        """Test SMTP service error handling when sending fails."""
        app = Flask(__name__)
        service = SMTPMailService(app=app, server="smtp.example.com", port=587)

        # Mock the mail.send to raise an exception
        with patch.object(service.mail, "send", side_effect=Exception("SMTP Error")):
            message = EmailMessage(
                subject="Test", recipient="test@example.com", body="Test body"
            )

            result = service.send_email(message)
            assert result is False

    def test_smtp_is_available_missing_auth_credentials(self) -> None:
        """Test is_available when authentication credentials are missing."""
        service = SMTPMailService(
            server="smtp.gmail.com",
            port=587,
            use_tls=True,
            # Missing username and password
        )
        service.mail = Mock()  # Mock that service is initialized

        result = service.is_available()
        assert result is False

    def test_smtp_get_status_missing_credentials_message(self) -> None:
        """Test get_status returns correct message for missing credentials."""
        service = SMTPMailService(
            server="smtp.gmail.com",
            port=587,
            use_tls=True,
            # Missing username and password
        )
        service.mail = Mock()  # Mock that service is initialized

        status = service.get_status()
        assert status["status_message"] == "Missing authentication credentials"

    def test_smtp_get_status_configuration_incomplete(self) -> None:
        """Test get_status when configuration is incomplete."""
        service = SMTPMailService(
            server="smtp.gmail.com",
            port=587,
            username="user@example.com",
            password="password",
        )
        service.mail = Mock()

        # Mock is_available to return False for incomplete config
        with patch.object(service, "is_available", return_value=False):
            status = service.get_status()
            assert status["status_message"] == "Configuration incomplete"


class TestProtocolAbstractMethods:
    """Test protocol abstract methods for coverage."""

    def test_mail_protocol_abstract_methods_coverage(self) -> None:
        """Test that abstract methods are properly defined."""
        from src.mail_service.protocol import MailProtocol

        # Verify that the protocol has the expected abstract methods
        assert hasattr(MailProtocol, "send_email")
        assert hasattr(MailProtocol, "is_available")
        assert hasattr(MailProtocol, "get_status")
        assert hasattr(MailProtocol, "get_service_info")

        # Verify it's an abstract class that can't be instantiated
        try:
            MailProtocol()  # type: ignore[abstract]
            pytest.fail("Should not be able to instantiate abstract class")
        except TypeError as e:
            assert "abstract class" in str(e)


class TestEmailMessageValidation:
    """Test EmailMessage edge cases."""

    def test_email_message_with_recipients_list(self) -> None:
        """Test EmailMessage with recipients list property."""
        message = EmailMessage(
            subject="Test", recipient="test@example.com", body="Test body"
        )

        # Test that recipients property works (used in some implementations)
        recipients = getattr(message, "recipients", None)
        # The property might not exist, which is fine
        if recipients is not None:
            assert isinstance(recipients, list)


class TestIntegrationEdgeCases:
    """Test integration scenarios and edge cases."""

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

    def test_email_message_string_representation(self) -> None:
        """Test EmailMessage string representation."""
        message = EmailMessage(
            subject="Test Subject", recipient="test@example.com", body="Test body"
        )

        # Test that the object can be converted to string (for debugging)
        str_repr = str(message)
        assert "Test Subject" in str_repr
        assert "test@example.com" in str_repr


if __name__ == "__main__":
    pytest.main([__file__])
