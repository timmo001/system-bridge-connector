"""Test the websocket client module."""

import asyncio
from typing import Any
from unittest.mock import patch

from aiohttp import web
import pytest

from systembridgeconnector.websocket_client import WebSocketClient
from systembridgemodels.response import Response

from . import API_HOST, API_PORT, TOKEN, ClientSessionGenerator


async def _websocket_response(
    request: web.Request,
    response: Response | None = None,
) -> web.WebSocketResponse:
    """Return a websocket response."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    if response is not None:
        await ws.send_json(response)
    await ws.close()
    return ws


async def _websocket_alive_response(request: web.Request) -> web.WebSocketResponse:
    """Return a websocket response."""
    return await _websocket_response(
        request,
        Response(
            id="test",
            type="TEST",
            data={"test": "test"},
        ),
    )


async def _get_websocket_client(
    aiohttp_client: ClientSessionGenerator,
) -> WebSocketClient:
    """Return a websocket client."""
    app = web.Application()

    # Add websocket route at /api/websocket
    app.router.add_get("/api/websocket", _websocket_response)

    client = await aiohttp_client(
        app,
        server_kwargs={
            "port": API_PORT,
        },
    )

    websocket_client = WebSocketClient(
        API_HOST,
        API_PORT,
        TOKEN,
    )

    await websocket_client.connect(session=client.session)

    return websocket_client


@pytest.mark.asyncio
async def test_close(aiohttp_client: ClientSessionGenerator):
    """Test close."""
    websocket_client = await _get_websocket_client(aiohttp_client)
    assert websocket_client.connected is True

    await websocket_client.close()
    assert websocket_client.connected is False
