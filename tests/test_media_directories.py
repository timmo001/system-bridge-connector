"""Test the media_directories model."""

from syrupy.assertion import SnapshotAssertion

from systembridgeconnector.models.media_directories import MediaDirectory


def test_media_directories(snapshot: SnapshotAssertion):
    """Test the media_directories."""
    media_directories = [
        MediaDirectory(
            key="music",
            path="path/to/file",
        )
    ]
    assert isinstance(media_directories, list)
    assert isinstance(media_directories[0], MediaDirectory)
    assert media_directories == snapshot
