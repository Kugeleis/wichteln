# Quick Start Guide

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
source venv/bin/activate  # On Windows: venv\Scripts\activate

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
