"""
Email template utilities for the Secret Santa application.

This module provides utilities for creating email content and templates
for different types of notifications.
"""

import datetime
from typing import Dict, Any


class EmailTemplateService:
    """Service for generating email templates and content."""

    @staticmethod
    def create_confirmation_email_content(confirmation_link: str) -> tuple[str, str]:
        """Create content for Secret Santa assignment confirmation email.

        Args:
            confirmation_link: The URL link for confirming assignments

        Returns:
            Tuple of (subject, body)
        """
        subject = "Confirm Secret Santa Assignments"
        body = f"""Hello,

Please click the following link to confirm and send out the Secret Santa assignments: {confirmation_link}

This link will expire after one use or if the game is reset."""

        return subject, body

    @staticmethod
    def create_assignment_email_content(
        giver_name: str, receiver_name: str
    ) -> tuple[str, str]:
        """Create content for Secret Santa assignment notification email.

        Args:
            giver_name: Name of the person giving the gift
            receiver_name: Name of the person receiving the gift

        Returns:
            Tuple of (subject, body)
        """
        subject = "Your Secret Santa Assignment!"
        body = f"""Hello {giver_name},

You are the Secret Santa for: {receiver_name}!"""

        return subject, body

    @staticmethod
    def create_test_email_content(service_status: Dict[str, Any]) -> tuple[str, str]:
        """Create content for test email.

        Args:
            service_status: Status information from the mail service

        Returns:
            Tuple of (subject, body)
        """
        subject = "🎄 Test Email from Wichteln App"
        body = f"""Hello from your Wichteln application!

This is a test email to verify that email integration is working correctly.

Configuration:
- Mail Service: {service_status["service"]} ({service_status["type"]})
- Status: {service_status["status_message"]}
- Timestamp: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

If you can see this email in Mailpit at http://localhost:8025,
your email configuration is working perfectly!

Happy Secret Santa organizing! 🎅
"""

        return subject, body

    @staticmethod
    def create_test_email_response(success: bool, subject: str) -> str:
        """Create HTML response for test email results.

        Args:
            success: Whether the email was sent successfully
            subject: The subject of the test email

        Returns:
            HTML response content
        """
        if success:
            return f"""
            <h2>✅ Test Email Sent Successfully!</h2>
            <p>Check your emails in Mailpit: <a href="http://localhost:8025" target="_blank">http://localhost:8025</a></p>
            <p>Email sent to: test@example.com</p>
            <p>Subject: {subject}</p>
            <hr>
            <p><a href="/">← Back to Wichteln</a></p>
            """
        else:
            return """
            <h2>❌ Email Test Failed</h2>
            <p>Could not send test email. Check the console for error details.</p>
            <p>Make sure Mailpit is running on localhost:1025</p>
            <hr>
            <p><a href="/">← Back to Wichteln</a></p>
            """


class EmailAddressValidator:
    """Utility class for email address validation and extraction."""

    @staticmethod
    def get_creator_email(
        participants: list[dict[str, Any]], fallback: str = "admin@example.com"
    ) -> str:
        """Get the email address of the game creator (first participant).

        Args:
            participants: List of participant dictionaries
            fallback: Fallback email if no participants exist

        Returns:
            Email address of the creator
        """
        return str(participants[0]["email"]) if participants else fallback

    @staticmethod
    def extract_participant_emails(
        participants: list[dict[str, Any]],
    ) -> dict[str, str]:
        """Extract mapping of participant names to email addresses.

        Args:
            participants: List of participant dictionaries

        Returns:
            Dictionary mapping names to email addresses
        """
        return {
            str(participant["name"]): str(participant["email"])
            for participant in participants
        }
