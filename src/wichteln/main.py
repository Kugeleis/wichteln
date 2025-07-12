"""
This module contains the core logic for the Secret Santa application.
"""

import random
from typing import List, Dict

class SecretSanta:
    """
    Manages the participants and assignments for a Secret Santa game.
    """

    def __init__(self) -> None:
        """
        Initializes a new Secret Santa game.
        """
        self.participants: List[Dict[str, str]] = []
        self.participant_emails: Dict[str, str] = {}
        self.assignments: Dict[str, str] = {}

    def add_participant(self, name: str, email: str) -> None:
        """
        Adds a participant to the game.

        Args:
            name: The name of the participant to add.
            email: The email address of the participant.
        """
        if name and email and name not in self.participant_emails and email not in self.participant_emails.values():
            self.participants.append({'name': name, 'email': email})
            self.participant_emails[name] = email

    def assign_santas(self) -> None:
        """
        Assigns Secret Santas to all participants.
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
        Resets the game to its initial state.
        """
        self.participants = []
        self.assignments = {}
        self.participant_emails = {}
