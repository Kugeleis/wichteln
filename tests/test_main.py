"""
This module contains tests for the SecretSanta class.
"""

from src.wichteln.main import SecretSanta

def test_add_participant():
    """
    Tests that a participant is added to the game.
    """
    game = SecretSanta()
    game.add_participant('testuser')
    assert 'testuser' in game.participants

def test_assign_santas():
    """
    Tests that Secret Santas are assigned correctly.
    """
    game = SecretSanta()
    game.add_participant('user1')
    game.add_participant('user2')
    game.assign_santas()
    assert len(game.assignments) == 2
    assert 'user1' in game.assignments
    assert 'user2' in game.assignments
    assert game.assignments['user1'] != 'user1'
    assert game.assignments['user2'] != 'user2'

def test_reset():
    """
    Tests that the game is reset correctly.
    """
    game = SecretSanta()
    game.add_participant('testuser')
    game.assign_santas()
    game.reset()
    assert not game.participants
    assert not game.assignments
