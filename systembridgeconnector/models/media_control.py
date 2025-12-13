"""Media Control."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class MediaAction(Enum):
    """Media Action."""

    PLAY = "PLAY"
    PAUSE = "PAUSE"
    STOP = "STOP"
    PREVIOUS = "PREVIOUS"
    NEXT = "NEXT"
    SEEK = "SEEK"
    REWIND = "REWIND"
    FASTFORWARD = "FASTFORWARD"
    SHUFFLE = "SHUFFLE"
    REPEAT = "REPEAT"
    MUTE = "MUTE"
    VOLUMEDOWN = "VOLUMEDOWN"
    VOLUMEUP = "VOLUMEUP"


@dataclass(slots=True)
class MediaControl:
    """Media Control."""

    action: str
    value: Any | None = None

