PYTHON := .venv/Scripts/python.exe
UV := .venv/Scripts/uv.exe

.PHONY: all run test update publish clean

all: run

run:
	@echo "Starting Flask development server..."
	@$(PYTHON) app.py

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
