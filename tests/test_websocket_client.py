"""Test the websocket client module."""

import asyncio
from typing import Any
from unittest.mock import patch

import aiohttp
from aiohttp.test_utils import TestClient
import pytest
from syrupy.assertion import SnapshotAssertion

from systembridgeconnector.const import EventKey, EventType
from systembridgeconnector.exceptions import (
    ConnectionClosedException,
    ConnectionErrorException,
)
from systembridgeconnector.websocket_client import WebSocketClient
from systembridgemodels.keyboard_key import KeyboardKey
from systembridgemodels.keyboard_text import KeyboardText
from systembridgemodels.media_control import MediaControl
from systembridgemodels.media_get_file import MediaGetFile
from systembridgemodels.media_get_files import MediaGetFiles
from systembridgemodels.modules import (
    GetData,
    Module,
    ModulesData,
    RegisterDataListener,
)
from systembridgemodels.notification import Notification
from systembridgemodels.open_path import OpenPath
from systembridgemodels.open_url import OpenUrl
from systembridgemodels.response import Response
from systembridgemodels.update import Update

from . import API_HOST, API_PORT, TOKEN, ClientSessionGenerator

modules_data = ModulesData()


@pytest.fixture
async def mock_websocket_client(
    mock_http_client: ClientSessionGenerator,
    mock_websocket_server: TestClient,
) -> WebSocketClient:
    """Return a websocket client."""
    client = await mock_http_client()
    ws = await mock_websocket_server.ws_connect("/api/websocket")

    return WebSocketClient(
        api_host=API_HOST,
        api_port=API_PORT,
        token=TOKEN,
        session=client.session,
        websocket=ws,
    )


@pytest.mark.asyncio
async def test_websocket(mock_websocket_client: WebSocketClient):
    """Test the websocket client."""
    await mock_websocket_client.connect()
    await asyncio.sleep(0.1)

    assert mock_websocket_client.connected
