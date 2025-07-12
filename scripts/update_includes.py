#!/usr/bin/env python3
"""
Template generator for documentation content using single point of truth.
This script dynamically extracts information from the project structure.
"""

import sys
from pathlib import Path

# Add the config directory to the Python path
config_dir = Path(__file__).parent.parent / "docs" / "_config"
sys.path.insert(0, str(config_dir))

try:
    from content import (
        PROJECT_NAME,
        PROJECT_DESCRIPTION,
        REPOSITORY_URL,
        PYTHON_VERSION,
        COMMANDS,
        PREREQUISITES,
        PLATFORM_NOTES,
        DEV_COMMANDS,
        MAKE_COMMANDS,
        PROJECT_VERSION,
        PYPROJECT_INFO,
        PROJECT_DEPENDENCIES,
    )
except ImportError as e:
    print(f"❌ Error importing configuration: {e}")
    print("Make sure content.py is properly configured.")
    sys.exit(1)


def generate_installation_section():
    """Generate installation section content."""
    content = f"""<!-- --8<-- [start: prerequisites] -->
## Prerequisites

{chr(10).join(f"- {req}" for req in PREREQUISITES)}

> **💡 Platform Notes**:
> - **Windows**: {PLATFORM_NOTES["windows"]}
> - **Linux/macOS**: {PLATFORM_NOTES["linux_macos"]}
<!-- --8<-- [end: prerequisites] -->

<!-- --8<-- [start: installation-uv] -->
### Using UV (Recommended)

```bash
# Clone the repository
{COMMANDS["clone"]}
{COMMANDS["enter_dir"]}

# Install dependencies
{COMMANDS["uv_sync"]}

# Start the development server
{COMMANDS["start_dev"]}
```
<!-- --8<-- [end: installation-uv] -->

<!-- --8<-- [start: installation-pip] -->
### Using Pip

```bash
# Clone the repository
{COMMANDS["clone"]}
{COMMANDS["enter_dir"]}

# Create virtual environment
{COMMANDS["pip_venv_create"]}
{COMMANDS["pip_venv_activate_unix"]}  # On Windows: {COMMANDS["pip_venv_activate_windows"]}

# Install dependencies
{COMMANDS["pip_install"]}

# Start the development server
{COMMANDS["start_dev"]}
```
<!-- --8<-- [end: installation-pip] -->

<!-- --8<-- [start: quick-start] -->
```bash
# Start the development server
{COMMANDS["start_dev"]}
```

Open your browser to `{COMMANDS["open_browser"]}`
<!-- --8<-- [end: quick-start] -->"""
    return content


def generate_commands_section():
    """Generate common commands section."""
    task_commands = "\n".join(f"{cmd:<20} # {desc}" for cmd, desc in DEV_COMMANDS)
    make_commands = "\n".join(f"{cmd:<20} # {desc}" for cmd, desc in MAKE_COMMANDS)

    content = f"""<!-- --8<-- [start: common-commands] -->
## Available Commands

```bash
# View all available commands
task --list        # Windows
make help          # Linux/macOS (if help target exists)

# Key commands (cross-platform):
{task_commands}

# Alternative for Linux/macOS:
{make_commands}
```

> **💡 Platform Notes**:
> - **{PLATFORM_NOTES["task_benefits"]}**
> - **{PLATFORM_NOTES["make_availability"]}**
> - Both tools run the same underlying commands
<!-- --8<-- [end: common-commands] -->"""
    return content


def generate_project_summary_section():
    """Generate a project summary section with all extracted information."""
    content = f"""<!-- --8<-- [start: project-summary] -->
## Project Information

- **Name**: {PROJECT_NAME}
- **Version**: {PROJECT_VERSION}
- **Description**: {PROJECT_DESCRIPTION}
- **Python Version**: {PYTHON_VERSION} or higher
- **Repository**: [{REPOSITORY_URL}]({REPOSITORY_URL})

### Dependencies

The project uses the following main dependencies:
{chr(10).join(f"- `{dep}`" for dep in PROJECT_DEPENDENCIES) if PROJECT_DEPENDENCIES else "- Dependencies managed through pyproject.toml"}

### Project Structure

This project follows modern Python packaging standards with:
- `pyproject.toml` for project configuration
- UV for dependency management
- Task runner for development commands
- MkDocs for documentation
<!-- --8<-- [end: project-summary] -->"""
    return content


