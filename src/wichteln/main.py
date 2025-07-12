"""
This module contains the core logic for the Secret Santa application.
"""

import random


class SecretSanta:
    """
    Manages the participants and assignments for a Secret Santa game.
    """

    def __init__(self) -> None:
        """
        Initializes a new Secret Santa game.

        Attributes:
            participants (list[dict[str, str | bool]]): A list of dictionaries, where each dictionary represents a participant
                                                and contains their 'name', 'email', and 'is_admin'.
            participant_emails (dict[str, str]): A dictionary mapping participant names to their email addresses.
            assignments (dict[str, str]): A dictionary mapping giver names to receiver names after assignments are made.
        """
        self.participants: list[dict[str, str | bool]] = []
        self.participant_emails: dict[str, str] = {}
        self.assignments: dict[str, str] = {}

    def add_participant(self, name: str, email: str) -> tuple[bool, str]:
        """
        Adds a participant to the game if the name and email are valid and not already present.

        Args:
            name (str): The name of the participant to add.
            email (str): The email address of the participant.

        Returns:
            tuple[bool, str]: A tuple containing success status and message.
                             (True, "Success message") if added successfully,
                             (False, "Error message") if addition failed.
        """
        if not name or not email:
            return False, "Name and email are required."

        # Check for duplicate name
        if name in self.participant_emails:
            return False, f"A participant with the name '{name}' was already added."

        # Check for duplicate email
        if email in self.participant_emails.values():
            return False, f"A participant with the email '{email}' was already added."

        # If we get here, both name and email are unique
        # The first participant becomes the administrator
        is_admin = len(self.participants) == 0
        self.participants.append({"name": name, "email": email, "is_admin": is_admin})
        self.participant_emails[name] = email

        admin_msg = " (Administrator)" if is_admin else ""
        return True, f"Successfully added {name}{admin_msg}!"

    def assign_santas(self) -> None:
        """
        Assigns Secret Santas to all participants. Each participant is assigned to a different person.
        Assignments are stored in the `assignments` attribute.
        If there are fewer than two participants, no assignments are made.
        """
        if len(self.participants) < 2:
            return

        # Extract only names for shuffling
        participant_names = [str(p["name"]) for p in self.participants]
        shuffled_participants = random.sample(participant_names, len(participant_names))

        self.assignments = {
            giver: shuffled_participants[(i + 1) % len(shuffled_participants)]
            for i, giver in enumerate(shuffled_participants)
        }

    def clear_participants(self) -> None:
        """
        Clears participants list while keeping assignments intact.

        This is useful after assignments have been sent to maintain secrecy
        while preserving the record that assignments were made.
        """
        self.participants = []
        self.participant_emails = {}

    def remove_participant(self, name: str) -> tuple[bool, str]:
        """
        Removes a participant from the game by name.

        Args:
            name (str): The name of the participant to remove.

        Returns:
            tuple[bool, str]: A tuple containing success status and message.
                             (True, "Success message") if removed successfully,
                             (False, "Error message") if removal failed.
        """
        if not name:
            return False, "Name is required."

        # Check if participant exists
        if name not in self.participant_emails:
            return False, f"Participant '{name}' not found."

        # Remove from participants list
        self.participants = [p for p in self.participants if str(p["name"]) != name]

        # Remove from participant_emails dict
        del self.participant_emails[name]

        # Clear assignments if they exist (assignments become invalid when participants change)
        if self.assignments:
            self.assignments = {}

        return True, f"Successfully removed {name}!"

    def reset(self) -> None:
        """
        Resets the game to its initial state, clearing all participants and assignments.
        """
        self.participants = []
        self.assignments = {}
        self.participant_emails = {}
