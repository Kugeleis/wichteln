"""
reCAPTCHA verification service for the Secret Santa application.
"""

import requests
from flask import Flask


class RecaptchaService:
    """Handles reCAPTCHA verification for the Secret Santa application."""

    def __init__(self, app: Flask):
        """Initialize with Flask app to access configuration."""
        self.app = app

    def verify_recaptcha(self, token: str | None) -> bool:
        """
        Verifies the reCAPTCHA token with Google's reCAPTCHA service.

        Args:
            token (str | None): The reCAPTCHA token received from the frontend.

        Returns:
            bool: True if the reCAPTCHA verification is successful and the score is above the threshold, False otherwise.
        """
        if not token:
            return False

        if self.app.config["RECAPTCHA_SECRET_KEY"] == "YOUR_RECAPTCHA_SECRET_KEY":
            print(
                "WARNING: reCAPTCHA secret key not configured. Skipping verification."
            )
            return True  # Skip verification if key is not set

        payload = {"secret": self.app.config["RECAPTCHA_SECRET_KEY"], "response": token}
        try:
            response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data=payload,
                timeout=10,
            )
            result = response.json()
            return (
                result.get("success", False) and result.get("score", 0) > 0.5
            )  # Adjust score threshold as needed
        except Exception as e:
            print(f"Error verifying reCAPTCHA: {e}")
            return False
