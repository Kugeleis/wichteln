"""
Pydantic models for form validation in the Secret Santa application.
"""

from pydantic import BaseModel, EmailStr, field_validator, ValidationError, Field
from typing import Optional
import re
import uuid


class ParticipantForm(BaseModel):
    """Form model for adding participants to the Secret Santa game."""

    name: str = Field(..., min_length=2, max_length=50, description="Participant name")
    email: EmailStr = Field(..., description="Valid email address")
    recaptcha_token: Optional[str] = Field(default=None, description="reCAPTCHA token")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and sanitize participant name."""
        v = v.strip()

        # Remove extra whitespace
        v = re.sub(r"\s+", " ", v)

        # Check for valid characters (letters, numbers, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z0-9\s\-']+$", v):
            raise ValueError(
                "Name can only contain letters, numbers, spaces, hyphens, and apostrophes"
            )

        # Check for reasonable length after cleaning
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters long")

        return v

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v: EmailStr) -> EmailStr:
        """Validate email address and domain."""
        email_str = str(v).strip().lower()

        # Block common disposable email domains if needed
        blocked_domains = ["10minutemail.com", "tempmail.org", "guerrillamail.com"]
        domain = email_str.split("@")[1]

        if domain in blocked_domains:
            raise ValueError("Disposable email addresses are not allowed")

        return v


class AssignmentConfirmForm(BaseModel):
    """Form model for confirming Secret Santa assignments."""

    token: str = Field(
        ..., min_length=36, max_length=36, description="Confirmation token"
    )

    @field_validator("token")
    @classmethod
    def validate_token_format(cls, v: str) -> str:
        """Validate UUID token format."""
        try:
            uuid.UUID(v)
            return v
        except ValueError:
            raise ValueError("Invalid token format")


class ParticipantRemoveForm(BaseModel):
    """Form model for removing participants from the Secret Santa game."""

    name: str = Field(
        ..., min_length=1, max_length=50, description="Participant name to remove"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and sanitize participant name for removal."""
        v = v.strip()

        # Remove extra whitespace
        v = re.sub(r"\s+", " ", v)

        # Check for reasonable length after cleaning
        if len(v) < 1:
            raise ValueError("Name cannot be empty")

        # Check for valid characters (letters, numbers, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z0-9\s\-']+$", v):
            raise ValueError(
                "Name can only contain letters, numbers, spaces, hyphens, and apostrophes"
            )

        return v


def validate_form_data(
    form_class: type[BaseModel], form_data: dict
) -> tuple[Optional[BaseModel], list[str]]:
    """
    Validate form data using a Pydantic model.

    Args:
        form_class: The Pydantic model class to use for validation
        form_data: Dictionary of form data to validate

    Returns:
        Tuple of (validated_data, error_messages)
        If validation succeeds: (model_instance, [])
        If validation fails: (None, [error_messages])
    """
    try:
        validated_data = form_class(**form_data)
        return validated_data, []
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            field = str(error["loc"][0]) if error["loc"] else "form"
            message = error["msg"]
            error_messages.append(f"{field.title()}: {message}")
        return None, error_messages
