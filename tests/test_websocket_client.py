"""Test the websocket client module."""

import asyncio
from dataclasses import asdict
from json import dumps
from unittest.mock import patch

import aiohttp
import pytest
from syrupy.assertion import SnapshotAssertion

from systembridgeconnector.const import EventSubType, EventType
from systembridgeconnector.exceptions import (
    AuthenticationException,
    BadMessageException,
    ConnectionClosedException,
    ConnectionErrorException,
    DataMissingException,
)
from systembridgeconnector.websocket_client import WebSocketClient
from systembridgemodels.keyboard_key import KeyboardKey
from systembridgemodels.keyboard_text import KeyboardText
from systembridgemodels.media_control import MediaControl
from systembridgemodels.media_get_file import MediaGetFile
from systembridgemodels.media_get_files import MediaGetFiles
from systembridgemodels.modules import GetData, Module, RegisterDataListener
from systembridgemodels.notification import Notification
from systembridgemodels.open_path import OpenPath
from systembridgemodels.open_url import OpenUrl
from systembridgemodels.response import Response
from systembridgemodels.update import Update

from . import API_HOST, API_PORT, REQUEST_ID, ClientSessionGenerator


@pytest.mark.asyncio
async def test_connect(mock_websocket_client_connected: WebSocketClient):
    """Test the websocket client."""
    assert mock_websocket_client_connected.connected


@pytest.mark.asyncio
async def test_connect_error(mock_websocket_client: WebSocketClient):
    """Test the websocket client."""
    with patch(
        "aiohttp.ClientSession.ws_connect",
        side_effect=aiohttp.ClientConnectionError(),
    ), pytest.raises(ConnectionErrorException):
        await mock_websocket_client.connect()


@pytest.mark.asyncio
async def test_connection_closed(mock_websocket_client_connected: WebSocketClient):
    """Test the websocket client."""
    await mock_websocket_client_connected.close()

    with pytest.raises(ConnectionClosedException):
        await mock_websocket_client_connected.application_update(
            Update(version="1.0.0"),
            request_id=REQUEST_ID,
        )


@pytest.mark.asyncio
async def test_close(mock_websocket_client_connected: WebSocketClient):
    """Test the websocket client."""
    await mock_websocket_client_connected.close()

    assert not mock_websocket_client_connected.connected


