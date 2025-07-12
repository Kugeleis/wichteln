# Secret Santa Application

A modern Flask web application for organizing Secret Santa events with participant management, automatic assignment generation, and email notifications.

## Features

✨ **Modern Web Interface**
- Clean, responsive design
- Easy participant registration
- Real-time form validation

🎯 **Smart Assignment Generation**
- Automatic Secret Santa assignment
- Configurable constraints and rules
- Duplicate prevention

📧 **Email Integration**
- Automated assignment notifications
- Custom email templates
- SMTP configuration support

🔒 **Security & Privacy**
- reCAPTCHA integration
- Input validation and sanitization
- Secure token management

## Quick Start

1. **Install Dependencies**
   ```bash
   uv sync
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Start the Development Server**
   ```bash
   task dev
   ```

4. **Access the Web Interface**
   - Open your browser to `http://localhost:5000`
   - Start adding participants and generating assignments!

## Architecture

The application follows a modular architecture with clear separation of concerns:

- **Services**: Core business logic and external integrations
- **Routes**: Web interface and API endpoints
- **Templates**: HTML templates with modern styling
- **Tests**: Comprehensive test suite with high coverage

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Email**: Flask-Mail with SMTP support
- **Security**: reCAPTCHA, input validation
- **Testing**: pytest with comprehensive coverage
- **Development**: Modern tooling with UV package manager

## Documentation Structure

- [**User Guide**](guide/quickstart.md) - How to use the application
- [**API Reference**](reference/services.md) - Detailed code documentation
- [**Development**](DEVELOPMENT_SETUP.md) - Setup and contribution guide

## Project Status

This project is actively maintained and follows modern Python development practices:

- 🔄 Continuous Integration with automated testing
- 📊 Code coverage tracking
- 🔧 Automated code formatting and linting
- 📝 Comprehensive documentation
- 🚀 Easy deployment with Docker support

---

**Ready to get started?** Check out the [Quick Start Guide](guide/quickstart.md) or explore the [API documentation](reference/services.md).
