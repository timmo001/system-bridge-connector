"""Notification."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast


@dataclass(slots=True)
class Action:
    """Notification Action."""

    command: str
    label: str
    data: dict[str, Any] | None = None


@dataclass(slots=True)
class Audio:
    """Notification Audio."""

    source: str
    volume: float | None = None


@dataclass(slots=True)
class Notification:
    """Notification."""

    title: str
    message: str | None = None
    icon: str | None = None
    image: str | None = None
    actions: list[Action] | None = None
    timeout: float | None = None
    audio: Audio | None = None

    def __post_init__(self):
        """Post init."""
        if isinstance(self.actions, list) and all(
            isinstance(item, dict) for item in self.actions
        ):
            new_actions: list[Action] = []
            for a in self.actions:
                action = cast(dict, a)
                new_actions.append(Action(**action))
            self.actions = new_actions

        if isinstance(self.audio, dict):
            audio = cast(dict, self.audio)
            self.audio = Audio(**audio)

