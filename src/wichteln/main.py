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
        self.participants: List[str] = []
        self.assignments: Dict[str, str] = {}

    def add_participant(self, name: str) -> None:
        """
        Adds a participant to the game.

        Args:
            name: The name of the participant to add.
        """
        if name and name not in self.participants:
            self.participants.append(name)

    def assign_santas(self) -> None:
        """
        Assigns Secret Santas to all participants.
        """
        if len(self.participants) < 2:
            return

        shuffled_participants = random.sample(self.participants, len(self.participants))
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
