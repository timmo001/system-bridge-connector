"""Setup for tests."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any, Final

from aiohttp import web
from aiohttp.test_utils import TestClient

API_HOST: Final[str] = "127.0.0.1"
API_PORT: Final[int] = 9170
REQUEST_ID: Final[str] = "test"
TOKEN: Final[str] = "abc123"
WEBSOCKET_PATH: Final[str] = "/api/websocket"

ClientSessionGenerator = Callable[..., Coroutine[Any, Any, TestClient]]


async def bad_request_response(_: web.Request):
    """Return a bad request response."""
    return web.json_response(
        {"test": "test"},
        status=400,
    )


async def json_response(_: web.Request):
    """Return a json response."""
    return web.json_response({"test": "test"})


async def text_response(_: web.Request):
    """Return a text response."""
    return web.Response(text="test")


async def unauthorised_response(_: web.Request):
    """Return an unauthorised response."""
    return web.json_response(
        {"test": "test"},
        status=401,
    )
