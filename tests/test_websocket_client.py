"""Test the websocket client module."""

from unittest.mock import patch

import aiohttp
from aiohttp import web
import pytest

from systembridgeconnector.const import EVENT_MODULES, TYPE_DATA_GET, TYPE_DIRECTORIES
from systembridgeconnector.exceptions import ConnectionErrorException
from systembridgeconnector.websocket_client import WebSocketClient
from systembridgemodels.const import MODEL_SYSTEM
from systembridgemodels.keyboard_key import KeyboardKey
from systembridgemodels.keyboard_text import KeyboardText
from systembridgemodels.media_control import MediaControl
from systembridgemodels.media_directories import MediaDirectory
from systembridgemodels.media_files import MediaFile, MediaFiles
from systembridgemodels.media_get_file import MediaGetFile
from systembridgemodels.media_get_files import MediaGetFiles
from systembridgemodels.modules import GetData, RegisterDataListener
from systembridgemodels.notification import Notification
from systembridgemodels.open_path import OpenPath
from systembridgemodels.open_url import OpenUrl
from systembridgemodels.request import Request
from systembridgemodels.response import Response
from systembridgemodels.update import Update

from . import API_HOST, API_PORT, TOKEN, ClientSessionGenerator

REQUEST_ID = "test"


async def _websocket_response(
    request: web.Request,
    response: Response,
) -> web.WebSocketResponse:
    """Return a websocket response."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("websocket_response", response)
    await ws.send_json(response)
    await ws.close()
    return ws


async def _get_websocket_client(
    aiohttp_client: ClientSessionGenerator,
    response: Response = Response(
        id=REQUEST_ID,
        type="TEST",
        data={"test": "test"},
    ),
) -> WebSocketClient:
    """Return a websocket client."""
    app = web.Application()

    # Add websocket route at /api/websocket
    app.router.add_get(
        "/api/websocket",
        lambda request: _websocket_response(
            request,
            response,
        ),
    )

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


@pytest.mark.asyncio
async def test_application_update(aiohttp_client: ClientSessionGenerator):
    """Test application update."""
    websocket_client = await _get_websocket_client(aiohttp_client)
    response = await websocket_client.application_update(
        Update(
            version="0.0.0",
        )
    )
    assert isinstance(response, Response)
    assert response.type == "N/A"
    assert response.data == {}


@pytest.mark.asyncio
async def test_exit_backend(aiohttp_client: ClientSessionGenerator):
    """Test exit backend."""
    websocket_client = await _get_websocket_client(aiohttp_client)
    response = await websocket_client.exit_backend(
        request_id=REQUEST_ID,
    )
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == "N/A"
    assert response.data == {}


@pytest.mark.asyncio
async def test_get_data(aiohttp_client: ClientSessionGenerator):
    """Test get data."""
    websocket_client = await _get_websocket_client(
        aiohttp_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_DATA_GET,
            data={EVENT_MODULES: [MODEL_SYSTEM]},
        ),
    )
    response = await websocket_client.get_data(
        GetData(
            modules=[MODEL_SYSTEM],
        ),
        request_id=REQUEST_ID,
    )
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == "N/A"
    assert response.data == {}


@pytest.mark.asyncio
async def test_get_directories(aiohttp_client: ClientSessionGenerator):
    """Test get directories."""
    websocket_client = await _get_websocket_client(
        aiohttp_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_DIRECTORIES,
            data=[{"key": "documents", "path": "/documents"}],
        ),
    )
    response = await websocket_client.get_directories(
        request_id=REQUEST_ID,
    )
    # assert isinstance(response, list)
    # assert len(response) == 1
    # assert isinstance(response[0], MediaDirectory)
    # assert response[0].key == "documents"
    # assert response[0].path == "/documents"


@pytest.mark.asyncio
async def test_connection_error(aiohttp_client: ClientSessionGenerator):
    """Test connection error."""
    app = web.Application()

    _ = await aiohttp_client(
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

    with patch(
        "aiohttp.ClientSession.ws_connect",
        side_effect=aiohttp.ClientConnectionError,
    ), pytest.raises(ConnectionErrorException):
        await websocket_client.connect()
