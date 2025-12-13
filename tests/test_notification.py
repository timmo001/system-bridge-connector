"""Test the OpenPath model."""

from dataclasses import asdict

from syrupy.assertion import SnapshotAssertion

from systembridgeconnector.models.fixtures.notification import FIXTURE_NOTIFICATION
from systembridgeconnector.models.notification import Notification


def test_notification(snapshot: SnapshotAssertion):
    """Test the notification."""
    notification = FIXTURE_NOTIFICATION
    assert isinstance(notification, Notification)
    assert notification == snapshot


def test_notification_dict(snapshot: SnapshotAssertion):
    """Test notification dict."""
    notification_dict = asdict(FIXTURE_NOTIFICATION)
    assert isinstance(notification_dict, dict)
    assert notification_dict == snapshot

    notification_converted = Notification(**notification_dict)
    assert isinstance(notification_converted, Notification)
    assert notification_converted == snapshot(
        name="notification-dict-converted",
    )
