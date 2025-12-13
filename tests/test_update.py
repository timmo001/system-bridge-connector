"""Test the update model."""

from syrupy.assertion import SnapshotAssertion

from systembridgeconnector._version import __version__
from systembridgeconnector.models.update import Update


def test_update(snapshot: SnapshotAssertion):
    """Test the update."""
    update = Update(
        version=__version__.public(),
    )
    assert isinstance(update, Update)
    assert update == snapshot
