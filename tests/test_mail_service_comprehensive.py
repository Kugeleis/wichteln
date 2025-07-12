"""Comprehensive tests for mail service functionality."""

import pytest
from unittest.mock import Mock, patch

from src.mail_service import (
    MailServiceFactory,
    EmailMessage,
    MailpitMailService,
    SMTPMailService,
)
from src.mail_service.protocol import MailProtocol


class TestEmailMessage:
    """Tests for EmailMessage dataclass."""

    def test_email_message_creation_with_required_fields(self) -> None:
        """Test that EmailMessage can be created with required fields."""
        message = EmailMessage(
            subject="Test Subject",
            recipient="test@example.com",
            body="Test body content",
        )

        assert message.subject == "Test Subject"
        assert message.recipient == "test@example.com"
        assert message.body == "Test body content"
        assert message.sender is None
        assert message.html_body is None

    def test_email_message_creation_with_all_fields(self) -> None:
        """Test that EmailMessage can be created with all fields."""
        message = EmailMessage(
            subject="Test Subject",
            recipient="test@example.com",
            body="Test body content",
            sender="sender@example.com",
            html_body="<h1>Test HTML</h1>",
        )

        assert message.subject == "Test Subject"
        assert message.recipient == "test@example.com"
        assert message.body == "Test body content"
        assert message.sender == "sender@example.com"
        assert message.html_body == "<h1>Test HTML</h1>"

    @pytest.mark.parametrize(
        "field_name,field_value",
        [
            ("subject", ""),
            ("recipient", ""),
            ("body", ""),
        ],
    )
    def test_email_message_with_empty_required_fields(
        self, field_name: str, field_value: str
    ) -> None:
        """Test that EmailMessage accepts empty strings for required fields."""
        kwargs = {
            "subject": "Test Subject",
            "recipient": "test@example.com",
            "body": "Test body",
        }
        kwargs[field_name] = field_value

        message = EmailMessage(**kwargs)
        assert getattr(message, field_name) == field_value


