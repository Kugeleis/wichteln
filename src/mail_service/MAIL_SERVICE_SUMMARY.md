# Mail Service Module Documentation

## Overview

The `mail_service` module is a self-contained email abstraction layer providing clean, protocol-based architecture for email functionality with support for both development (Mailpit) and production (SMTP) environments.

## 📁 Architecture

```
src/mail_service/
├── __init__.py          # Module exports and main interface
├── protocol.py          # Abstract protocol and EmailMessage
├── mailpit.py          # Mailpit implementation (development)
├── smtp.py             # SMTP implementation (production)
└── factory.py          # Factory for creating service instances
```

**Protocol hierarchy:**
```
MailProtocol (Abstract Interface)
├── MailpitMailService (Development/Testing)
└── SMTPMailService (Production)
```

## 🎯 Key Features

- **Self-contained**: Independent module, reusable across projects
- **Protocol-based**: Clean abstractions with `MailProtocol` interface
- **Environment-aware**: Auto-detects development vs production mode
- **Easy integration**: Single import for Flask apps
- **Comprehensive**: Supports both Mailpit (dev) and SMTP (prod)
- **Developer-friendly**: Auto-start Mailpit, clear status reporting

## � Quick Start

```python
from src.mail_service import MailServiceFactory, EmailMessage

# Auto-detect environment and create service
mail_service = MailServiceFactory.create_mail_service(app)

# Send an email
message = EmailMessage(
    recipient="user@example.com",
    subject="Secret Santa Assignment",
    body="You are the Secret Santa for: Alice"
)
success = mail_service.send_email(message)
```

## ⚙️ Configuration

### Development Mode (Mailpit)
```bash
FLASK_ENV=development         # Enable development mode
MAILPIT_PORT=1025            # SMTP port (default: 1025)
MAILPIT_WEB_PORT=8025        # Web UI port (default: 8025)
```

### Production Mode (SMTP)
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### Force Specific Service
```python
# Force Mailpit for testing
mail_service = MailServiceFactory.create_mail_service(force_type="mailpit")

# Force SMTP for production
mail_service = MailServiceFactory.create_mail_service(app, force_type="smtp")
```

## � Development Workflow

### 1. Start Mailpit
```bash
./mailpit/mailpit.exe                                    # Default ports
./mailpit/mailpit.exe --smtp=localhost:2525 --listen=localhost:9025  # Custom ports
```

### 2. Run Flask Application
```bash
task dev
```

### 3. Test Email Functionality
- **Test route**: http://localhost:5000/dev/test-email
- **View emails**: http://localhost:8025 (or custom port)
- **Demo script**: `python mail_service_demo.py`

## 📊 Service Status

Check service status programmatically:
```python
status = mail_service.get_status()
print(f"Service: {status['service']} ({status['type']})")
print(f"Available: {status['available']}")
print(f"Status: {status['status_message']}")
```

**Example outputs:**
- **Mailpit**: `"Mailpit (development)" - "Ready for email capture"`
- **SMTP**: `"SMTP Server (production)" - "Ready to send emails"`

## � Code Examples

### Basic Usage
```python
# Automatic service selection
from src.mail_service import MailServiceFactory, EmailMessage

factory = MailServiceFactory()
mail_service = factory.get_service()

# Send email
message = EmailMessage(
    subject="Test Email",
    recipients=["test@example.com"],
    body="Hello from Python!",
    html_body="<h1>Hello from Python!</h1>"
)

success = mail_service.send_email(message)
```

### Manual Service Creation
```python
# Force specific service
from src.mail_service import MailpitMailService, SMTPMailService

# Development with Mailpit
dev_service = MailpitMailService()

# Production with SMTP
smtp_service = SMTPMailService(flask_app=app)
```

## 🏗️ Architecture

The mail service follows a protocol-based architecture:

```
MailProtocol (ABC)
├── MailpitMailService    → Development email capture
└── SMTPMailService       → Production email sending

MailServiceFactory        → Automatic service selection
EmailMessage             → Standardized message format
```

**Benefits:**
- **Decoupling**: Easy service switching without code changes
- **Testing**: Mock implementations for unit tests
- **Environment adaptation**: Automatic dev/prod configuration
- **Extensibility**: Add new services by implementing MailProtocol

## 🎯 Production Ready

### Development Setup
```bash
# Set environment
$env:FLASK_ENV="development"
$env:MAILPIT_PORT="2525"      # If port 1025 is busy
$env:MAILPIT_WEB_PORT="9025"  # If port 8025 is busy

# Start services
./mailpit/mailpit.exe         # Auto-starts with factory
task dev                      # Flask app with auto-detection
```

### Production Setup
```bash
# Configure SMTP
$env:MAIL_SERVER="smtp.gmail.com"
$env:MAIL_PORT="587"
$env:MAIL_USE_TLS="true"
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-app-password"
$env:MAIL_DEFAULT_SENDER="your-email@gmail.com"

# Start app (automatically uses SMTP in production)
task dev
```

The mail service module is now a complete, self-contained solution that can be easily reused across projects while providing excellent developer experience and production reliability! 🚀
