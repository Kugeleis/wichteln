"""
This module contains tests for the Flask application.
"""

import pytest
from app import app, game

@pytest.fixture
def client():
    """
    Creates a test client for the Flask application.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_game():
    """
    Resets the game state before each test.
    """
    game.reset()

def test_index(client):
    """
    Tests that the index page is rendered correctly.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'Secret Santa' in response.data

def test_add_participant(client):
    """
    Tests that a participant is added to the game.
    """
    client.post('/add', data={'name': 'testuser'})
    response = client.get('/')
    assert b'testuser' in response.data

def test_assign(client):
    """
    Tests that Secret Santas are assigned correctly.
    """
    client.post('/add', data={'name': 'user1'})
    client.post('/add', data={'name': 'user2'})
    response = client.get('/assign', follow_redirects=True)
    assert response.status_code == 200
    assert b'Secret Santa Assignments' in response.data

def test_reset(client):
    """
    Tests that the game is reset correctly.
    """
    client.post('/add', data={'name': 'testuser'})
    client.post('/reset', follow_redirects=True)
    response = client.get('/')
    assert b'testuser' not in response.data