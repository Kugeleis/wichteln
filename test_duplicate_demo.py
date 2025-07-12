#!/usr/bin/env python3
"""
Simple test script to demonstrate the duplicate prevention feature.
"""

from src.wichteln.main import SecretSanta


def test_duplicate_prevention():
    """Test the duplicate prevention feature."""
    game = SecretSanta()

    print("=== Testing Duplicate Prevention Feature ===\n")

    # Test 1: Add a valid participant
    print("1. Adding first participant:")
    success, message = game.add_participant("John Doe", "john@example.com")
    print(f"   Result: {success}")
    print(f"   Message: {message}")
    print(f"   Total participants: {len(game.participants)}\n")

    # Test 2: Try to add duplicate name
    print("2. Trying to add participant with same name:")
    success, message = game.add_participant("John Doe", "different@example.com")
    print(f"   Result: {success}")
    print(f"   Message: {message}")
    print(f"   Total participants: {len(game.participants)}\n")

    # Test 3: Try to add duplicate email
    print("3. Trying to add participant with same email:")
    success, message = game.add_participant("Jane Smith", "john@example.com")
    print(f"   Result: {success}")
    print(f"   Message: {message}")
    print(f"   Total participants: {len(game.participants)}\n")

    # Test 4: Add a valid different participant
    print("4. Adding second valid participant:")
    success, message = game.add_participant("Jane Smith", "jane@example.com")
    print(f"   Result: {success}")
    print(f"   Message: {message}")
    print(f"   Total participants: {len(game.participants)}\n")

    # Test 5: Try to add empty fields
    print("5. Trying to add participant with empty name:")
    success, message = game.add_participant("", "empty@example.com")
    print(f"   Result: {success}")
    print(f"   Message: {message}")
    print(f"   Total participants: {len(game.participants)}\n")

    print("=== Final participant list ===")
    for i, participant in enumerate(game.participants, 1):
        print(f"{i}. {participant['name']} ({participant['email']})")


if __name__ == "__main__":
    test_duplicate_prevention()
