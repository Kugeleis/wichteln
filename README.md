# 🎄 Secret Santa Application (Wichteln)

A modern Flask web application for organizing Secret Santa events with participant management, automatic assignment generation, and email notifications.

## 🎯 Purpose

This application simplifies the organization of Secret Santa (Wichteln) events by:

- **Collecting Participants**: Easy web form for adding participants with names and email addresses
- **Generating Assignments**: Automatically creates random Secret Santa pairings with configurable constraints
- **Sending Notifications**: Automated email delivery to inform participants of their assignments
- **Managing Events**: Complete workflow from setup to completion with a clean web interface

Perfect for office parties, family gatherings, friend groups, or any event where you want to organize a gift exchange without the hassle of manual coordination.

## ⚡ Quick Installation

### Prerequisites
- Python 3.12 or higher
- UV package manager (recommended)

### Install & Run
```bash
# Clone the repository
git clone https://github.com/Kugeleis/wichteln.git
cd wichteln

# Install dependencies
uv sync

# Run the application
uv run python app.py
```

🌐 **Open your browser to**: `http://localhost:5000`

## 🚀 Features

- ✨ **Modern Web Interface** - Clean, responsive design
- 🎯 **Smart Assignment Generation** - Automatic Secret Santa pairing with duplicate prevention
- 📧 **Email Integration** - Automated notifications with customizable templates
- 🔒 **Security & Privacy** - reCAPTCHA integration and input validation
- 🎨 **Professional UI** - Modern styling with intuitive user experience

## 📚 Documentation

For detailed setup, configuration, and deployment instructions, visit our comprehensive documentation:

🔗 **[Full Documentation](https://kugeleis.github.io/wichteln/)**

### Quick Links
- [📖 User Guide](docs/guide/quickstart.md) - Complete setup and usage instructions
- [⚙️ Configuration](docs/guide/configuration.md) - Email and security settings
- [🚀 Deployment](docs/guide/deployment.md) - Production deployment options
- [🔧 API Reference](docs/reference/services.md) - Technical documentation

## 🛠️ Development

### Available Commands
```bash
# Development server
task dev

# Run tests
task test

# Generate documentation
task docs

# View documentation locally
task docs-serve
```

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Email**: Flask-Mail with SMTP support
- **Security**: reCAPTCHA, input validation
- **Testing**: pytest with comprehensive coverage
- **Development**: Modern tooling with UV package manager

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:
- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

## 📄 License

This project is open source. See the license file for details.

## 🎉 Getting Started

1. **Clone and install** (see Quick Installation above)
2. **Configure email settings** (optional - see [Configuration Guide](docs/guide/configuration.md))
3. **Add participants** via the web interface
4. **Generate assignments** with one click
5. **Send notifications** to all participants automatically

Ready to organize your next Secret Santa event? [Get started now!](docs/guide/quickstart.md)

---

**Need help?** Check out the [documentation](https://kugeleis.github.io/wichteln/) or [open an issue](https://github.com/Kugeleis/wichteln/issues).