def update_includes():
    """Update the include files with generated content."""
    docs_dir = Path(__file__).parent.parent / "docs"
    includes_dir = docs_dir / "_includes"
    includes_dir.mkdir(exist_ok=True)

    print("🔄 Updating includes from project configuration...")
    print(f"📊 Project: {PROJECT_NAME}")
    print(f"🐍 Python: {PYTHON_VERSION}")
    print(f"📦 Repository: {REPOSITORY_URL}")
    print(f"📝 Description: {PROJECT_DESCRIPTION}")

    # Update installation.md
    installation_content = generate_installation_section()
    (includes_dir / "installation.md").write_text(
        installation_content, encoding="utf-8"
    )

    # Update commands.md
    commands_content = generate_commands_section()
    (includes_dir / "commands.md").write_text(commands_content, encoding="utf-8")

    # Update project_summary.md
    project_summary_content = generate_project_summary_section()
    (includes_dir / "project_summary.md").write_text(
        project_summary_content, encoding="utf-8"
    )

    print("✅ Include files updated from project structure")
    print("📁 Files updated:")
    print(f"   - {includes_dir / 'installation.md'}")
    print(f"   - {includes_dir / 'commands.md'}")
    print(f"   - {includes_dir / 'project_summary.md'}")
    print(
        f"🎯 Tasks extracted: {len(DEV_COMMANDS)} task commands, {len(MAKE_COMMANDS)} make commands"
    )


def display_extraction_summary():
    """Display what information was extracted from where."""
    print("\n📋 Configuration Extraction Summary:")
    print("=" * 50)

    # Check if pyproject.toml was used
    pyproject_used = bool(PYPROJECT_INFO)

    print(f"📁 Project Name: {PROJECT_NAME}")
    if pyproject_used and PYPROJECT_INFO.get("name"):
        print("   └─ Source: pyproject.toml [project.name]")
    else:
        print("   └─ Source: Hardcoded fallback")

    print(f"📝 Project Description: {PROJECT_DESCRIPTION[:60]}...")
    if pyproject_used and PYPROJECT_INFO.get("description"):
        print("   └─ Source: pyproject.toml [project.description]")
    else:
        print("   └─ Source: README.md first paragraph")

    print(f"🔢 Project Version: {PROJECT_VERSION}")
    if pyproject_used and PYPROJECT_INFO.get("version"):
        print("   └─ Source: pyproject.toml [project.version]")
    else:
        print("   └─ Source: Source code __version__")

    print(f"🐍 Python Version: {PYTHON_VERSION}")
    if pyproject_used and PYPROJECT_INFO.get("requires_python"):
        print("   └─ Source: pyproject.toml [project.requires-python]")
    else:
        print("   └─ Source: uv.lock file (requires-python)")

    print(f"📦 Repository URL: {REPOSITORY_URL}")
    if pyproject_used and (
        PYPROJECT_INFO.get("repository")
        or PYPROJECT_INFO.get("urls", {}).get("repository")
    ):
        print("   └─ Source: pyproject.toml [project.urls.repository]")
    else:
        print("   └─ Source: git remote origin")

    if PROJECT_DEPENDENCIES:
        print(f"� Dependencies: {len(PROJECT_DEPENDENCIES)} found")
        print("   └─ Source: pyproject.toml [project.dependencies]")
        print(
            f"   └─ Packages: {', '.join(PROJECT_DEPENDENCIES[:5])}{'...' if len(PROJECT_DEPENDENCIES) > 5 else ''}"
        )

    print(f"🎯 Task Commands: {len(DEV_COMMANDS)} extracted")
    print("   └─ Source: Taskfile.yml task descriptions")

    print(f"🔧 Make Commands: {len(MAKE_COMMANDS)} extracted")
    print("   └─ Source: Makefile target comments")

    if pyproject_used:
        print("\n🎉 pyproject.toml successfully integrated!")
    else:
        print("\n⚠️  No pyproject.toml found, using fallback sources")

    print("\n💡 All documentation now reflects actual project state!")


if __name__ == "__main__":
    update_includes()
    display_extraction_summary()
    display_extraction_summary()
