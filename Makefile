PYTHON := .venv/Scripts/python.exe
UV := .venv/Scripts/uv.exe

.PHONY: all dev test update publish clean version-minor version-patch docs docs-serve docs-build docs-deploy docs-generate

all: dev

dev:
	@echo "🎄 Starting Wichteln Development Environment 🎄"
	@echo "=================================================="
	@echo "Setting up development environment..."
	@echo "  FLASK_ENV: development"
	@echo "  USE_MAILPIT: true"
	@echo "  FLASK_DEBUG: true"
	@echo ""
	@if not exist ".\mailpit\mailpit.exe" ( \
		echo "❌ Mailpit executable not found at .\mailpit\mailpit.exe" && \
		echo "   Please download Mailpit from: https://github.com/axllent/mailpit/releases" && \
		exit /b 1 \
	) else ( \
		echo "✅ Mailpit executable found" \
	)
	@echo ""
	@echo "🚀 Starting application..."
	@echo "   📧 Mailpit will start automatically if not running"
	@echo "   🌐 Mailpit Web UI: http://localhost:8025"
	@echo "   🎯 Flask App: http://127.0.0.1:5000"
	@echo ""
	@echo "Press Ctrl+C to stop the application"
	@echo ""
	@set FLASK_ENV=development && set USE_MAILPIT=true && set FLASK_DEBUG=true && $(PYTHON) app.py

test:
	@echo "Running tests..."
	@$(UV) run python -m pytest

update:
	@echo "Updating dependencies..."
	@$(UV) pip install -e .
	@$(UV) pip install -U flask pytest python-semantic-release pre-commit

pre-commit-install:
	@echo "Installing pre-commit hooks..."
	@$(UV) run pre-commit install

release:
	@echo "Running semantic-release to publish a new version..."
	@$(UV) run python -m semantic_release publish

version-minor:
	@echo "Creating a minor version bump..."
	@$(UV) run semantic-release version --minor --no-vcs-release

version-patch:
	@echo "Creating a patch version bump..."
	@$(UV) run semantic-release version --patch --no-vcs-release

publish:
	@echo "Building distribution..."
	@$(UV) run hatch build
	@echo "To publish, you would typically use 'hatch publish' or 'twine upload dist/*'"

clean:
	@echo "Cleaning up build artifacts and cache..."
	@rm -rf dist/
	@rm -rf .pytest_cache/
	@rm -rf __pycache__/
	@find . -name "*.pyc" -exec rm -f {} +
	@find . -name "*.egg-info" -exec rm -rf {} +

# Documentation targets
docs-generate:
	@echo "🔄 Generating API documentation..."
	@$(UV) run python scripts/generate_docs.py

docs-serve:
	@echo "🌐 Starting documentation server..."
	@echo "   📚 Documentation: http://localhost:8000"
	@$(UV) run mkdocs serve

docs-build:
	@echo "🏗️ Building documentation..."
	@$(UV) run mkdocs build

docs-deploy:
	@echo "🚀 Deploying documentation to GitHub Pages..."
	@$(UV) run mkdocs gh-deploy

docs: docs-generate docs-build
	@echo "📚 Documentation built successfully!"
	@echo "   View at: ./site/index.html"
