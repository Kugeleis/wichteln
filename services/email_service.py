"""
Email service functionality for the Secret Santa application.
"""

from src.mail_service import EmailMessage


class EmailService:
    """Handles email operations for the Secret Santa application."""

    def __init__(self, mail_service):
        """Initialize with a mail service instance."""
        self.mail_service = mail_service

    def send_email(self, recipient_email: str, subject: str, body: str) -> bool:
        """
        Sends an email to the specified recipient using the configured mail service.

        Args:
            recipient_email (str): The email address of the recipient.
            subject (str): The subject of the email.
            body (str): The body content of the email.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        try:
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
        """Send confirmation email to the game creator."""
        subject = "Confirm Secret Santa Assignments"
        body = f"""Hello,

Please click the following link to confirm and send out the Secret Santa assignments: {confirmation_link}

This link will expire after one use or if the game is reset."""

        return self.send_email(creator_email, subject, body)

    def send_assignment_email(
        self, giver_email: str, giver_name: str, receiver_name: str
    ) -> bool:
        """Send assignment email to a participant."""
        subject = "Your Secret Santa Assignment!"
        body = f"""Hello {giver_name},

You are the Secret Santa for: {receiver_name}!"""

        return self.send_email(giver_email, subject, body)

    def send_test_email(self) -> tuple[bool, str]:
        """Send a test email and return success status and response message."""
        import datetime

        status = self.mail_service.get_status()
        subject = "🎄 Test Email from Wichteln App"
        body = f"""Hello from your Wichteln application!

This is a test email to verify that email integration is working correctly.

Configuration:
- Mail Service: {status["service"]} ({status["type"]})
- Status: {status["status_message"]}
- Timestamp: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

If you can see this email in Mailpit at http://localhost:8025,
your email configuration is working perfectly!

Happy Secret Santa organizing! 🎅
"""

        success = self.send_email("test@example.com", subject, body)

        if success:
            response = f"""
            <h2>✅ Test Email Sent Successfully!</h2>
            <p>Check your emails in Mailpit: <a href="http://localhost:8025" target="_blank">http://localhost:8025</a></p>
            <p>Email sent to: test@example.com</p>
            <p>Subject: {subject}</p>
            <hr>
            <p><a href="/">← Back to Wichteln</a></p>
            """
        else:
            response = """
            <h2>❌ Email Test Failed</h2>
            <p>Could not send test email. Check the console for error details.</p>
            <p>Make sure Mailpit is running on localhost:1025</p>
            <hr>
            <p><a href="/">← Back to Wichteln</a></p>
            """

        return success, response
