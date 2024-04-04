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

from . import REQUEST_ID

modules_data = ModulesData()


@pytest.mark.asyncio
async def test_connect(mock_websocket_client: WebSocketClient):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert mock_websocket_client.connected


@pytest.mark.asyncio
async def test_connect_error(mock_websocket_client: WebSocketClient):
    """Test the websocket client."""
    with patch(
        "aiohttp.ClientSession.ws_connect",
        side_effect=aiohttp.ClientConnectionError(),
    ), pytest.raises(ConnectionErrorException):
        await mock_websocket_client.connect()


@pytest.mark.asyncio
async def test_close(mock_websocket_client: WebSocketClient):
    """Test the websocket client."""
    await mock_websocket_client.connect()
    await mock_websocket_client.close()

    assert not mock_websocket_client.connected


@pytest.mark.asyncio
async def test_application_update(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.application_update(
            Update(version="1.0.0"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_exit_backend(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.exit_backend(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


# @pytest.mark.asyncio
# async def test_get_data(
#     snapshot: SnapshotAssertion,
#     mock_websocket_client: WebSocketClient,
# ):
#     """Test the websocket client."""
#     await mock_websocket_client.connect()

#     assert (
#         await mock_websocket_client.get_data(
#             GetData(modules=[Module.SYSTEM]),
#             request_id=REQUEST_ID,
#             timeout=6,
#         )
#         == snapshot
#     )


@pytest.mark.asyncio
async def test_get_directories(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.get_directories(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_get_files(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.get_files(
            MediaGetFiles(
                base="documents",
                path="/home/user/documents",
            ),
            request_id=REQUEST_ID,
        )
        == snapshot
    )
