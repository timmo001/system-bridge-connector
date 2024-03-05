"""Setup for tests."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any

from aiohttp import ClientWebSocketResponse
from aiohttp.test_utils import TestClient

API_HOST = "localhost"
API_PORT = 9123
TOKEN = "abc123"

ClientSessionGenerator = Callable[..., Coroutine[Any, Any, TestClient]]

WebSocketGenerator = Callable[..., Coroutine[Any, Any, ClientWebSocketResponse]]
