"""Command Result."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CommandResult:
    """Command Result."""

    commandID: str  # noqa: N815
    exitCode: int  # noqa: N815
    stdout: str
    stderr: str
    error: str | None = None

