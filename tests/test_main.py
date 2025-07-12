"""
This module contains tests for the SecretSanta class.
"""

from src.wichteln.main import SecretSanta


def test_add_participant():
    """
    Tests that a participant is added to the game with name and email.
    """
    game = SecretSanta()
    game.add_participant("testuser", "test@example.com")
    assert len(game.participants) == 1
    assert game.participants[0]["name"] == "testuser"
    assert game.participants[0]["email"] == "test@example.com"
    assert game.participant_emails["testuser"] == "test@example.com"


def test_add_duplicate_participant():
    """
    Tests that duplicate participants are not added.
    """
    game = SecretSanta()
    game.add_participant("testuser", "test@example.com")
    game.add_participant(
        "testuser", "another@example.com"
    )  # Same name, different email
    game.add_participant(
        "anotheruser", "test@example.com"
    )  # Different name, same email
    assert len(game.participants) == 1


def test_assign_santas():
    """
    Tests that Secret Santas are assigned correctly.
    """
    game = SecretSanta()
    game.add_participant("user1", "user1@example.com")
    game.add_participant("user2", "user2@example.com")
    game.add_participant("user3", "user3@example.com")
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
    game.add_participant("user1", "user1@example.com")
    game.assign_santas()
    assert not game.assignments


def test_reset():
    """
    Tests that the game is reset correctly.
    """
    game = SecretSanta()
    game.add_participant("testuser", "test@example.com")
    game.assign_santas()
    game.reset()
    assert not game.participants
    assert not game.assignments
    assert not game.participant_emails
