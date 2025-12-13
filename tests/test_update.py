"""Test the update model."""

from pathlib import Path
import re

from syrupy.assertion import SnapshotAssertion

from systembridgeconnector.models.update import Update


def get_version() -> str:
    """Get version from setup.py."""
    project_root = Path(__file__).resolve().parents[1]
    setup_path = project_root / "setup.py"
    setup_contents = setup_path.read_text(encoding="utf-8")
    match = re.search(r'version="([^"]+)"', setup_contents)
    if not match:
        raise ValueError("version field not found in setup.py")
    return match.group(1)


def test_update(snapshot: SnapshotAssertion):
    """Test the update."""
    update = Update(
        version=get_version(),
    )
    assert isinstance(update, Update)
    assert update == snapshot
