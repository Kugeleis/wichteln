<!-- --8<-- [start: common-commands] -->
## Available Commands

```bash
# View all available commands
task --list        # Windows
make help          # Linux/macOS (if help target exists)

# Key commands (cross-platform):
task dev             # Starts the Flask development server with Mailpit in development mode.
task test            # Runs all project tests using pytest.
task update          # Updates project dependencies.
task pre-commit-install # Installs pre-commit hooks.
task release         # Runs semantic-release to publish a new version.
task version-minor   # Creates a minor version bump.
task version-patch   # Creates a patch version bump.
task publish         # Builds the project distribution.
task clean           # Cleans up build artifacts and cache.
task docs-generate   # Generates API documentation from source code.
task docs-serve      # Starts the documentation development server.
task docs-build      # Builds the documentation site.
task docs-deploy     # Deploys documentation to GitHub Pages.
task docs            # Generates and builds the complete documentation.
task update-includes # Update documentation includes from single point of truth.

# Alternative for Linux/macOS:
make dev             # Start development server
make test            # Run tests
make docs            # Generate and build documentation
```

> **💡 Platform Notes**:
> - **Task provides better Windows support and consistent behavior across platforms**
> - **Make is built into Linux/macOS but requires additional setup on Windows**
> - Both tools run the same underlying commands
<!-- --8<-- [end: common-commands] -->
