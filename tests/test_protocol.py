"""
Tests for src/mail_service/protocol.py.

This module provides comprehensive tests for the EmailMessage dataclass
and MailProtocol abstract class.
"""

import pytest
from abc import ABC

from src.mail_service.protocol import EmailMessage, MailProtocol


class TestEmailMessage:
    """Test EmailMessage dataclass."""

    def test_email_message_creation_with_required_fields(self) -> None:
        """Test EmailMessage creation with required fields only."""
        email = EmailMessage(
            recipient="test@example.com", subject="Test Subject", body="Test Body"
        )

        assert email.recipient == "test@example.com"
        assert email.subject == "Test Subject"
        assert email.body == "Test Body"
        assert email.sender is None
        assert email.html_body is None

    def test_email_message_creation_with_all_fields(self) -> None:
        """Test EmailMessage creation with all fields."""
        email = EmailMessage(
            recipient="test@example.com",
            subject="Test Subject",
            body="Test Body",
            sender="sender@example.com",
            html_body="<h1>Test HTML Body</h1>",
        )

        assert email.recipient == "test@example.com"
        assert email.subject == "Test Subject"
        assert email.body == "Test Body"
        assert email.sender == "sender@example.com"
        assert email.html_body == "<h1>Test HTML Body</h1>"

    def test_email_message_dataclass_behavior(self) -> None:
        """Test that EmailMessage behaves as a dataclass."""
        email1 = EmailMessage(
            recipient="test@example.com", subject="Test Subject", body="Test Body"
        )

        email2 = EmailMessage(
            recipient="test@example.com", subject="Test Subject", body="Test Body"
        )

        # Test equality (dataclass behavior)
        assert email1 == email2

    def test_email_message_inequality(self) -> None:
        """Test EmailMessage inequality."""
        email1 = EmailMessage(
            recipient="test1@example.com", subject="Test Subject", body="Test Body"
        )

        email2 = EmailMessage(
            recipient="test2@example.com", subject="Test Subject", body="Test Body"
        )

        assert email1 != email2

    def test_email_message_repr(self) -> None:
        """Test EmailMessage string representation."""
        email = EmailMessage(
            recipient="test@example.com", subject="Test Subject", body="Test Body"
        )

        repr_str = repr(email)
        assert "EmailMessage" in repr_str
        assert "test@example.com" in repr_str
        assert "Test Subject" in repr_str

    def test_email_message_with_empty_strings(self) -> None:
        """Test EmailMessage with empty strings."""
        email = EmailMessage(recipient="", subject="", body="")

        assert email.recipient == ""
        assert email.subject == ""
        assert email.body == ""

    def test_email_message_with_unicode_content(self) -> None:
        """Test EmailMessage with Unicode content."""
        email = EmailMessage(
            recipient="test@example.com",
            subject="Тест Subject 🎄",
            body="Test Body with émojis 🎅",
            html_body="<h1>HTML with émojis 🎁</h1>",
        )

        assert email.subject == "Тест Subject 🎄"
        assert email.body == "Test Body with émojis 🎅"
        assert email.html_body == "<h1>HTML with émojis 🎁</h1>"

    def test_email_message_field_types(self) -> None:
        """Test EmailMessage field type annotations."""
        # Test that fields have correct types
        email = EmailMessage(
            recipient="test@example.com",
            subject="Test Subject",
            body="Test Body",
            sender="sender@example.com",
            html_body="<h1>HTML</h1>",
        )

        assert isinstance(email.recipient, str)
        assert isinstance(email.subject, str)
        assert isinstance(email.body, str)
        assert isinstance(email.sender, str) or email.sender is None
        assert isinstance(email.html_body, str) or email.html_body is None


class TestMailProtocol:
    """Test MailProtocol abstract class."""

    def test_mail_protocol_is_abstract(self) -> None:
        """Test that MailProtocol is an abstract class."""
        assert issubclass(MailProtocol, ABC)

    def test_mail_protocol_cannot_be_instantiated(self) -> None:
        """Test that MailProtocol cannot be instantiated directly."""
        with pytest.raises(TypeError):
            MailProtocol()  # type: ignore

    def test_mail_protocol_abstract_methods(self) -> None:
        """Test that MailProtocol has required abstract methods."""
        # Check that the abstract methods exist
        abstract_methods = MailProtocol.__abstractmethods__

        expected_methods = {
            "send_email",
            "is_available",
            "get_status",
            "get_service_info",
        }

        assert expected_methods.issubset(abstract_methods)

    def test_mail_protocol_implementation_requirements(self) -> None:
        """Test that implementing MailProtocol requires all abstract methods."""

        # Incomplete implementation (missing methods)
        class IncompleteMailService(MailProtocol):
            def send_email(self, message: EmailMessage) -> bool:
                return True

            # Missing is_available, get_status, and get_service_info

        # Should not be able to instantiate incomplete implementation
        with pytest.raises(TypeError):
            IncompleteMailService()  # type: ignore

    def test_mail_protocol_complete_implementation(self) -> None:
        """Test that complete MailProtocol implementation can be instantiated."""

        class CompleteMailService(MailProtocol):
            def send_email(self, message: EmailMessage) -> bool:
                return True

            def is_available(self) -> bool:
                return True

            def get_status(self) -> dict[str, object]:
                return {"status": "ok"}

            def get_service_info(self) -> dict[str, object]:
                return {"name": "Test Service"}

        # Should be able to instantiate complete implementation
        service = CompleteMailService()
        assert isinstance(service, MailProtocol)
        assert (
            service.send_email(EmailMessage("test@example.com", "subject", "body"))
            is True
        )
        assert service.is_available() is True
        assert service.get_status() == {"status": "ok"}

    def test_mail_protocol_method_signatures(self) -> None:
        """Test that MailProtocol defines correct method signatures."""

        class TestMailService(MailProtocol):
            def send_email(self, message: EmailMessage) -> bool:
                return True

            def is_available(self) -> bool:
                return True

            def get_status(self) -> dict[str, object]:
                return {}

            def get_service_info(self) -> dict[str, object]:
                return {"name": "Test"}

        service = TestMailService()

        # Test method signatures
        email = EmailMessage(
            "test@example.com", "subject", "body"
        )  # send_email should accept EmailMessage and return bool
        send_result = service.send_email(email)
        assert isinstance(send_result, bool)

        # is_available should return bool
        available_result = service.is_available()
        assert isinstance(available_result, bool)

        # get_status should return dict
        status_result = service.get_status()
        assert isinstance(status_result, dict)


if __name__ == "__main__":
    pytest.main([__file__])
