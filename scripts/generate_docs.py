"""
Generate API documentation automatically from source code.

This script creates markdown files for each Python module that can be
automatically processed by mkdocstrings to generate comprehensive API documentation.
"""

from pathlib import Path
from typing import Any
import ast


def get_module_info(module_path: Path) -> dict[str, Any]:
    """Extract information about a Python module."""
    try:
        with open(module_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        # Extract module docstring
        docstring = ast.get_docstring(tree)

        # Extract classes and functions
        classes: list[str] = [
            node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
        ]
        functions: list[str] = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
        ]

        return {
            "docstring": docstring,
            "classes": classes,
            "functions": functions,
            "has_content": bool(classes or functions),
        }
    except Exception as e:
        print(f"Warning: Could not parse {module_path}: {e}")
        return {"docstring": None, "classes": [], "functions": [], "has_content": False}


def generate_service_docs() -> None:
    """Generate documentation for the services module."""
    services_dir = Path("services")
    docs_dir = Path("docs/reference")
    docs_dir.mkdir(parents=True, exist_ok=True)

    if not services_dir.exists():
        print(f"Warning: {services_dir} directory not found")
        return

    service_modules: list[dict[str, Any]] = []

    for py_file in services_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue

        module_info = get_module_info(py_file)
        if not module_info["has_content"]:
            continue

        module_name = py_file.stem
        module_path = f"services.{module_name}"

        service_modules.append(
            {"name": module_name, "path": module_path, "info": module_info}
        )

    # Generate services overview page
    with open(docs_dir / "services.md", "w", encoding="utf-8") as f:
        f.write("# Services API Reference\n\n")
        f.write(
            "The services layer contains the core business logic and external integrations.\n\n"
        )

        for module in service_modules:
            f.write(f"## {module['name'].replace('_', ' ').title()}\n\n")
            if module["info"]["docstring"]:
                f.write(f"{module['info']['docstring']}\n\n")
            f.write(f"::: {module['path']}\n\n")


def generate_routes_docs() -> None:
    """Generate documentation for the routes module."""
    routes_dir = Path("routes")
    docs_dir = Path("docs/reference")
    docs_dir.mkdir(parents=True, exist_ok=True)

    if not routes_dir.exists():
        print(f"Warning: {routes_dir} directory not found")
        return

    route_modules: list[dict[str, Any]] = []

    for py_file in routes_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue

        module_info = get_module_info(py_file)
        if not module_info["has_content"]:
            continue

        module_name = py_file.stem
        module_path = f"routes.{module_name}"

        route_modules.append(
            {"name": module_name, "path": module_path, "info": module_info}
        )

    # Generate routes overview page
    with open(docs_dir / "routes.md", "w", encoding="utf-8") as f:
        f.write("# Routes API Reference\n\n")
        f.write(
            "The routes layer handles HTTP requests and responses for the web interface.\n\n"
        )

        for module in route_modules:
            f.write(f"## {module['name'].replace('_', ' ').title()}\n\n")
            if module["info"]["docstring"]:
                f.write(f"{module['info']['docstring']}\n\n")
            f.write(f"::: {module['path']}\n\n")


def generate_utils_docs() -> None:
    """Generate documentation for utility modules."""
    docs_dir = Path("docs/reference")
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Check for utility modules in various locations
    util_locations = ["src", "utils", "."]
    util_modules: list[dict[str, Any]] = []

    for location in util_locations:
        location_path = Path(location)
        if not location_path.exists():
            continue

        for py_file in location_path.glob("*.py"):
            if py_file.name in ["__init__.py", "app.py", "setup.py"]:
                continue

            module_info = get_module_info(py_file)
            if not module_info["has_content"]:
                continue

            module_name = py_file.stem
            module_path = (
                module_name if location == "." else f"{location}.{module_name}"
            )

            util_modules.append(
                {"name": module_name, "path": module_path, "info": module_info}
            )

    if not util_modules:
        return

    # Generate utils overview page
    with open(docs_dir / "utils.md", "w", encoding="utf-8") as f:
        f.write("# Utilities API Reference\n\n")
        f.write("Utility modules and helper functions.\n\n")

        for module in util_modules:
            f.write(f"## {module['name'].replace('_', ' ').title()}\n\n")
            if module["info"]["docstring"]:
                f.write(f"{module['info']['docstring']}\n\n")
            f.write(f"::: {module['path']}\n\n")


