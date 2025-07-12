"""
Mail service factory for creating and managing mail service instances.

This module provides a factory pattern implementation for creating appropriate
mail service instances based on environment and configuration.
"""

import os
import subprocess  # nosec B404 - needed for starting Mailpit process safely
from typing import Optional, Any
from flask import Flask
from .protocol import MailProtocol
from .mailpit import MailpitMailService
from .smtp import SMTPMailService


class MailServiceFactory:
    """
    Factory for creating and managing mail service instances.

    This factory automatically detects the environment and creates the appropriate
    mail service implementation. It also provides utilities for managing Mailpit.
    """

    @staticmethod
    def create_mail_service(
        app: Optional[Flask] = None, force_type: Optional[str] = None, **config: Any
    ) -> MailProtocol:
        """
        Create appropriate mail service based on environment and availability.

        Args:
            app: Flask application instance (optional)
            force_type: Force specific service type ("mailpit" or "smtp")
            **config: Additional configuration parameters

        Returns:
            MailProtocol instance (MailpitMailService or SMTPMailService)
        """
        # Check for forced type
        if force_type == "mailpit":
            return MailServiceFactory._create_mailpit_service(**config)
        elif force_type == "smtp":
            return MailServiceFactory._create_smtp_service(app, **config)

        # Auto-detect based on environment
        if MailServiceFactory._is_development_mode():
            # Try Mailpit first in development
            mailpit_service = MailServiceFactory._create_mailpit_service(**config)
            if mailpit_service.is_available():
                print("🔧 Using Mailpit for email (development mode)")
                return mailpit_service
            else:
                print("⚠️  Mailpit not available, falling back to SMTP service")
                return MailServiceFactory._create_smtp_service(app, **config)
        else:
            # Use SMTP service in production
            print("📧 Using SMTP service (production mode)")
            return MailServiceFactory._create_smtp_service(app, **config)

    @staticmethod
    def _create_mailpit_service(**config: Any) -> MailpitMailService:
        """
        Create Mailpit mail service.

        Args:
            **config: Configuration overrides

        Returns:
            MailpitMailService instance
        """
        host = str(config.get("host") or os.environ.get("MAILPIT_HOST", "localhost"))
        port = config.get("port") or int(os.environ.get("MAILPIT_PORT", 1025))
        web_ui_port = config.get("web_ui_port") or int(
            os.environ.get("MAILPIT_WEB_PORT", 8025)
        )
        sender = str(
            config.get("default_sender")
            or os.environ.get("MAIL_DEFAULT_SENDER", "noreply@localhost")
        )

        return MailpitMailService(
            host=host, port=port, web_ui_port=web_ui_port, default_sender=sender
        )

    @staticmethod
    def _create_smtp_service(
        app: Optional[Flask] = None, **config: Any
    ) -> SMTPMailService:
        """
        Create SMTP mail service.

        Args:
            app: Flask application instance
            **config: Configuration overrides

        Returns:
            SMTPMailService instance
        """
        return SMTPMailService(app, **config)

    @staticmethod
    def _is_development_mode() -> bool:
        """
        Check if application is running in development mode.

        Returns:
            bool: True if in development mode
        """
        return (
            os.environ.get("FLASK_ENV") == "development"
            or os.environ.get("FLASK_DEBUG", "").lower() in ["true", "1", "on"]
            or os.environ.get("USE_MAILPIT", "").lower() in ["true", "1", "on"]
        )

    @staticmethod
    def get_available_services() -> dict[str, Any]:
        """
        Get information about available mail services.

        Returns:
            Dict containing information about available services
        """
        services = {}

        # Check Mailpit
        mailpit = MailServiceFactory._create_mailpit_service()
        services["mailpit"] = {
            **mailpit.get_service_info(),
            "available": mailpit.is_available(),
            "status": mailpit.get_status(),
        }

        # Check SMTP (basic check without Flask app)
        smtp = SMTPMailService()
        services["smtp"] = {
            **smtp.get_service_info(),
            "available": smtp.is_available(),
            "status": smtp.get_status(),
        }

        return services

    @staticmethod
    def start_mailpit(mailpit_path: Optional[str] = None) -> bool:
        """
        Start Mailpit if it's not running.

        Args:
            mailpit_path: Path to mailpit executable

        Returns:
            bool: True if Mailpit was started or already running
        """
        # Check if Mailpit is already running
        mailpit_service = MailServiceFactory._create_mailpit_service()
        if mailpit_service.is_available():
            print("✅ Mailpit is already running")
            return True

        # Try to find and start Mailpit
        if not mailpit_path:
            # Look for mailpit.exe in common locations
            possible_paths = [
                "./mailpit/mailpit.exe",
                "./mailpit.exe",
                "mailpit/mailpit.exe",
                "mailpit",
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    mailpit_path = path
                    break

        if not mailpit_path or not os.path.exists(mailpit_path):
            print("❌ Mailpit executable not found")
            print(
                "   Please download from: https://github.com/axllent/mailpit/releases"
            )
            return False

        try:
            print(f"🚀 Starting Mailpit from: {mailpit_path}")

            # Get ports from environment and validate them
            smtp_port = os.environ.get("MAILPIT_PORT", "1025")
            web_port = os.environ.get("MAILPIT_WEB_PORT", "8025")

            # Validate ports are numeric to prevent injection
            try:
                int(smtp_port)
                int(web_port)
            except ValueError:
                print("❌ Invalid port numbers in environment variables")
                return False

            # Build command with custom ports if specified
            # Use absolute path to prevent PATH manipulation attacks
            cmd = [os.path.abspath(mailpit_path)]
            if smtp_port != "1025":
                cmd.extend(["--smtp", f"localhost:{smtp_port}"])
            if web_port != "8025":
                cmd.extend(["--listen", f"localhost:{web_port}"])

            # Start Mailpit in background with security measures
            subprocess.Popen(  # nosec B603 - safe because we control the executable path and validate inputs
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                if os.name == "nt"
                else 0,
                cwd=os.path.dirname(mailpit_path),  # Set working directory for safety
            )

            # Give it a moment to start
            import time

            time.sleep(2)

            # Check if it started successfully
            if mailpit_service.is_available():
                print("✅ Mailpit started successfully")
                status = mailpit_service.get_status()
                print(f"   📧 SMTP: {status['host']}:{status['smtp_port']}")
                print(f"   🌐 Web UI: {status['web_ui']}")
                return True
            else:
                print("❌ Mailpit failed to start")
                return False

        except Exception as e:
            print(f"❌ Failed to start Mailpit: {e}")
            return False

    def get_service(
        self,
        app: Optional[Flask] = None,
        force_type: Optional[str] = None,
        **config: Any,
    ) -> MailProtocol:
        """
        Get appropriate mail service instance.

        This is a convenience instance method that delegates to the static create_mail_service method.

        Args:
            app: Flask application instance (optional)
            force_type: Force specific service type ("mailpit" or "smtp")
            **config: Additional configuration parameters

        Returns:
            MailProtocol: Appropriate mail service instance
        """
        return self.create_mail_service(app=app, force_type=force_type, **config)
