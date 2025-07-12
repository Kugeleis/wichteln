"""Tests for forms.py - Pydantic validation models."""

import pytest
from pydantic import ValidationError

from src.wichteln.forms import (
    ParticipantForm,
    AssignmentConfirmForm,
    validate_form_data,
)


class TestParticipantForm:
    """Tests for ParticipantForm validation."""

    def test_valid_participant_creation(self) -> None:
        """Test creating participant with valid data."""
        form = ParticipantForm(
            name="John Doe", email="john@example.com", recaptcha_token="valid_token"
        )

        assert form.name == "John Doe"
        assert form.email == "john@example.com"
        assert form.recaptcha_token == "valid_token"

    def test_participant_without_recaptcha_token(self) -> None:
        """Test creating participant without recaptcha token."""
        form = ParticipantForm(name="Jane Smith", email="jane@example.com")

        assert form.name == "Jane Smith"
        assert form.email == "jane@example.com"
        assert form.recaptcha_token is None

    def test_name_validation_removes_extra_whitespace(self) -> None:
        """Test that name validation removes extra whitespace."""
        form = ParticipantForm(name="  John    Doe  ", email="john@example.com")

        assert form.name == "John Doe"

    def test_name_validation_allows_valid_characters(self) -> None:
        """Test that name validation allows letters, numbers, spaces, hyphens, apostrophes."""
        form = ParticipantForm(name="Mary-Jane O'Connor 123", email="mary@example.com")

        assert form.name == "Mary-Jane O'Connor 123"

    def test_name_validation_rejects_invalid_characters(self) -> None:
        """Test that name validation rejects invalid characters."""
        with pytest.raises(ValidationError) as exc_info:
            ParticipantForm(name="John@Doe", email="john@example.com")

        assert "can only contain letters" in str(exc_info.value)

    def test_name_validation_rejects_too_short_name(self) -> None:
        """Test that name validation rejects names that are too short after cleaning."""
        with pytest.raises(ValidationError) as exc_info:
            ParticipantForm(name="J", email="john@example.com")

        assert "at least 2 characters" in str(exc_info.value)

    def test_email_validation_blocks_disposable_domains(self) -> None:
        """Test that email validation blocks disposable email domains."""
        with pytest.raises(ValidationError) as exc_info:
            ParticipantForm(name="John Doe", email="test@10minutemail.com")

        assert "Disposable email addresses are not allowed" in str(exc_info.value)

    def test_email_validation_allows_normal_domains(self) -> None:
        """Test that email validation allows normal domains."""
        form = ParticipantForm(name="John Doe", email="john@gmail.com")

        assert str(form.email) == "john@gmail.com"

    def test_participant_form_name_invalid_characters(self) -> None:
        """Test that names with invalid characters are rejected."""
        invalid_names = [
            "John@Doe",  # Contains @
            "Jane#Smith",  # Contains #
            "Bob$",  # Contains $
            "Alice%Jones",  # Contains %
            "Mike&Sarah",  # Contains &
            "Test*Name",  # Contains *
            "Name+Plus",  # Contains +
            "Equal=Sign",  # Contains =
            "Question?Mark",  # Contains ?
        ]

        for invalid_name in invalid_names:
            with pytest.raises(ValidationError) as exc_info:
                ParticipantForm(name=invalid_name, email="test@example.com")

            errors = exc_info.value.errors()
            assert len(errors) == 1
            assert errors[0]["loc"] == ("name",)
            assert (
                "can only contain letters, numbers, spaces, hyphens, and apostrophes"
                in errors[0]["msg"]
            )

    def test_participant_form_name_too_short_after_cleaning(self) -> None:
        """Test that names too short after cleaning are rejected."""
        short_names = [
            "  a  ",  # Only 1 character after stripping/cleaning
            "x",  # Single character
        ]

        for short_name in short_names:
            with pytest.raises(ValidationError) as exc_info:
                ParticipantForm(name=short_name, email="test@example.com")

            errors = exc_info.value.errors()
            assert len(errors) == 1
            assert errors[0]["loc"] == ("name",)
            assert "at least 2 characters" in errors[0]["msg"]


class TestAssignmentConfirmForm:
    """Tests for AssignmentConfirmForm validation."""

    def test_valid_uuid_token(self) -> None:
        """Test that valid UUID token is accepted."""
        form = AssignmentConfirmForm(token="550e8400-e29b-41d4-a716-446655440000")

        assert form.token == "550e8400-e29b-41d4-a716-446655440000"

    def test_invalid_token_format(self) -> None:
        """Test that invalid token format is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            AssignmentConfirmForm(token="invalid-token")

        # Check that the error is about string length (too short for UUID)
        assert "should have at least 36 characters" in str(exc_info.value)

    def test_token_too_short(self) -> None:
        """Test that token that's too short is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            AssignmentConfirmForm(token="short")

        errors = exc_info.value.errors()
        assert any("at least 36 characters" in str(error["msg"]) for error in errors)

    def test_token_too_long(self) -> None:
        """Test that token that's too long is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            AssignmentConfirmForm(token="550e8400-e29b-41d4-a716-446655440000-extra")

        errors = exc_info.value.errors()
        assert any("at most 36 characters" in str(error["msg"]) for error in errors)


class TestValidateFormData:
    """Tests for validate_form_data utility function."""

    def test_successful_validation(self) -> None:
        """Test successful form validation."""
        form_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "recaptcha_token": "valid_token",
        }

        validated_data, errors = validate_form_data(ParticipantForm, form_data)

        assert validated_data is not None
        assert isinstance(validated_data, ParticipantForm)
        assert errors == []
        assert validated_data.name == "John Doe"

    def test_validation_with_errors(self) -> None:
        """Test form validation with errors."""
        form_data = {
            "name": "",  # Too short
            "email": "invalid-email",  # Invalid format
        }

        validated_data, errors = validate_form_data(ParticipantForm, form_data)

        assert validated_data is None
        assert len(errors) > 0
        assert any("Name:" in error for error in errors)
        assert any("Email:" in error for error in errors)

    def test_validation_missing_required_fields(self) -> None:
        """Test validation with missing required fields."""
        form_data: dict[str, str] = {}  # Missing all required fields

        validated_data, errors = validate_form_data(ParticipantForm, form_data)

        assert validated_data is None
        assert len(errors) > 0

    def test_validation_with_assignment_form(self) -> None:
        """Test validation with AssignmentConfirmForm."""
        form_data = {"token": "550e8400-e29b-41d4-a716-446655440000"}

        validated_data, errors = validate_form_data(AssignmentConfirmForm, form_data)

        assert validated_data is not None
        assert isinstance(validated_data, AssignmentConfirmForm)
        assert errors == []
        assert validated_data.token == "550e8400-e29b-41d4-a716-446655440000"

    def test_validation_error_message_formatting(self) -> None:
        """Test that validation error messages are properly formatted."""
        form_data = {
            "name": "J",  # Too short
            "email": "john@example.com",
        }

        validated_data, errors = validate_form_data(ParticipantForm, form_data)

        assert validated_data is None
        assert len(errors) == 1
        assert errors[0].startswith("Name:")
        assert "at least 2 characters" in errors[0]
