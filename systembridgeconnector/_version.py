"""Version shims for backward compatibility.

Expose ``__version__`` as a string using importlib.metadata to avoid
runtime dependency on incremental.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as get_version

PACKAGE_NAME = "systembridgeconnector"

try:
    __version__: str = get_version(PACKAGE_NAME)
except PackageNotFoundError:  # pragma: no cover - fallback for editable installs
    __version__ = "0.0.0"

__all__ = ["__version__"]
