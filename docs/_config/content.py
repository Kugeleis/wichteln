"""
Central configuration for documentation content.
This serves as the single point of truth for all repeated information.
It dynamically extracts information from the project structure.
"""

import re
import subprocess  # nosec B404 # subprocess is safe for git commands
import toml
from pathlib import Path
from typing import Any

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent


def load_pyproject() -> dict[str, Any]:
    """Load and return pyproject.toml as a dictionary."""
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    if not pyproject_path.exists():
        return {}

    try:
        with open(pyproject_path, "r", encoding="utf-8") as f:
            return toml.load(f)
    except Exception as e:
        print(f"Warning: Could not parse pyproject.toml: {e}")
        return {}


# Load pyproject.toml once
PYPROJECT = load_pyproject()


def get_from_pyproject(path: str, fallback: Any = "") -> Any:
    """Extract value from pyproject.toml using dot notation path."""
    keys = path.split(".")
    value = PYPROJECT

    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return fallback


def get_python_version_from_uv_lock() -> str:
    """Extract Python version requirement from uv.lock."""
    uv_lock_path = PROJECT_ROOT / "uv.lock"
    if uv_lock_path.exists():
        try:
            with open(uv_lock_path, "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r'requires-python\s*=\s*">=([0-9.]+)"', content)
                if match:
                    return match.group(1)
        except (OSError, IOError):
            # Specific exception handling instead of bare except pass
            return "3.12"
    return "3.12"


def get_git_repository_url() -> str:
    """Extract repository URL from git config."""
    try:
        result = subprocess.run(  # nosec B603, B607 # git is trusted command
            ["git", "remote", "get-url", "origin"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=10,  # Add timeout for security
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            if url.startswith("git@github.com:"):
                url = url.replace("git@github.com:", "https://github.com/")
            if url.endswith(".git"):
                url = url[:-4]
            return url
    except (subprocess.SubprocessError, subprocess.TimeoutExpired, OSError):
        # Specific exception handling instead of bare except pass
        return ""
    return ""


def clean_dependencies(deps: list[str]) -> list[str]:
    """Clean dependency names by removing version specifiers."""
    clean_deps = []
    for dep in deps:
        package_name = re.split(r"[>=<~!\[]", dep)[0].strip()
        if package_name:
            clean_deps.append(package_name)
    return clean_deps


def extract_tasks_from_taskfile() -> list[tuple]:
    """Extract available tasks from Taskfile.yml."""
    taskfile_path = PROJECT_ROOT / "Taskfile.yml"
    if not taskfile_path.exists():
        return [
            ("task dev", "Start development server"),
            ("task test", "Run tests"),
            ("task docs", "Generate and build documentation"),
        ]

    try:
        with open(taskfile_path, "r", encoding="utf-8") as f:
            content = f.read()
            tasks = []
            current_task = None

            for line in content.split("\n"):
                line = line.strip()
                if line.endswith(":") and not line.startswith(" ") and line != "tasks:":
                    current_task = line[:-1]
                elif line.startswith("desc:") and current_task:
                    desc = line.split("desc:", 1)[1].strip().strip("\"'")
                    tasks.append((f"task {current_task}", desc))
                    current_task = None

            return (
                tasks
                if tasks
                else [
                    ("task dev", "Start development server"),
                    ("task test", "Run tests"),
                    ("task docs", "Generate and build documentation"),
                ]
            )
    except Exception:
        return [
            ("task dev", "Start development server"),
            ("task test", "Run tests"),
            ("task docs", "Generate and build documentation"),
        ]


def extract_makefile_tasks() -> list[tuple]:
    """Extract available tasks from Makefile."""
    makefile_path = PROJECT_ROOT / "Makefile"
    if not makefile_path.exists():
        return [
            ("make dev", "Start development server"),
            ("make test", "Run tests"),
            ("make docs", "Generate and build documentation"),
        ]

    try:
        with open(makefile_path, "r", encoding="utf-8") as f:
            content = f.read()
            tasks = []

            for line in content.split("\n"):
                if (
                    ":" in line
                    and not line.startswith("\t")
                    and not line.startswith(" ")
                ):
                    parts = line.split("#", 1)
                    if len(parts) == 2:
                        target = parts[0].split(":")[0].strip()
                        desc = parts[1].strip()
                        tasks.append((f"make {target}", desc))

            return (
                tasks
                if tasks
                else [
                    ("make dev", "Start development server"),
                    ("make test", "Run tests"),
                    ("make docs", "Generate and build documentation"),
                ]
            )
    except Exception:
        return [
            ("make dev", "Start development server"),
            ("make test", "Run tests"),
            ("make docs", "Generate and build documentation"),
        ]


# Simplified project information extraction using dictionary access
PROJECT_DICT = get_from_pyproject("project", {})

# Extract Python version with fallback chain
python_version_match = re.search(
    r">=([0-9.]+)", PROJECT_DICT.get("requires-python", "")
)
PYTHON_VERSION = (
    python_version_match.group(1)
    if python_version_match
    else get_python_version_from_uv_lock()
)

# Extract basic project information
PROJECT_NAME = (
    PROJECT_DICT.get("name", "wichteln").replace("-", " ").replace("_", " ").title()
)
PROJECT_VERSION = PROJECT_DICT.get("version", "1.0.0")
PROJECT_DESCRIPTION = PROJECT_DICT.get(
    "description", "A modern Flask application for organizing Secret Santa events"
)

# Extract repository URL with fallback
PROJECT_URLS = PROJECT_DICT.get("urls", {})
REPOSITORY_URL = (
    PROJECT_URLS.get("repository")
    or PROJECT_URLS.get("Repository")
    or get_from_pyproject("tool.poetry.repository", "")
    or get_git_repository_url()
    or "https://github.com/Kugeleis/wichteln"
)

# Extract and clean dependencies
PROJECT_DEPENDENCIES = clean_dependencies(PROJECT_DICT.get("dependencies", []))

# Extract project directory name from repository URL
PROJECT_DIR_NAME = (
    REPOSITORY_URL.rstrip("/").split("/")[-1] if REPOSITORY_URL else "wichteln"
)

# Installation Commands
COMMANDS = {
    "clone": f"git clone {REPOSITORY_URL}.git"
    if not REPOSITORY_URL.endswith(".git")
    else f"git clone {REPOSITORY_URL}",
    "enter_dir": f"cd {PROJECT_DIR_NAME}",
    "uv_sync": "uv sync",
    "start_dev": "task dev",
    "pip_venv_create": "python -m venv venv",
    "pip_venv_activate_unix": "source venv/bin/activate",
    "pip_venv_activate_windows": "venv\\Scripts\\activate",
    "pip_install": "pip install -r requirements.txt",
    "open_browser": "http://localhost:5000",
}

# Prerequisites
PREREQUISITES = [
    f"Python {PYTHON_VERSION} or higher",
    "UV package manager (recommended) or pip",
    "Git for version control",
]

# Platform-specific notes
PLATFORM_NOTES = {
    "windows": "Use `task` commands (requires [Task](https://taskfile.dev/installation/))",
    "linux_macos": "Use either `task` or `make` commands",
    "task_benefits": "Task provides better Windows support and consistent behavior across platforms",
    "make_availability": "Make is built into Linux/macOS but requires additional setup on Windows",
}

# Dynamic command extraction
DEV_COMMANDS = extract_tasks_from_taskfile()
MAKE_COMMANDS = extract_makefile_tasks()

# Keep original PYPROJECT_INFO for backward compatibility
PYPROJECT_INFO = PYPROJECT
