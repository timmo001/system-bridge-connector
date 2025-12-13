"""Command Result."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CommandResult:
    """Command Result."""

    commandID: str  # noqa: N815  # pylint: disable=invalid-name
    exitCode: int  # noqa: N815  # pylint: disable=invalid-name
    stdout: str
    stderr: str
    error: str | None = None

