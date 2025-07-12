"""
This module contains tests for the SecretSanta class.
"""

from src.wichteln.main import SecretSanta


def test_add_participant():
    """
    Tests that a participant is added to the game with name and email.
    """
    game = SecretSanta()
    success, message = game.add_participant("testuser", "test@example.com")
    assert success is True
    assert "Successfully added testuser!" in message
    assert len(game.participants) == 1
    assert game.participants[0]["name"] == "testuser"
    assert game.participants[0]["email"] == "test@example.com"
    assert game.participant_emails["testuser"] == "test@example.com"


def test_add_duplicate_participant():
    """
    Tests that duplicate participants are not added.
    """
    game = SecretSanta()
    success1, message1 = game.add_participant("testuser", "test@example.com")
    assert success1 is True

    # Try to add same name, different email
    success2, message2 = game.add_participant("testuser", "another@example.com")
    assert success2 is False
    assert "A participant with the name 'testuser' was already added." in message2

    # Try to add different name, same email
    success3, message3 = game.add_participant("anotheruser", "test@example.com")
    assert success3 is False
    assert (
        "A participant with the email 'test@example.com' was already added." in message3
    )

    assert len(game.participants) == 1


def test_add_participant_empty_fields():
    """
    Tests that participants with empty name or email are not added.
    """
    game = SecretSanta()

    # Empty name
    success1, message1 = game.add_participant("", "test@example.com")
    assert success1 is False
    assert "Name and email are required." in message1

    # Empty email
    success2, message2 = game.add_participant("testuser", "")
    assert success2 is False
    assert "Name and email are required." in message2

    # Both empty
    success3, message3 = game.add_participant("", "")
    assert success3 is False
    assert "Name and email are required." in message3

    assert len(game.participants) == 0


def test_assign_santas():
    """
    Tests that Secret Santas are assigned correctly.
    """
    game = SecretSanta()
    game.add_participant(
        "user1", "user1@example.com"
    )  # Ignore return value for this test
    game.add_participant(
        "user2", "user2@example.com"
    )  # Ignore return value for this test
    game.add_participant(
        "user3", "user3@example.com"
    )  # Ignore return value for this test
    game.assign_santas()
    assert len(game.assignments) == 3
    assert "user1" in game.assignments
    assert "user2" in game.assignments
    assert "user3" in game.assignments
    for giver, receiver in game.assignments.items():
        assert giver != receiver  # A person cannot be their own Secret Santa
        assert receiver in [
            p["name"] for p in game.participants
        ]  # Receiver is a valid participant


def test_assign_santas_not_enough_participants():
    """
    Tests that assign_santas does nothing if there are less than 2 participants.
    """
    game = SecretSanta()
    game.add_participant(
        "user1", "user1@example.com"
    )  # Ignore return value for this test
    game.assign_santas()
    assert not game.assignments


def test_reset():
    """
    Tests that the game is reset correctly.
    """
    game = SecretSanta()
    game.add_participant(
        "testuser", "test@example.com"
    )  # Ignore return value for this test
    game.assign_santas()
    game.reset()
    assert not game.participants
    assert not game.assignments
    assert not game.participant_emails


def test_reset_clears_all_data():
    """Test that reset() properly clears all game data."""
    game = SecretSanta()

    # Add some participants
    game.add_participant("Alice", "alice@example.com")
    game.add_participant("Bob", "bob@example.com")

    # Assign participants
    game.assign_santas()

    # Verify data exists
    assert len(game.participants) > 0
    assert len(game.assignments) > 0
    assert len(game.participant_emails) > 0

    # Reset the game
    game.reset()

    # Verify all data is cleared
    assert game.participants == []
    assert game.assignments == {}
    assert game.participant_emails == {}
