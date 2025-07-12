# Configuration Guide

Configure the Secret Santa application for your environment.

## Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# reCAPTCHA Configuration
RECAPTCHA_SITE_KEY=your-site-key
RECAPTCHA_SECRET_KEY=your-secret-key
```

## Email Setup

### Gmail Configuration

1. Enable 2-factor authentication
2. Generate an app password
3. Use the app password in `MAIL_PASSWORD`

### Custom SMTP Server

```env
MAIL_SERVER=your.smtp.server.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-username
MAIL_PASSWORD=your-password
```

## Security Settings

### reCAPTCHA Setup

1. Visit [Google reCAPTCHA](https://www.google.com/recaptcha/)
2. Create a new site
3. Add your domain
4. Copy the site key and secret key to your `.env` file

### Secret Key

Generate a secure secret key:

```python
import secrets
print(secrets.token_hex(16))
```

## Advanced Configuration

### Custom Email Templates

Email templates are located in `services/email_templates.py`. Customize the message content and styling as needed.

### Logging Configuration

Configure logging levels in `services/debug_logger.py` for different environments.
