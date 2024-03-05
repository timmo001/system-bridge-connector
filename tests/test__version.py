"""Test base module."""

from systembridgeconnector._version import __version__


def test__version():
    """Test the version string."""
    assert isinstance(__version__.public(), str)
