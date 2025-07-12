"""
Email service functionality for the Secret Santa application.

Refactored to use single responsibility functions for better maintainability.
"""

from src.mail_service import EmailMessage
from services.validators import MailServiceValidator
from services.email_templates import EmailTemplateService


class EmailService:
    """Handles email operations using single responsibility functions."""

    def __init__(self, mail_service):
        """Initialize with a mail service instance and template service."""
        self.mail_service = mail_service
        self.template_service = EmailTemplateService()

    def send_email(self, recipient_email: str, subject: str, body: str) -> bool:
        """
        Sends an email using single responsibility validation and creation functions.

        Args:
            recipient_email: The email address of the recipient.
            subject: The subject of the email.
            body: The body content of the email.

        Returns:
            True if the email was sent successfully, False otherwise.
        """
        try:
            # Validate recipient using single responsibility function
            is_valid, error_msg = MailServiceValidator.validate_email_recipient(
                recipient_email
            )
            if not is_valid:
                print(f"Invalid email recipient: {error_msg}")
                return False

            # Create email message using single responsibility pattern
            message = EmailMessage(
                recipient=recipient_email, subject=subject, body=body
            )
            return self.mail_service.send_email(message)
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_confirmation_email(
        self, creator_email: str, confirmation_link: str
    ) -> bool:
        """Send confirmation email using single responsibility template function."""
        # Use template service for content generation (single responsibility)
        subject, body = self.template_service.create_confirmation_email_content(
            confirmation_link
        )
        return self.send_email(creator_email, subject, body)

    def send_assignment_email(
        self, giver_email: str, giver_name: str, receiver_name: str
    ) -> bool:
        """Send assignment email using single responsibility template function."""
        # Use template service for content generation (single responsibility)
        subject, body = self.template_service.create_assignment_email_content(
            giver_name, receiver_name
        )
        return self.send_email(giver_email, subject, body)

    def send_test_email(self) -> tuple[bool, str]:
        """Send a test email using single responsibility functions."""
        # Get service status
        status = self.mail_service.get_status()

        # Validate development mode access using single responsibility function
        is_allowed, error_msg = MailServiceValidator.validate_development_mode_access(
            status
        )
        if not is_allowed:
            return False, error_msg

        # Create test email content using single responsibility function
        subject, body = self.template_service.create_test_email_content(status)

        # Send test email
        success = self.send_email("test@example.com", subject, body)

        # Generate response using single responsibility function
        response = self.template_service.create_test_email_response(success, subject)

        return success, response


class EmailBatchProcessor:
    """Utility for processing multiple emails efficiently with single responsibility pattern."""

    def __init__(self, email_service: EmailService):
        """Initialize with email service."""
        self.email_service = email_service

    def send_assignment_batch(
        self, assignments: dict[str, str], participant_emails: dict[str, str]
    ) -> tuple[int, int, list[str]]:
        """Send assignment emails to all participants efficiently.

        Single responsibility: Batch email processing only.

        Args:
            assignments: Dictionary mapping giver names to receiver names
            participant_emails: Dictionary mapping names to email addresses

        Returns:
            Tuple of (successful_sends, total_attempts, failed_participants)
        """
        successful = 0
        total = 0
        failed_participants = []

        for giver, receiver in assignments.items():
            giver_email = participant_emails.get(giver)
            if giver_email:
                total += 1
                if self.email_service.send_assignment_email(
                    str(giver_email), giver, receiver
                ):
                    successful += 1
                else:
                    failed_participants.append(giver)

        return successful, total, failed_participants
