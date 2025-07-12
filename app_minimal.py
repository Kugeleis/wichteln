"""
Main application entry point for the Secret Santa web interface.

This is the refactored version that uses modular components.
"""

import os
from services.app_factory import create_complete_app

# Create the app with all services and routes configured
app = create_complete_app()

if __name__ == "__main__":
    # Only enable debug mode in development environment
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "on", "1"]
    app.run(debug=debug_mode)
# This is a test comment for automated versioning.
