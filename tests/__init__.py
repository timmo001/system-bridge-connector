"""Setup for tests."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any, Final

from aiohttp import ClientWebSocketResponse
from aiohttp.test_utils import TestClient

API_HOST: Final[str] = "localhost"
API_PORT: Final[int] = 9123
REQUEST_ID: Final[str] = "test"
TOKEN: Final[str] = "abc123"
WEBSOCKET_PATH: Final[str] = "/api/websocket"


ClientSessionGenerator = Callable[..., Coroutine[Any, Any, TestClient]]

WebSocketGenerator = Callable[..., Coroutine[Any, Any, ClientWebSocketResponse]]
