"""Fixture for media files."""
from systembridgeconnector.models.media_files import MediaFile, MediaFiles

FIXTURE_MEDIA_FILES = MediaFiles(
    files=[
        MediaFile(
            name="file1",
            path="path/to/file1",
            fullpath="/full/path/to/file1",
            size=100,
            last_accessed=100.0,
            created=100.0,
            modified=100.0,
            is_directory=False,
            is_file=True,
            is_link=False,
            mime_type="text/plain",
        ),
    ],
    path="path/to/file",
)
