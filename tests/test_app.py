"""
This module contains tests for the Flask application.
"""

import pytest
from app import app, game, pending_assignments
from unittest.mock import patch


@pytest.fixture
def client():
    """
    Creates a test client for the Flask application.
    """
    app.config["TESTING"] = True
    app.config["MAIL_SUPPRESS_SEND"] = (
        True  # Suppress actual email sending during tests
    )
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(autouse=True)
def reset_game_and_pending_assignments():
    """
    Resets the game state and pending assignments before each test.
    """
    game.reset()
    pending_assignments.clear()


@pytest.fixture
def mock_send_email():
    with patch("app.send_email") as mock_send:
        yield mock_send


@pytest.fixture
def mock_verify_recaptcha():
    with patch("app.verify_recaptcha") as mock_verify:
        mock_verify.return_value = True  # By default, assume reCAPTCHA passes
        yield mock_verify


def test_index(client):
    """
    Tests that the index page is rendered correctly.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Secret Santa" in response.data


def test_add_participant(client, mock_verify_recaptcha):
    """
    Tests that a participant is added to the game with name and email.
    """
    response = client.post(
        "/add",
        data={
            "name": "testuser",
            "email": "test@example.com",
            "g-recaptcha-response": "mock_token",
        },
    )
    assert response.status_code == 302  # Redirect to index
    assert game.participants[0]["name"] == "testuser"
    assert game.participants[0]["email"] == "test@example.com"
    mock_verify_recaptcha.assert_called_once_with("mock_token")


def test_add_participant_recaptcha_fail(client, mock_verify_recaptcha):
    """
    Tests that a participant is not added if reCAPTCHA fails.
    """
    mock_verify_recaptcha.return_value = False
    response = client.post(
        "/add",
        data={
            "name": "testuser",
            "email": "test@example.com",
            "g-recaptcha-response": "mock_token",
        },
    )
    assert response.status_code == 302  # Still redirects
    assert not game.participants  # Participant should not be added
    # Check that error message appears in the response
    assert b"CAPTCHA verification failed" in client.get("/").data


def test_assign_and_send_confirmation(client, mock_send_email, mock_verify_recaptcha):
    """
    Tests that assign triggers a confirmation email.
    """
    client.post(
        "/add",
        data={
            "name": "user1",
            "email": "user1@example.com",
            "g-recaptcha-response": "mock_token",
        },
    )
    client.post(
        "/add",
        data={
            "name": "user2",
            "email": "user2@example.com",
            "g-recaptcha-response": "mock_token",
        },
    )

    response = client.post("/assign", follow_redirects=True)
    assert response.status_code == 200  # Redirects to index
    mock_send_email.assert_called_once()  # Confirmation email should be sent
    assert len(pending_assignments) == 1  # Assignments should be pending
    assert b"Confirmation email sent" in response.data


def test_confirm_assignments(client, mock_send_email, mock_verify_recaptcha):
    """
    Tests that confirming assignments sends out emails to participants.
    """
    client.post(
        "/add",
        data={
            "name": "user1",
            "email": "user1@example.com",
            "g-recaptcha-response": "mock_token",
        },
    )
    client.post(
        "/add",
        data={
            "name": "user2",
            "email": "user2@example.com",
            "g-recaptcha-response": "mock_token",
        },
    )
    client.post("/assign")  # This populates pending_assignments

    # Get the token from pending_assignments (there should be only one)
    token = list(pending_assignments.keys())[0]

    response = client.get(f"/confirm/{token}", follow_redirects=True)
    assert response.status_code == 200  # Redirects to index
    assert not pending_assignments  # Pending assignments should be cleared
    assert mock_send_email.call_count == 3  # 1 confirmation + 2 participant emails
    assert b"Secret Santa assignments have been sent!" in response.data


def test_confirm_assignments_invalid_token(client):
    """
    Tests that an invalid token for confirmation is handled correctly.
    """
    response = client.get("/confirm/invalid_token", follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid or expired confirmation link." in response.data


def test_reset(client, mock_verify_recaptcha):
    """
    Tests that the game and pending assignments are reset correctly.
    """
    client.post(
        "/add",
        data={
            "name": "testuser",
            "email": "test@example.com",
            "g-recaptcha-response": "mock_token",
        },
    )
    client.post(
        "/add",
        data={
            "name": "user2",
            "email": "user2@example.com",
            "g-recaptcha-response": "mock_token",
        },
    )
    client.post("/assign")

    assert len(game.participants) > 0
    assert len(pending_assignments) > 0

    response = client.post("/reset", follow_redirects=True)
    assert response.status_code == 200
    assert not game.participants
    assert not pending_assignments
    assert b"Game has been reset." in response.data


def test_add_duplicate_participant_flask(client, mock_verify_recaptcha):
    """
    Tests that duplicate participants are not added via Flask app and proper error messages are shown.
    """
    # Add first participant
    response1 = client.post(
        "/add",
        data={
            "name": "testuser",
            "email": "test@example.com",
            "g-recaptcha-response": "mock_token",
        },
        follow_redirects=True,
    )
    assert response1.status_code == 200
    assert b"Successfully added testuser!" in response1.data
    assert len(game.participants) == 1

    # Try to add participant with same name, different email
    response2 = client.post(
        "/add",
        data={
            "name": "testuser",
            "email": "another@example.com",
            "g-recaptcha-response": "mock_token",
        },
        follow_redirects=True,
    )
    assert response2.status_code == 200
    assert (
        b"A participant with the name &#39;testuser&#39; was already added."
        in response2.data
    )
    assert len(game.participants) == 1  # Should still be 1

    # Try to add participant with different name, same email
    response3 = client.post(
        "/add",
        data={
            "name": "anotheruser",
            "email": "test@example.com",
            "g-recaptcha-response": "mock_token",
        },
        follow_redirects=True,
    )
    assert response3.status_code == 200
    assert (
        b"A participant with the email &#39;test@example.com&#39; was already added."
        in response3.data
    )
    assert len(game.participants) == 1  # Should still be 1
