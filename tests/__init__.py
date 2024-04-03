"""Setup for tests."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any, Final

from aiohttp import ClientWebSocketResponse
from aiohttp.test_utils import TestClient

API_HOST: Final[str] = "127.0.0.1"
API_PORT: Final[int] = 9170
REQUEST_ID: Final[str] = "test"
TOKEN: Final[str] = "abc123"
WEBSOCKET_PATH: Final[str] = "/api/websocket"


class MockClientWebSocket(ClientWebSocketResponse):
    """Protocol for a wrapped ClientWebSocketResponse."""

    client: TestClient


ClientSessionGenerator = Callable[..., Coroutine[Any, Any, TestClient]]

WebSocketGenerator = Callable[..., Coroutine[Any, Any, MockClientWebSocket]]
