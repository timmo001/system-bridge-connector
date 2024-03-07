"""Test the const module."""

from systembridgeconnector.const import (
    EVENT_BASE,
    EVENT_DATA,
    SUBTYPE_BAD_TOKEN,
    TYPE_DATA_GET,
    TYPE_DATA_LISTENER_REGISTERED,
    TYPE_DATA_LISTENER_UNREGISTERED,
    TYPE_ERROR,
)


def test_const():
    """Test the const module."""
    assert EVENT_BASE == "base"
    assert EVENT_DATA == "data"
    assert SUBTYPE_BAD_TOKEN == "BAD_TOKEN"
    assert TYPE_DATA_GET == "DATA_GET"
    assert TYPE_DATA_LISTENER_REGISTERED == "DATA_LISTENER_REGISTERED"
    assert TYPE_DATA_LISTENER_UNREGISTERED == "DATA_LISTENER_UNREGISTERED"
    assert TYPE_ERROR == "ERROR"