@pytest.mark.asyncio
async def test_application_update(
    snapshot: SnapshotAssertion,
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_connected.application_update(
            Update(version="1.0.0"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_exit_backend(
    snapshot: SnapshotAssertion,
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_connected.exit_backend(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_get_data(
    snapshot: SnapshotAssertion,
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_connected.get_data(
            GetData(modules=[Module.SYSTEM]),
            request_id=REQUEST_ID,
            timeout=8,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_get_directories(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.get_directories(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_get_files(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.get_files(
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
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.get_file(
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
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.register_data_listener(
            RegisterDataListener(modules=[Module.SYSTEM]),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_keyboard_keypress(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.keyboard_keypress(
            KeyboardKey(key="a"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_keyboard_text(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.keyboard_text(
            KeyboardText(text="test"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_media_control(
    snapshot: SnapshotAssertion,
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_connected.media_control(
            MediaControl(action="play"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_send_notification(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.send_notification(
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
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.open_path(
            OpenPath(path="/home/user/documents"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_open_url(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.open_url(
            OpenUrl(url="https://www.google.com"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_sleep(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.power_sleep(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_hibernate(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.power_hibernate(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_restart(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.power_restart(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_shutdown(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.power_shutdown(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_lock(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.power_lock(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_power_logout(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.power_logout(
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_wait_for_response_timeout(
    snapshot: SnapshotAssertion,
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    with patch(
        "systembridgeconnector.websocket_client.asyncio.wait_for",
        side_effect=asyncio.TimeoutError(),
    ):
        assert (
            await mock_websocket_client_connected.get_data(
                GetData(modules=[Module.SYSTEM]),
                request_id=REQUEST_ID,
                timeout=1,
            )
            == snapshot
        )


@pytest.mark.asyncio
async def test_get_data_data_missing(
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    with pytest.raises(DataMissingException):
        await mock_websocket_client_connected.get_data(
            GetData(modules=[Module.CPU]),
            request_id=REQUEST_ID,
            timeout=1,
        )


@pytest.mark.asyncio
async def test_get_data_task_cancelled(
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    with patch(
        "systembridgeconnector.websocket_client.WebSocketClient.listen",
        side_effect=asyncio.CancelledError(),
    ), pytest.raises(asyncio.CancelledError):
        await mock_websocket_client_listening.get_data(
            GetData(modules=[Module.SYSTEM]),
            request_id=REQUEST_ID,
            timeout=1,
        )


@pytest.mark.asyncio
async def test_get_data_task_exception(
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    with patch(
        "systembridgeconnector.websocket_client.WebSocketClient.listen",
        side_effect=ConnectionClosedException(),
    ), pytest.raises(ConnectionClosedException):
        await mock_websocket_client_listening.get_data(
            GetData(modules=[Module.SYSTEM]),
            request_id=REQUEST_ID,
            timeout=1,
        )


@pytest.mark.asyncio
async def test_unknown_message(
    snapshot: SnapshotAssertion,
    mock_websocket_client_listening: WebSocketClient,
):
    """Test the websocket client."""
    assert (
        await mock_websocket_client_listening.send_message(
            event="BAD_TYPE",
            request_id=REQUEST_ID,
            data={},
            wait_for_response=False,
            response_type="BAD_TYPE",
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_bad_token(
    snapshot: SnapshotAssertion,
    mock_websocket_session: ClientSessionGenerator,
):
    """Test the websocket client."""
    client = await mock_websocket_session()
    ws = await client.ws_connect("/api/websocket")

    websocket_client = WebSocketClient(
        api_host=API_HOST,
        api_port=API_PORT,
        token="badtoken",
        session=client.session,
        websocket=ws,
        can_close_session=True,
    )

    await websocket_client.connect()

    assert (
        await websocket_client.application_update(
            Update(version="1.0.0"),
            request_id=REQUEST_ID,
        )
        == snapshot
    )


@pytest.mark.asyncio
async def test_listen_for_messages_disconnnected(
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client_connected.close()

    async def callback(_):
        pass

    with pytest.raises(ConnectionClosedException):
        await mock_websocket_client_connected.listen_for_messages(
            callback=callback,
            name="Test WebSocket Listener",
        )


@pytest.mark.asyncio
async def test_receive_message_disconnnected(
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    await mock_websocket_client_connected.close()

    with pytest.raises(ConnectionClosedException):
        await mock_websocket_client_connected.receive_message()


@pytest.mark.asyncio
async def test_receive_message_runtime_error(
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    with patch(
        "aiohttp.ClientWebSocketResponse.receive",
        side_effect=RuntimeError(),
    ):
        assert await mock_websocket_client_connected.receive_message() is None


@pytest.mark.asyncio
async def test_receive_message_type_close(
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    with patch(
        "aiohttp.ClientWebSocketResponse.receive",
        return_value=aiohttp.WSMessage(
            type=aiohttp.WSMsgType.CLOSE,
            data=None,
            extra=None,
        ),
    ), pytest.raises(ConnectionClosedException):
        await mock_websocket_client_connected.receive_message()


@pytest.mark.asyncio
async def test_receive_message_type_error(
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    with patch(
        "aiohttp.ClientWebSocketResponse.receive",
        return_value=aiohttp.WSMessage(
            type=aiohttp.WSMsgType.ERROR,
            data=None,
            extra=None,
        ),
    ), pytest.raises(ConnectionErrorException):
        await mock_websocket_client_connected.receive_message()


#
@pytest.mark.asyncio
async def test_receive_message_bad_token(
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    with patch(
        "aiohttp.ClientWebSocketResponse.receive",
        return_value=aiohttp.WSMessage(
            type=aiohttp.WSMsgType.TEXT,
            data=dumps(
                asdict(
                    Response(
                        id=REQUEST_ID,
                        type=EventType.ERROR,
                        subtype=EventSubType.BAD_TOKEN,
                        data={},
                    )
                )
            ),
            extra=None,
        ),
    ), pytest.raises(AuthenticationException):
        await mock_websocket_client_connected.receive_message()


@pytest.mark.asyncio
async def test_receive_message_type_unknown_message(
    mock_websocket_client_connected: WebSocketClient,
):
    """Test the websocket client."""
    with patch(
        "aiohttp.ClientWebSocketResponse.receive",
        return_value=aiohttp.WSMessage(
            type=aiohttp.WSMsgType.BINARY,
            data=None,
            extra=None,
        ),
    ), pytest.raises(BadMessageException):
        await mock_websocket_client_connected.receive_message()