def generate_guide_docs() -> None:
    """Generate user guide documentation."""
    guide_dir = Path("docs/guide")
    guide_dir.mkdir(parents=True, exist_ok=True)

    # Quick Start Guide
    with open(guide_dir / "quickstart.md", "w", encoding="utf-8") as f:
        f.write("""# Quick Start Guide

Get up and running with the Secret Santa application in minutes.

## Prerequisites

- Python 3.12 or higher
- UV package manager (recommended) or pip

## Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/Kugeleis/wichteln.git
cd wichteln

# Install dependencies
uv sync

# Run the application
uv run python app.py
```

### Using Pip

```bash
# Clone the repository
git clone https://github.com/Kugeleis/wichteln.git
cd wichteln

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Basic Usage

1. **Start the Application**
   ```bash
   uv run python app.py
   ```

2. **Open Your Browser**
   Navigate to `http://localhost:5000`

3. **Add Participants**
   - Click "Add Participant"
   - Enter name and email address
   - Repeat for all participants

4. **Generate Assignments**
   - Click "Generate Assignments"
   - Review the assignments
   - Send notification emails

## Next Steps

- [Configure email settings](configuration.md)
- [Deploy to production](deployment.md)
- [Explore the API](../reference/services.md)
""")

    # Configuration Guide
    with open(guide_dir / "configuration.md", "w", encoding="utf-8") as f:
        f.write("""# Configuration Guide

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
""")

    # Deployment Guide
    with open(guide_dir / "deployment.md", "w", encoding="utf-8") as f:
        f.write("""# Deployment Guide

Deploy the Secret Santa application to production.

## Production Checklist

- [ ] Set `FLASK_DEBUG=False`
- [ ] Use a strong `SECRET_KEY`
- [ ] Configure proper email settings
- [ ] Set up reCAPTCHA
- [ ] Configure logging
- [ ] Set up monitoring

## Deployment Options

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync --frozen

EXPOSE 5000
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t secret-santa .
docker run -p 5000:5000 --env-file .env secret-santa
```

### Heroku Deployment

1. Create a `Procfile`:
   ```
   web: uv run gunicorn app:app
   ```

2. Deploy:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### VPS Deployment

1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   pip3 install uv
   ```

2. **Setup Application**
   ```bash
   git clone https://github.com/Kugeleis/wichteln.git
   cd wichteln
   uv sync
   ```

3. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Setup Systemd Service**
   ```ini
   [Unit]
   Description=Secret Santa App
   After=network.target

   [Service]
   User=your-user
   WorkingDirectory=/path/to/wichteln
   ExecStart=/path/to/uv run gunicorn app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

## Monitoring

### Logging

Configure structured logging for production:

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
```

### Health Checks

Add a health check endpoint:

```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'version': '1.0.0'}
```

## Security Considerations

- Use HTTPS in production
- Set proper CORS headers
- Implement rate limiting
- Regular security updates
- Monitor for suspicious activity
""")


def main():
    """Generate all documentation files."""
    print("🔄 Generating API documentation...")

    # Generate API reference docs
    generate_service_docs()
    print("✅ Services documentation generated")

    generate_routes_docs()
    print("✅ Routes documentation generated")

    generate_utils_docs()
    print("✅ Utils documentation generated")

    # Generate user guide docs
    generate_guide_docs()
    print("✅ User guide documentation generated")

    print("📚 Documentation generation complete!")
    print("\nNext steps:")
    print("  uv run mkdocs serve    # Start development server")
    print("  uv run mkdocs build    # Build static site")
    print("  uv run mkdocs gh-deploy # Deploy to GitHub Pages")


if __name__ == "__main__":
    main()
