# Contributing to Secret Santa Application

Thank you for your interest in contributing to the Secret Santa application! This guide will help you get started.

## Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Kugeleis/wichteln.git
   cd wichteln
   ```

2. **Install Dependencies**
   ```bash
   uv sync
   ```

3. **Install Pre-commit Hooks**
   ```bash
   uv run pre-commit install
   ```

4. **Run Tests**
   ```bash
   make test
   ```

## Development Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run Quality Checks**
   ```bash
   # Run tests
   make test

   # Generate documentation
   make docs-generate

   # Check formatting
   uv run ruff check .
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- Follow PEP 8 conventions
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose

## Testing

- Write tests for all new functionality
- Maintain test coverage above 80%
- Use descriptive test names
- Include both unit and integration tests

## Documentation

- Update docstrings for any changes
- Add examples for new features
- Update the changelog for significant changes
- Generate docs with `make docs-generate`

## Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add a clear description of the changes
4. Reference any related issues
5. Request review from maintainers

## Getting Help

- Check existing issues and discussions
- Ask questions in issue comments
- Join our community discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
