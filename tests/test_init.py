"""Test base module."""

from systembridgeconnector._version import __version__


def test_version():
    """Test the version string."""
    assert isinstance(__version__.public(), str)