class TestMailpitMailService:
    """Tests for MailpitMailService class."""

    @pytest.fixture
    def mailpit_service(self) -> MailpitMailService:
        """Create a MailpitMailService instance for testing."""
        return MailpitMailService(
            host="localhost",
            port=2525,
            web_ui_port=9025,
            default_sender="test@localhost",
        )

    @pytest.fixture
    def sample_email(self) -> EmailMessage:
        """Create a sample email message for testing."""
        return EmailMessage(
            subject="Test Email",
            recipient="recipient@example.com",
            body="This is a test email body.",
        )

    def test_mailpit_service_initialization_with_defaults(self) -> None:
        """Test MailpitMailService initialization with default values."""
        service = MailpitMailService()

        assert service.host == "localhost"
        assert service.port == 1025
        assert service.web_ui_port == 8025
        assert service.default_sender == "noreply@localhost"

    def test_mailpit_service_initialization_with_custom_values(self) -> None:
        """Test MailpitMailService initialization with custom values."""
        service = MailpitMailService(
            host="custom-host",
            port=9999,
            web_ui_port=8888,
            default_sender="custom@sender.com",
        )

        assert service.host == "custom-host"
        assert service.port == 9999
        assert service.web_ui_port == 8888
        assert service.default_sender == "custom@sender.com"

    @patch("smtplib.SMTP")
    def test_send_email_with_plain_text_message_succeeds(
        self,
        mock_smtp: Mock,
        mailpit_service: MailpitMailService,
        sample_email: EmailMessage,
    ) -> None:
        """Test sending a plain text email successfully."""
        # Setup mock
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Send email
        result = mailpit_service.send_email(sample_email)

        # Verify result
        assert result is True
        mock_smtp.assert_called_once_with("localhost", 2525)
        mock_server.sendmail.assert_called_once()

        # Verify sendmail arguments
        call_args = mock_server.sendmail.call_args[0]
        assert call_args[0] == "test@localhost"  # sender
        assert call_args[1] == ["recipient@example.com"]  # recipients

    @patch("smtplib.SMTP")
    def test_send_email_with_html_message_succeeds(
        self, mock_smtp: Mock, mailpit_service: MailpitMailService
    ) -> None:
        """Test sending an HTML email successfully."""
        # Setup mock
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Create HTML email
        html_email = EmailMessage(
            subject="HTML Test",
            recipient="test@example.com",
            body="Plain text version",
            html_body="<h1>HTML Version</h1>",
        )

        # Send email
        result = mailpit_service.send_email(html_email)

        # Verify result
        assert result is True
        mock_server.sendmail.assert_called_once()

    @patch("smtplib.SMTP")
    def test_send_email_with_smtp_error_returns_false(
        self,
        mock_smtp: Mock,
        mailpit_service: MailpitMailService,
        sample_email: EmailMessage,
    ) -> None:
        """Test that SMTP errors are handled gracefully."""
        # Setup mock to raise exception
        mock_smtp.side_effect = ConnectionRefusedError("Connection refused")

        # Send email
        result = mailpit_service.send_email(sample_email)

        # Verify failure
        assert result is False

    @patch("socket.create_connection")
    def test_is_available_when_mailpit_running_returns_true(
        self, mock_connection: Mock, mailpit_service: MailpitMailService
    ) -> None:
        """Test is_available returns True when Mailpit is running."""
        # Setup mock for successful connection
        mock_connection.return_value.__enter__.return_value = Mock()

        result = mailpit_service.is_available()

        assert result is True
        mock_connection.assert_called_once_with(("localhost", 2525), timeout=5)

    @patch("socket.create_connection")
    def test_is_available_when_mailpit_not_running_returns_false(
        self, mock_connection: Mock, mailpit_service: MailpitMailService
    ) -> None:
        """Test is_available returns False when Mailpit is not running."""
        # Setup mock to raise connection error
        mock_connection.side_effect = ConnectionRefusedError("Connection refused")

        result = mailpit_service.is_available()

        assert result is False

    def test_get_status_returns_correct_structure(
        self, mailpit_service: MailpitMailService
    ) -> None:
        """Test that get_status returns properly structured data."""
        with patch.object(mailpit_service, "is_available", return_value=True):
            status = mailpit_service.get_status()

        # Verify required fields
        assert status["service"] == "Mailpit"
        assert status["type"] == "development"
        assert status["available"] is True
        assert status["host"] == "localhost"
        assert status["smtp_port"] == 2525
        assert status["web_ui_port"] == 9025
        assert "web_ui" in status
        assert "status_message" in status

    def test_get_service_info_returns_basic_info(
        self, mailpit_service: MailpitMailService
    ) -> None:
        """Test that get_service_info returns basic service information."""
        info = mailpit_service.get_service_info()

        assert info["name"] == "Mailpit"
        assert info["type"] == "development"
        assert "description" in info
        assert "website" in info


class TestSMTPMailService:
    """Tests for SMTPMailService class."""

    @pytest.fixture
    def mock_flask_app(self) -> Mock:
        """Create a mock Flask application."""
        app = Mock()
        app.config = {}
        app.debug = False
        app.testing = False
        return app

    @pytest.fixture
    def smtp_service(self, mock_flask_app: Mock) -> SMTPMailService:
        """Create an SMTPMailService instance for testing."""
        return SMTPMailService(
            app=mock_flask_app,
            server="smtp.example.com",
            port=587,
            username="test@example.com",
            password="testpassword",
        )

    def test_smtp_service_initialization_without_app(self) -> None:
        """Test SMTPMailService initialization without Flask app."""
        service = SMTPMailService()

        assert service.app is None
        assert service.mail is None
        assert isinstance(service.config, dict)

    def test_smtp_service_configuration_from_environment(self) -> None:
        """Test that SMTP service reads configuration from environment."""
        with patch.dict(
            "os.environ",
            {
                "MAIL_SERVER": "custom.smtp.com",
                "MAIL_PORT": "465",
                "MAIL_USERNAME": "user@custom.com",
            },
        ):
            service = SMTPMailService()

            assert service.config["MAIL_SERVER"] == "custom.smtp.com"
            assert service.config["MAIL_PORT"] == 465
            assert service.config["MAIL_USERNAME"] == "user@custom.com"

    def test_smtp_service_init_app_configures_flask_mail(
        self, mock_flask_app: Mock
    ) -> None:
        """Test that init_app properly configures Flask-Mail."""
        service = SMTPMailService()

        with patch("src.mail_service.smtp.Mail") as mock_mail:
            service.init_app(mock_flask_app)

            # Verify Flask app configuration
            assert mock_flask_app.config["MAIL_SERVER"] == "smtp.gmail.com"
            assert mock_flask_app.config["MAIL_PORT"] == 587

            # Verify Mail instance creation
            mock_mail.assert_called_once_with(mock_flask_app)

    @patch("src.mail_service.smtp.Message")
    def test_send_email_with_configured_service_succeeds(
        self, mock_message: Mock, smtp_service: SMTPMailService
    ) -> None:
        """Test sending email with properly configured SMTP service."""
        # Setup mocks
        mock_mail_instance = Mock()
        smtp_service.mail = mock_mail_instance
        sample_email = EmailMessage(
            subject="Test", recipient="test@example.com", body="Test body"
        )

        # Send email
        result = smtp_service.send_email(sample_email)

        # Verify result
        assert result is True
        mock_message.assert_called_once()
        mock_mail_instance.send.assert_called_once()

    def test_send_email_without_initialized_service_fails(self) -> None:
        """Test that sending email fails when service is not initialized."""
        service = SMTPMailService()
        sample_email = EmailMessage(
            subject="Test", recipient="test@example.com", body="Test body"
        )

        result = service.send_email(sample_email)

        assert result is False

    def test_is_available_with_complete_config_returns_true(
        self, smtp_service: SMTPMailService
    ) -> None:
        """Test is_available returns True with complete configuration."""
        result = smtp_service.is_available()

        assert result is True

    def test_is_available_with_incomplete_config_returns_false(self) -> None:
        """Test is_available returns False with incomplete configuration."""
        service = SMTPMailService()

        result = service.is_available()

        assert result is False


