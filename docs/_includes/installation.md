<!-- --8<-- [start: prerequisites] -->
## Prerequisites

- Python 3.12 or higher
- UV package manager (recommended) or pip
- Git for version control

> **💡 Platform Notes**:
> - **Windows**: Use `task` commands (requires [Task](https://taskfile.dev/installation/))
> - **Linux/macOS**: Use either `task` or `make` commands
<!-- --8<-- [end: prerequisites] -->

<!-- --8<-- [start: installation-uv] -->
### Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/Kugeleis/wichteln.git
cd wichteln

# Install dependencies
uv sync

# Start the development server
task dev
```
<!-- --8<-- [end: installation-uv] -->

<!-- --8<-- [start: installation-pip] -->
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

# Start the development server
task dev
```
<!-- --8<-- [end: installation-pip] -->

<!-- --8<-- [start: quick-start] -->
```bash
# Start the development server
task dev
```

Open your browser to `http://localhost:5000`
<!-- --8<-- [end: quick-start] -->
