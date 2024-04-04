"""Test the websocket client module."""

import asyncio
from typing import Any
from unittest.mock import patch

import aiohttp
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

from . import API_HOST, API_PORT, REQUEST_ID, TOKEN, WebSocketGenerator

base_response = Response(
    id=REQUEST_ID,
    type="TEST",
    data={"test": "test"},
)

modules_data = ModulesData()


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

    async def _handle_module_data(
        module: str,
        data: Any,
    ) -> None:
        """Handle module data."""
        setattr(modules_data, module, data)

    # Run the listener in the background
    asyncio.get_event_loop().create_task(
        websocket_client.listen(
            callback=_handle_module_data,
            accept_other_types=False,
            name="Test WebSocket Listener",
        ),
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
async def test_connection_closed(ws_client: WebSocketGenerator):
    """Test connection closed."""
    websocket_client = await _get_websocket_client(ws_client, base_response)
    assert websocket_client.connected is True

    await websocket_client.close()
    assert websocket_client.connected is False

    with patch(
        "aiohttp.ClientSession.ws_connect",
        side_effect=aiohttp.ClientConnectionError,
    ), pytest.raises(ConnectionClosedException):
        await websocket_client.application_update(Update(version="0.0.0"))


@pytest.mark.asyncio
async def test_timeout(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test timeout."""
    websocket_client = await _get_websocket_client(ws_client, base_response)
    assert websocket_client.connected is True

    with patch(
        "systembridgeconnector.websocket_client.WebSocketClient._wait_for_future",
        side_effect=asyncio.TimeoutError,
    ):
        response = await websocket_client.get_data(
            GetData(
                modules=[Module.SYSTEM],
            ),
            request_id=REQUEST_ID,
        )

    assert response == snapshot(
        name="websocket_client_timeout",
    )


@pytest.mark.asyncio
async def test_close(ws_client: WebSocketGenerator):
    """Test close."""
    websocket_client = await _get_websocket_client(ws_client, base_response)
    assert websocket_client.connected is True

    await websocket_client.close()
    assert websocket_client.connected is False


@pytest.mark.asyncio
async def test_application_update(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test application update."""
    websocket_client = await _get_websocket_client(ws_client, base_response)
    assert websocket_client.connected is True
    response = await websocket_client.application_update(
        Update(
            version="0.0.0",
        ),
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_application_update",
    )


@pytest.mark.asyncio
async def test_exit_backend(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test exit backend."""
    websocket_client = await _get_websocket_client(ws_client, base_response)
    assert websocket_client.connected is True
    response = await websocket_client.exit_backend(
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_exit_backend",
    )


@pytest.mark.asyncio
async def test_get_data(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test get data."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.DATA_GET,
            data={EventKey.MODULES: [Module.SYSTEM]},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.get_data(
        GetData(
            modules=[Module.SYSTEM],
        ),
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_get_data",
    )


@pytest.mark.asyncio
async def test_get_directories(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test get directories."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.DIRECTORIES,
            data=[{"key": "documents", "path": "/documents"}],
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.get_directories(
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_get_directories",
    )


@pytest.mark.asyncio
async def test_get_files(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test get files."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.FILES,
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
    assert response == snapshot(
        name="websocket_client_get_files",
    )


@pytest.mark.asyncio
async def test_get_file(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test get file."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.FILE,
            data={
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
            },
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.get_file(
        MediaGetFile(
            base="documents",
            path="path/to/test",
        ),
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_get_file",
    )


@pytest.mark.asyncio
async def test_register_data_listener(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test register data listener."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.DATA_LISTENER_REGISTERED,
            data={EventKey.MODULES: [Module.SYSTEM]},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.register_data_listener(
        RegisterDataListener(
            modules=[Module.SYSTEM],
        ),
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_register_data_listener",
    )


@pytest.mark.asyncio
async def test_keyboard_keypress(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test keyboard keypress."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.KEYBOARD_KEY_PRESSED,
            data={"key": "a"},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.keyboard_keypress(
        KeyboardKey(
            key="a",
        ),
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_keyboard_keypress",
    )


@pytest.mark.asyncio
async def test_keyboard_text(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test keyboard text."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.KEYBOARD_TEXT_SENT,
            data={"text": "test"},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.keyboard_text(
        KeyboardText(
            text="test",
        ),
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_keyboard_text",
    )


@pytest.mark.asyncio
async def test_media_control(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test media control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type="N/A",
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.media_control(
        MediaControl(
            action="play",
        ),
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_media_control",
    )


@pytest.mark.asyncio
async def test_send_notification(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test send notification."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.NOTIFICATION_SENT,
            data={"title": "test", "message": "test"},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.send_notification(
        Notification(
            title="test",
            message="test",
        ),
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_send_notification",
    )


@pytest.mark.asyncio
async def test_open_path(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test open path."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.OPENED,
            data={"path": "test"},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.open_path(
        OpenPath(
            path="test",
        ),
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_open_path",
    )


@pytest.mark.asyncio
async def test_open_url(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test open url."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.OPENED,
            data={"url": "test"},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.open_url(
        OpenUrl(
            url="test",
        ),
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_open_url",
    )


@pytest.mark.asyncio
async def test_power_sleep(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.POWER_SLEEPING,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_sleep(
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_power_sleep",
    )


@pytest.mark.asyncio
async def test_power_hibernate(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.POWER_HIBERNATING,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_hibernate(
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_power_hibernate",
    )


@pytest.mark.asyncio
async def test_power_restart(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.POWER_RESTARTING,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_restart(
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_power_restart",
    )


@pytest.mark.asyncio
async def test_power_shutdown(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.POWER_SHUTTINGDOWN,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_shutdown(
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_power_shutdown",
    )


@pytest.mark.asyncio
async def test_power_lock(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.POWER_LOCKING,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_lock(
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_power_lock",
    )


@pytest.mark.asyncio
async def test_power_logout(
    snapshot: SnapshotAssertion,
    ws_client: WebSocketGenerator,
):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=EventType.POWER_LOGGINGOUT,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_logout(
        request_id=REQUEST_ID,
    )
    assert response == snapshot(
        name="websocket_client_power_logout",
    )
