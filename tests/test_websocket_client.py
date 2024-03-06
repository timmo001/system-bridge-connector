"""Test the websocket client module."""

import asyncio
import concurrent.futures
from typing import Any, Final
from unittest.mock import patch

import aiohttp
from aiohttp import ClientWebSocketResponse, web
from attr import asdict
import pytest

from systembridgeconnector.const import (
    EVENT_MODULES,
    TYPE_DATA_GET,
    TYPE_DIRECTORIES,
    TYPE_FILES,
)
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

from . import API_HOST, API_PORT, REQUEST_ID, TOKEN, WebSocketGenerator

base_response = Response(
    id=REQUEST_ID,
    type="TEST",
    data={"test": "test"},
)


async def _get_websocket_client(
    ws_client: WebSocketGenerator,
    response: Response,
) -> WebSocketClient:
    """Return a websocket client."""
    ws = await ws_client(response=response)

    websocket_client = WebSocketClient(
        API_HOST,
        API_PORT,
        TOKEN,
        session=ws.client.session,
        websocket=ws,
    )

    # Run the listener in the background
    asyncio.get_event_loop().create_task(
        websocket_client.listen(callback=None),
        name="WebSocket Listener",
    )

    return websocket_client


@pytest.mark.asyncio
async def test_connection_error(ws_client: WebSocketGenerator):
    """Test connection error."""
    websocket_client = await _get_websocket_client(ws_client, base_response)

    with patch(
        "aiohttp.ClientSession.ws_connect",
        side_effect=aiohttp.ClientConnectionError,
    ), pytest.raises(ConnectionErrorException):
        await websocket_client.connect()


@pytest.mark.asyncio
async def test_close(ws_client: WebSocketGenerator):
    """Test close."""
    websocket_client = await _get_websocket_client(ws_client, base_response)
    assert websocket_client.connected is True

    await websocket_client.close()
    assert websocket_client.connected is False


@pytest.mark.asyncio
async def test_application_update(ws_client: WebSocketGenerator):
    """Test application update."""
    websocket_client = await _get_websocket_client(ws_client, base_response)
    assert websocket_client.connected is True
    response = await websocket_client.application_update(
        Update(
            version="0.0.0",
        )
    )
    assert isinstance(response, Response)
    assert response.type == "N/A"
    assert response.data == {}


@pytest.mark.asyncio
async def test_exit_backend(ws_client: WebSocketGenerator):
    """Test exit backend."""
    websocket_client = await _get_websocket_client(ws_client, base_response)
    assert websocket_client.connected is True
    response = await websocket_client.exit_backend(
        request_id=REQUEST_ID,
    )
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == "N/A"
    assert response.data == {}


@pytest.mark.asyncio
async def test_get_data(ws_client: WebSocketGenerator):
    """Test get data."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_DATA_GET,
            data={EVENT_MODULES: [MODEL_SYSTEM]},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.get_data(
        GetData(
            modules=[MODEL_SYSTEM],
        ),
        request_id=REQUEST_ID,
    )
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_DATA_GET
    assert response.data == {EVENT_MODULES: [MODEL_SYSTEM]}


@pytest.mark.asyncio
async def test_get_directories(ws_client: WebSocketGenerator):
    """Test get directories."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_DIRECTORIES,
            data=[{"key": "documents", "path": "/documents"}],
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.get_directories(
        request_id=REQUEST_ID,
    )
    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], MediaDirectory)
    assert response[0].key == "documents"
    assert response[0].path == "/documents"


@pytest.mark.asyncio
async def test_get_files(ws_client: WebSocketGenerator):
    """Test get files."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_FILES,
            data={
                "files": [
                    {
                        "name": "test",
                        "path": "path/to",
                        "fullpath": "path/to/test",
                        "size": 0,
                        "last_accessed": 0,
                        "created": 0,
                        "modified": 0,
                        "is_directory": False,
                        "is_file": True,
                        "is_link": False,
                        "mime_type": None,
                    }
                ],
                "path": "path/to",
            },
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.get_files(
        MediaGetFiles(
            base="documents",
            path="path/to",
        ),
        request_id=REQUEST_ID,
    )
    assert isinstance(response, MediaFiles)
    assert response.files[0].name == "test"
    assert response.files[0].path == "path/to"
    assert response.files[0].fullpath == "path/to/test"
    assert response.files[0].size == 0
    assert response.files[0].last_accessed == 0
    assert response.files[0].created == 0
    assert response.files[0].modified == 0
    assert response.files[0].is_directory is False
    assert response.files[0].is_file is True
    assert response.files[0].is_link is False
    assert response.files[0].mime_type is None
    assert response.path == "path/to"
