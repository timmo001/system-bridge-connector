"""Command Execute."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CommandExecute:
    """Command Execute."""

    commandID: str

