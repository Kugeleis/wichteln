"""
DEPRECATED: This test file has been split into separate modules.

This monolithic test file has been reorganized into focused test files:

- tests/test_validators.py - Tests for services/validators.py functions
- tests/test_email_templates.py - Tests for services/email_templates.py functions
- tests/test_token_manager.py - Tests for services/token_manager.py functions
- tests/test_email_service_integration.py - Tests for services/email_service.py integration

Please use the individual test files instead of this one.
See docs/SINGLE_RESPONSIBILITY_TEST_ORGANIZATION.md for details.

This file is kept for reference but should not be used for new development.
"""

import pytest


def test_deprecated_notice():
    """Test to indicate this file has been deprecated."""
    pytest.skip(
        "This test file has been split into separate modules. See docs/SINGLE_RESPONSIBILITY_TEST_ORGANIZATION.md"
    )
