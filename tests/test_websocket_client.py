"""Test the websocket client module."""

from unittest.mock import patch

import aiohttp
import pytest
from syrupy.assertion import SnapshotAssertion

from systembridgeconnector.exceptions import ConnectionErrorException
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


@pytest.mark.asyncio
async def test_get_file(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.get_file(
            MediaGetFile(
                base="documents",
                path="/home/user/documents/test.txt",
            ),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_register_data_listener(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.register_data_listener(
            RegisterDataListener(modules=[Module.SYSTEM]),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_keyboard_keypress(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.keyboard_keypress(
            KeyboardKey(key="a"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_keyboard_text(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.keyboard_text(
            KeyboardText(text="test"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_media_control(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.media_control(
            MediaControl(action="play"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_send_notification(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.send_notification(
            Notification(
                title="Test",
                message="test",
            ),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_open_path(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.open_path(
            OpenPath(path="/home/user/documents"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_open_url(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.open_url(
            OpenUrl(url="https://www.google.com"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_sleep(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.power_sleep(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_hibernate(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.power_hibernate(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_restart(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.power_restart(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_shutdown(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.power_shutdown(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_lock(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.power_lock(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_logout(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()

    assert (
        await mock_websocket_client.power_logout(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_listen(
    snapshot: SnapshotAssertion,
    mock_websocket_client: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client.connect()
    await mock_websocket_client.listen()

    assert await mock_websocket_client.listen() == snapshot
