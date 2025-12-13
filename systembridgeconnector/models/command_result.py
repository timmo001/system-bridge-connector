"""Command Result."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CommandResult:
    """Command Result."""

    commandID: str
    exitCode: int
    stdout: str
    stderr: str
    error: str | None = None

