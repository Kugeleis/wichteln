"""
Request handling utilities for the Secret Santa application.

This module provides common utilities for processing form requests,
handling validation, and managing flash messages.
"""

from flask import request, flash, redirect, url_for
from werkzeug.wrappers import Response
from typing import Any, Callable, TypeVar, Generic
from pydantic import BaseModel
from src.wichteln.forms import validate_form_data


T = TypeVar("T", bound=BaseModel)


class RequestProcessor(Generic[T]):
    """Generic request processor for handling form submissions with validation."""

    def __init__(self, form_class: type[T], redirect_endpoint: str = "main.index"):
        """Initialize the request processor.

        Args:
            form_class: The Pydantic form model class to use for validation
            redirect_endpoint: The endpoint to redirect to after processing
        """
        self.form_class = form_class
        self.redirect_endpoint = redirect_endpoint

    def extract_form_data(self, field_mapping: dict[str, str]) -> dict[str, Any]:
        """Extract form data based on field mapping.

        Args:
            field_mapping: Mapping of form field names to request form keys

        Returns:
            Dictionary of extracted form data
        """
        return {
            field: request.form.get(key, "").strip()
            if isinstance(request.form.get(key), str)
            else request.form.get(key, "")
            for field, key in field_mapping.items()
        }

    def validate_form(self, form_data: dict[str, Any]) -> tuple[T | None, list[str]]:
        """Validate form data using the configured form class.

        Args:
            form_data: The form data to validate

        Returns:
            Tuple of (validated_form_instance, validation_errors)
        """
        validated_form, errors = validate_form_data(self.form_class, form_data)
        # Type cast is safe here since form_class is bound to BaseModel
        return validated_form, errors  # type: ignore

    def handle_validation_errors(self, errors: list[str]) -> Response:
        """Handle validation errors by flashing messages and redirecting.

        Args:
            errors: List of validation error messages

        Returns:
            Redirect response
        """
        flash(f"Invalid input: {'; '.join(errors)}", "error")
        return redirect(url_for(self.redirect_endpoint))

    def handle_success(self, message: str) -> Response:
        """Handle successful operations.

        Args:
            message: Success message to display

        Returns:
            Redirect response
        """
        flash(message, "success")
        return redirect(url_for(self.redirect_endpoint))

    def handle_error(self, message: str) -> Response:
        """Handle error cases.

        Args:
            message: Error message to display

        Returns:
            Redirect response
        """
        flash(message, "error")
        return redirect(url_for(self.redirect_endpoint))

    def handle_exception(self, exception: Exception, context: str = "") -> Response:
        """Handle unexpected exceptions.

        Args:
            exception: The exception that occurred
            context: Context information for debugging

        Returns:
            Redirect response
        """
        flash("An unexpected error occurred. Please try again.", "error")
        print(f"Error in {context}: {exception}")
        return redirect(url_for(self.redirect_endpoint))


def process_form_request(
    form_class: type[T],
    field_mapping: dict[str, str],
    business_logic: Callable[[T], tuple[bool, str]],
    redirect_endpoint: str = "main.index",
    debug_context: str = "",
) -> Response:
    """Generic form request processor.

    Args:
        form_class: The Pydantic form model class
        field_mapping: Mapping of form fields to request form keys
        business_logic: Function that takes validated form and returns (success, message)
        redirect_endpoint: Endpoint to redirect to
        debug_context: Context for debug logging

    Returns:
        Response object
    """
    processor = RequestProcessor(form_class, redirect_endpoint)

    try:
        # Extract and validate form data
        form_data = processor.extract_form_data(field_mapping)
        validated_form, validation_errors = processor.validate_form(form_data)

        if validation_errors:
            return processor.handle_validation_errors(validation_errors)

        if validated_form is None:
            return processor.handle_error(
                "An unexpected error occurred. Please try again."
            )

        # Execute business logic
        success, message = business_logic(validated_form)

        if success:
            if debug_context:
                print(f"DEBUG: {debug_context} - {message}")
            return processor.handle_success(message)
        else:
            return processor.handle_error(message)

    except Exception as e:
        return processor.handle_exception(e, debug_context)