class TestMailServiceFactory:
    """Tests for MailServiceFactory class."""

    @pytest.fixture
    def mock_flask_app(self) -> Mock:
        """Create a mock Flask application."""
        app = Mock()
        app.config = {}
        app.debug = False
        app.testing = False
        return app

    def test_create_mail_service_defaults_to_mailpit_in_development(
        self, mock_flask_app: Mock
    ) -> None:
        """Test that factory creates Mailpit service by default in development."""
        with patch.dict("os.environ", {"FLASK_ENV": "development"}):
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
            mock_service = Mock(spec=MailProtocol)
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
    def test_start_mailpit_with_existing_executable_succeeds(
        self, mock_popen: Mock, mock_exists: Mock
    ) -> None:
        """Test that start_mailpit succeeds when executable exists."""
        # Setup mocks
        mock_exists.return_value = True
        mock_service = Mock()
        mock_service.is_available.side_effect = [
            False,
            True,
        ]  # First check fails, then succeeds after start

        with patch.object(
            MailServiceFactory, "_create_mailpit_service", return_value=mock_service
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


@pytest.mark.integration
class TestMailServiceIntegration:
    """Integration tests for mail service components."""

    def test_factory_creates_working_mailpit_service(self) -> None:
        """Test that factory creates a working Mailpit service."""
        service = MailServiceFactory.create_mail_service(force_type="mailpit")

        assert isinstance(service, MailpitMailService)
        assert hasattr(service, "send_email")
        assert hasattr(service, "is_available")
        assert hasattr(service, "get_status")

    def test_factory_creates_working_smtp_service(self) -> None:
        """Test that factory creates a working SMTP service."""
        service = MailServiceFactory.create_mail_service(force_type="smtp")

        assert isinstance(service, SMTPMailService)
        assert hasattr(service, "send_email")
        assert hasattr(service, "is_available")
        assert hasattr(service, "get_status")

    def test_email_message_works_with_all_services(self) -> None:
        """Test that EmailMessage works consistently across all services."""
        message = EmailMessage(
            subject="Integration Test",
            recipient="test@example.com",
            body="This is a test message.",
        )

        # Test with Mailpit service
        mailpit_service = MailServiceFactory.create_mail_service(force_type="mailpit")
        assert hasattr(mailpit_service, "send_email")

        # Test with SMTP service
        smtp_service = MailServiceFactory.create_mail_service(force_type="smtp")
        assert hasattr(smtp_service, "send_email")

        # Both should accept the same message format
        assert message.subject == "Integration Test"
        assert message.recipient == "test@example.com"
        assert message.body == "This is a test message."


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
