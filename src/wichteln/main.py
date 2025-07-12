"""
This module contains the core logic for the Secret Santa application.
"""

import random
from typing import Any

class SecretSanta:
    """
    Manages the participants and assignments for a Secret Santa game.
    """

    def __init__(self) -> None:
        """
        Initializes a new Secret Santa game.
        
        Attributes:
            participants (list[dict[str, str]]): A list of dictionaries, where each dictionary represents a participant
                                                and contains their 'name' and 'email'.
            participant_emails (dict[str, str]): A dictionary mapping participant names to their email addresses.
            assignments (dict[str, str]): A dictionary mapping giver names to receiver names after assignments are made.
        """
        self.participants: list[dict[str, str]] = []
        self.participant_emails: dict[str, str] = {}
        self.assignments: dict[str, str] = {}

    def add_participant(self, name: str, email: str) -> None:
        """
        Adds a participant to the game if the name and email are valid and not already present.

        Args:
            name (str): The name of the participant to add.
            email (str): The email address of the participant.
        """
        if name and email and name not in self.participant_emails and email not in self.participant_emails.values():
            self.participants.append({'name': name, 'email': email})
            self.participant_emails[name] = email

    def assign_santas(self) -> None:
        """
        Assigns Secret Santas to all participants. Each participant is assigned to a different person.
        Assignments are stored in the `assignments` attribute.
        If there are fewer than two participants, no assignments are made.
        """
        if len(self.participants) < 2:
            return

        # Extract only names for shuffling
        participant_names = [p['name'] for p in self.participants]
        shuffled_participants = random.sample(participant_names, len(participant_names))

        self.assignments = {
            giver: shuffled_participants[(i + 1) % len(shuffled_participants)]
            for i, giver in enumerate(shuffled_participants)
        }

    def reset(self) -> None:
        """
        Resets the game to its initial state, clearing all participants and assignments.
        """
        self.participants = []
        self.assignments = {}
        self.participant_emails = {}
