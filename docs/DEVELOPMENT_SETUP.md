# Development Environment Configuration for Wichteln Flask App

## Environment Variables for Development Mode with Mailpit

```bash
# Core Flask settings
FLASK_ENV=development
FLASK_DEBUG=true

# Mail service configuration
USE_MAILPIT=true
MAILPIT_HOST=localhost
MAILPIT_PORT=1025
MAILPIT_WEB_PORT=8025
MAIL_DEFAULT_SENDER=noreply@wichteln.local

# Optional: Secret key for Flask sessions
SECRET_KEY=your-secret-key-here

# Optional: reCAPTCHA (for production)
RECAPTCHA_SECRET_KEY=your-recaptcha-secret-key
```

## Starting the Development Environment

### Option 1: PowerShell Script (Recommended)
```powershell
.\start_dev.ps1
```

### Option 2: Batch File (Windows CMD)
```cmd
start_dev.bat
```

### Option 3: Manual Setup
```powershell
$env:FLASK_ENV="development"
$env:USE_MAILPIT="true"
$env:FLASK_DEBUG="true"
python app.py
```

## Accessing the Application

- **Flask App**: http://127.0.0.1:5000
- **Mailpit Web UI**: http://localhost:8025

## Testing Email Functionality

1. Open your Flask app at http://127.0.0.1:5000
2. Create participants and generate assignments
3. Check captured emails in Mailpit at http://localhost:8025
4. All emails will be captured locally - no real emails are sent

## Development Workflow

1. Start the environment using one of the startup scripts
2. Mailpit will automatically start if not already running
3. Make changes to your code - Flask will auto-reload
4. Test email functionality through Mailpit
5. Stop with Ctrl+C

## Troubleshooting

### Mailpit Not Starting
- Ensure `mailpit.exe` exists in the `./mailpit/` directory
- Check if ports 1025 (SMTP) and 8025 (Web UI) are available
- Try starting Mailpit manually: `./mailpit/mailpit.exe`

### Flask App Issues
- Ensure Python environment is activated
- Check that all dependencies are installed
- Verify environment variables are set correctly

### Email Not Being Captured
- Verify Mailpit is running (check http://localhost:8025)
- Ensure `USE_MAILPIT=true` is set
- Check Flask console output for error messages
