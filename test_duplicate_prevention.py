#!/usr/bin/env python3
"""
Test script to demonstrate the duplicate prevention functionality.
"""

import requests

# Base URL for the Flask app
BASE_URL = "http://127.0.0.1:5000"


def test_duplicate_prevention():
    """Test the duplicate prevention feature."""
    print("🎄 Testing Secret Santa Duplicate Prevention Feature")
    print("=" * 50)

    # Reset the game first
    print("1. Resetting the game...")
    response = requests.post(f"{BASE_URL}/reset", timeout=10)
    if response.status_code == 200:
        print("   ✅ Game reset successfully")
    else:
        print("   ❌ Failed to reset game")
        return

    # Add first participant
    print("\n2. Adding first participant (John, john@example.com)...")
    data = {
        "name": "John",
        "email": "john@example.com",
        "g-recaptcha-response": "dummy_token",
    }
    response = requests.post(f"{BASE_URL}/add", data=data, timeout=10)
    if response.status_code == 200:
        print("   ✅ First participant added successfully")
    else:
        print("   ❌ Failed to add first participant")
        return

    # Try to add duplicate name with different email
    print(
        "\n3. Trying to add duplicate name with different email (John, john2@example.com)..."
    )
    data = {
        "name": "John",
        "email": "john2@example.com",
        "g-recaptcha-response": "dummy_token",
    }
    response = requests.post(
        f"{BASE_URL}/add", data=data, allow_redirects=False, timeout=10
    )
    if "was already added" in response.text or response.status_code == 302:
        print("   ✅ Duplicate name correctly rejected")
    else:
        print("   ❌ Duplicate name was not rejected")

    # Try to add different name with duplicate email
    print(
        "\n4. Trying to add different name with duplicate email (Jane, john@example.com)..."
    )
    data = {
        "name": "Jane",
        "email": "john@example.com",
        "g-recaptcha-response": "dummy_token",
    }
    response = requests.post(
        f"{BASE_URL}/add", data=data, allow_redirects=False, timeout=10
    )
    if "was already added" in response.text or response.status_code == 302:
        print("   ✅ Duplicate email correctly rejected")
    else:
        print("   ❌ Duplicate email was not rejected")

    # Add a valid second participant
    print("\n5. Adding valid second participant (Jane, jane@example.com)...")
    data = {
        "name": "Jane",
        "email": "jane@example.com",
        "g-recaptcha-response": "dummy_token",
    }
    response = requests.post(f"{BASE_URL}/add", data=data, timeout=10)
    if response.status_code == 200:
        print("   ✅ Second participant added successfully")
    else:
        print("   ❌ Failed to add second participant")

    print("\n🎉 Duplicate prevention test completed!")
    print("\nYou can now check the web interface at http://127.0.0.1:5000")
    print("to see the red error messages when trying to add duplicates.")


if __name__ == "__main__":
    try:
        test_duplicate_prevention()
    except requests.exceptions.ConnectionError:
        print(
            "❌ Could not connect to the Flask app. Make sure it's running on http://127.0.0.1:5000"
        )
    except Exception as e:
        print(f"❌ An error occurred: {e}")
