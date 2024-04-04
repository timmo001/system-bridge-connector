"""Test the const module."""

from syrupy.assertion import SnapshotAssertion

from systembridgeconnector.const import (
    EventKey,
    EventSubType,
    EventType,
    QueryParameter,
)


def test_query_parameter(snapshot: SnapshotAssertion):
    """Test query parameter."""
    assert QueryParameter == snapshot


def test_event_key(snapshot: SnapshotAssertion):
    """Test event key."""
    assert EventKey == snapshot


def test_event_type(snapshot: SnapshotAssertion):
    """Test event type."""
    assert EventType == snapshot


def test_event_subtype(snapshot: SnapshotAssertion):
    """Test event subtype."""
    assert EventSubType == snapshot
