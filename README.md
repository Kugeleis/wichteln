# 🎄 Secret Santa Application (Wichteln)

[![Documentation](https://github.com/Kugeleis/wichteln/actions/workflows/docs.yml/badge.svg)](https://github.com/Kugeleis/wichteln/actions/workflows/docs.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![UV](https://img.shields.io/badge/package_manager-UV-blue.svg)](https://github.com/astral-sh/uv)

A modern Flask web application for organizing Secret Santa events with participant management, automatic assignment generation, and email notifications.

## 🚀 Live Documentation

📚 **[View Documentation](https://kugeleis.github.io/wichteln/)** - Automatically updated from this repository

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

# Start the development server
task dev
```

🌐 **Open your browser to**: `http://localhost:5000`

> **💡 Platform Notes**:
> - **Windows**: Use `task` commands (requires [Task](https://taskfile.dev/installation/))
> - **Linux/macOS**: Use `make` commands (built-in) or install Task
> - **Cross-platform**: Task works everywhere and provides better Windows support

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
task dev           # Windows: task dev | Linux/macOS: make dev

# Run tests
task test          # Windows: task test | Linux/macOS: make test

# Generate documentation
task docs          # Windows: task docs | Linux/macOS: make docs

# View documentation locally
task docs-serve    # Windows: task docs-serve | Linux/macOS: make docs-serve
```

> **💡 Command Reference**: Use `task --list` (Windows) or `make help` (Linux/macOS) to see all available commands.

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

## � Continuous Integration

This project uses GitHub Actions for automated:

- **📚 Documentation Building**: Automatic generation and deployment to GitHub Pages
- **🧪 Quality Checks**: Pre-commit hooks, linting, formatting, and security scanning
- **🔍 Link Validation**: Documentation link checking (non-blocking)
- **📦 Dependency Management**: UV package manager with intelligent caching

### CI/CD Features

- ✅ **Automatic deployment** on push to main/master
- ✅ **PR preview builds** with 7-day retention
- ✅ **Path-based triggering** (only runs when relevant files change)
- ✅ **Parallel job execution** for faster feedback
- ✅ **Smart caching** for improved performance

[📖 Learn more about GitHub Pages deployment](docs/GITHUB_PAGES_DEPLOYMENT.md)

## �📄 License

This project is open source. See the license file for details.

## 🎉 Getting Started

1. **Clone and install** (see Quick Installation above)
2. **Start the development server** with `task dev`
3. **Configure email settings** (optional - see [Configuration Guide](docs/guide/configuration.md))
4. **Add participants** via the web interface
5. **Generate assignments** with one click
6. **Send notifications** to all participants automatically

Ready to organize your next Secret Santa event? [Get started now!](docs/guide/quickstart.md)

---

**Need help?** Check out the [documentation](https://kugeleis.github.io/wichteln/) or [open an issue](https://github.com/Kugeleis/wichteln/issues).
