# Python Best Practices for this Project

This document outlines the recommended best practices for Python development within this project. Adhering to these guidelines ensures code quality, maintainability, and consistency.

## 1. Typing (Type Hints)

All new Python code should utilize type hints (PEP 484) for function arguments, return values, and variables. This improves code readability, enables static analysis, and helps catch errors early.

**Example:**

```python
def calculate_sum(a: int, b: int) -> int:
    """Calculates the sum of two integers."""
    return a + b

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
```

Run `mypy` regularly to check type consistency:
```bash
python -m mypy src/
```

## 2. Pytest for Testing

`pytest` is the preferred testing framework. Write comprehensive unit and integration tests for all new features and bug fixes.

*   Place test files in the `tests/` directory.
*   Name test files `test_*.py` or `*_test.py`.
*   Name test functions `test_*`.
*   Use `assert` statements for assertions.

**Example (`tests/test_example.py`):**

```python
import pytest
from src.wichteln.main import some_function # Example import

def test_some_function_returns_expected_value():
    assert some_function(2, 3) == 5

def test_some_function_handles_negative_numbers():
    assert some_function(-1, 1) == 0
```

Run tests using:
```bash
pytest
```

## 3. `uv` as Package Manager

`uv` is used for dependency management. Use `uv` for installing, updating, and managing project dependencies.

*   Install dependencies:
    ```bash
    uv pip install -r requirements.txt
    ```
*   Add a new dependency:
    ```bash
    uv pip install <package-name>
    ```
*   Update dependencies:
    ```bash
    uv pip install --upgrade <package-name>
    ```
*   Sync dependencies with `uv.lock`:
    ```bash
    uv pip sync
    ```

## 4. Reduce Coupling

Design components to be as independent as possible. High coupling makes code harder to understand, test, and maintain.

*   **Dependency Injection:** Pass dependencies into classes/functions rather than having them create or directly import them.
*   **Clear Interfaces:** Define clear and minimal interfaces for modules and classes.
*   **Avoid Global State:** Minimize the use of global variables.

## 5. DRY (Don't Repeat Yourself) Principle

Avoid duplicating code. If you find yourself writing the same logic more than once, abstract it into a reusable function, class, or module.

*   **Functions/Methods:** Encapsulate common operations.
*   **Classes:** Use inheritance or composition for shared behavior.
*   **Utility Modules:** Create modules for common helper functions.

## 6. Docstrings

All modules, classes, methods, and functions should have clear and concise docstrings (PEP 257). Use reStructuredText or Google style for formatting.

**Example (Google Style):**

```python
def greet(name: str) -> str:
    """Greets a person by their name.

    Args:
        name: The name of the person to greet.

    Returns:
        A greeting string.
    """
    return f"Hello, {name}!"


class Calculator:
    """A simple calculator class.

    Attributes:
        history: A list of operations performed.
    """
    def __init__(self):
        self.history = []

    def add(self, a: float, b: float) -> float:
        """Adds two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The sum of a and b.
        """
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
```
