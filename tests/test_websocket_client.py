"""Test the websocket client module."""

from systembridgeconnector.websocket_client import WebSocketClient

from . import API_HOST, API_PORT, TOKEN


def test_websocket_client():
    """Test the websocket client module."""
    client = WebSocketClient(
        API_HOST,
        API_PORT,
        TOKEN,
    )
