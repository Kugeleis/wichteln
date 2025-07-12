#!/usr/bin/env python3
"""
Example script demonstrating the mail service module.

This script shows how to use the mail service module in different scenarios.
"""

import sys
from pathlib import Path
from src.mail_service import MailServiceFactory, EmailMessage

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def demo_auto_detection():
    """Demo automatic service detection."""
    print("🔧 Demo: Automatic Service Detection")
    print("=" * 50)

    # Create service (auto-detects environment)
    mail_service = MailServiceFactory.create_mail_service()

    # Show status
    status = mail_service.get_status()
    print(f"Service: {status['service']} ({status['type']})")
    print(f"Available: {status['available']}")
    print(f"Status: {status['status_message']}")

    if "web_ui" in status:
        print(f"Web UI: {status['web_ui']}")

    return mail_service


def demo_forced_mailpit():
    """Demo forced Mailpit usage."""
    print("\n🔧 Demo: Forced Mailpit Service")
    print("=" * 50)

    # Force Mailpit (useful for testing)
    mail_service = MailServiceFactory.create_mail_service(force_type="mailpit")

    status = mail_service.get_status()
    print(f"Service: {status['service']}")
    print(f"Available: {status['available']}")

    if status["available"]:
        print(f"SMTP: {status['host']}:{status['smtp_port']}")
        print(f"Web UI: {status['web_ui']}")
    else:
        print("❌ Mailpit not running!")
        print("   Start it with: ./mailpit/mailpit.exe")

    return mail_service


def demo_service_info():
    """Demo service information."""
    print("\n📋 Demo: Available Services")
    print("=" * 50)

    services = MailServiceFactory.get_available_services()

    for service_name, info in services.items():
        print(f"\n{info['name']}:")
        print(f"  Type: {info['type']}")
        print(f"  Description: {info['description']}")
        print(f"  Available: {info['available']}")
        if not info["available"]:
            print(f"  Status: {info['status']['status_message']}")


def demo_send_email(mail_service):
    """Demo sending an email."""
    print("\n📧 Demo: Sending Test Email")
    print("=" * 50)

    if not mail_service.is_available():
        print("❌ Mail service not available - skipping email demo")
        return False

    # Create test email
    message = EmailMessage(
        recipient="test@example.com",
        subject="Test Email from Mail Service Module",
        body="""Hello!

This is a test email from the mail service module.

Features demonstrated:
- Protocol-based architecture
- Environment detection
- Clean abstractions

If you're seeing this in Mailpit, everything is working! :)

Best regards,
The Mail Service Module
""",
    )

    # Send email
    print(f"Sending email to: {message.recipient}")
    print(f"Subject: {message.subject}")

    success = mail_service.send_email(message)

    if success:
        print("✅ Email sent successfully!")
        status = mail_service.get_status()
        if "web_ui" in status:
            print(f"   View in Mailpit: {status['web_ui']}")
    else:
        print("❌ Failed to send email")

    return success


def demo_start_mailpit():
    """Demo starting Mailpit."""
    print("\n🚀 Demo: Starting Mailpit")
    print("=" * 50)

    success = MailServiceFactory.start_mailpit("./mailpit/mailpit.exe")
    if success:
        print("✅ Mailpit is running!")
    else:
        print("❌ Could not start Mailpit")
        print("   Make sure mailpit.exe is in the ./mailpit/ folder")

    return success


def main():
    """Main demo function."""
    print("🎄 Mail Service Module Demo 🎄")
    print("=" * 50)
    print()

    # Demo 1: Auto detection
    mail_service = demo_auto_detection()

    # Demo 2: Forced Mailpit
    demo_forced_mailpit()

    # Demo 3: Service info
    demo_service_info()

    # Demo 4: Start Mailpit if needed
    if not mail_service.is_available():
        print("\n⚠️  Mail service not available, trying to start Mailpit...")
        demo_start_mailpit()
        # Re-create service to check if Mailpit is now available
        mail_service = MailServiceFactory.create_mail_service()

    # Demo 5: Send email
    demo_send_email(mail_service)

    print("\n🎉 Demo completed!")
    print("\nNext steps:")
    print("- Check emails in Mailpit web interface")
    print("- Try setting environment variables to test different modes")
    print("- Integrate the mail service into your Flask application")


if __name__ == "__main__":
    main()
