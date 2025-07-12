<!-- --8<-- [start: common-commands] -->
## Available Commands

```bash
# View all available commands
task --list        # Windows
make help          # Linux/macOS (if help target exists)

# Key commands (cross-platform):
task dev             # Start development server
task test            # Run tests
task docs            # Generate and build documentation
task docs-serve      # Start documentation server
task clean           # Clean build artifacts

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
