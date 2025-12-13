"""Media Files."""
from __future__ import annotations

from dataclasses import dataclass
from typing import cast


@dataclass(slots=True)
class MediaFile:
    """Media File."""

    name: str
    path: str
    fullpath: str
    size: int
    last_accessed: float
    created: float
    modified: float
    is_directory: bool
    is_file: bool
    is_link: bool
    mime_type: str | None = None


@dataclass(slots=True)
class MediaFiles:
    """Media Files."""

    files: list[MediaFile]
    path: str

    def __post_init__(self) -> None:
        """Post Init."""
        if isinstance(self.files, list) and all(
            isinstance(item, dict) for item in self.files
        ):
            new_files: list[MediaFile] = []
            for f in self.files:
                file: dict = cast(dict, f)
                new_files.append(MediaFile(**file))
            self.files = new_files

