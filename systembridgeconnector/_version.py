"""Version shims for backward compatibility.

Expose ``__version__`` as a string using importlib.metadata to avoid
runtime dependency on incremental.
"""

from __future__ import annotations

try:  # Python 3.11+
    from importlib.metadata import PackageNotFoundError, version as get_version
except Exception:  # pragma: no cover - very old python not supported in runtime
    PackageNotFoundError = Exception  # type: ignore[assignment]
    def get_version(_: str) -> str:  # type: ignore[no-redef]
        raise PackageNotFoundError

PACKAGE_NAME = "systembridgeconnector"

try:
    __version__: str = get_version(PACKAGE_NAME)
except PackageNotFoundError:  # pragma: no cover - fallback for editable installs
    __version__ = "0.0.0"

__all__ = ["__version__"]
