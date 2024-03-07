"""Test the websocket client module."""

import asyncio
from typing import Any
from unittest.mock import patch

import aiohttp
import pytest

from systembridgeconnector.const import (
    EVENT_MODULES,
    TYPE_DATA_GET,
    TYPE_DATA_LISTENER_REGISTERED,
    TYPE_DIRECTORIES,
    TYPE_ERROR,
    TYPE_FILE,
    TYPE_FILES,
    TYPE_KEYBOARD_KEY_PRESSED,
    TYPE_KEYBOARD_TEXT_SENT,
    TYPE_NOTIFICATION_SENT,
    TYPE_OPENED,
    TYPE_POWER_HIBERNATING,
    TYPE_POWER_LOCKING,
    TYPE_POWER_LOGGINGOUT,
    TYPE_POWER_RESTARTING,
    TYPE_POWER_SHUTTINGDOWN,
    TYPE_POWER_SLEEPING,
)
from systembridgeconnector.exceptions import (
    ConnectionClosedException,
    ConnectionErrorException,
)
from systembridgeconnector.websocket_client import WebSocketClient
from systembridgemodels.const import MODEL_SYSTEM
from systembridgemodels.keyboard_key import KeyboardKey
from systembridgemodels.keyboard_text import KeyboardText
from systembridgemodels.media_control import MediaControl
from systembridgemodels.media_directories import MediaDirectory
from systembridgemodels.media_files import MediaFile, MediaFiles
from systembridgemodels.media_get_file import MediaGetFile
from systembridgemodels.media_get_files import MediaGetFiles
from systembridgemodels.modules import GetData, ModulesData, RegisterDataListener
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
        websocket_client.listen(callback=_handle_module_data),
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
async def test_timeout(ws_client: WebSocketGenerator):
    """Test timeout."""
    websocket_client = await _get_websocket_client(ws_client, base_response)
    assert websocket_client.connected is True

    with patch(
        "systembridgeconnector.websocket_client.WebSocketClient._wait_for_future",
        side_effect=asyncio.TimeoutError,
    ):
        response = await websocket_client.get_data(
            GetData(
                modules=[MODEL_SYSTEM],
            ),
            request_id=REQUEST_ID,
        )

    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_ERROR


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

    # # Test wait for data
    # while modules_data.system is None:
    #     await asyncio.sleep(0.1)

    # assert modules_data.system is not None


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


@pytest.mark.asyncio
async def test_get_file(ws_client: WebSocketGenerator):
    """Test get file."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_FILE,
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
    assert isinstance(response, MediaFile)
    assert response.name == "test"
    assert response.path == "path/to"
    assert response.fullpath == "path/to/test"
    assert response.size == 0
    assert response.last_accessed == 0
    assert response.created == 0
    assert response.modified == 0
    assert response.is_directory is False
    assert response.is_file is True
    assert response.is_link is False
    assert response.mime_type is None


@pytest.mark.asyncio
async def test_register_data_listener(ws_client: WebSocketGenerator):
    """Test register data listener."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_DATA_LISTENER_REGISTERED,
            data={EVENT_MODULES: [MODEL_SYSTEM]},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.register_data_listener(
        RegisterDataListener(
            modules=[MODEL_SYSTEM],
        ),
        request_id=REQUEST_ID,
    )
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_DATA_LISTENER_REGISTERED
    assert response.data == {EVENT_MODULES: [MODEL_SYSTEM]}


@pytest.mark.asyncio
async def test_keyboard_keypress(ws_client: WebSocketGenerator):
    """Test keyboard keypress."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_KEYBOARD_KEY_PRESSED,
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
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_KEYBOARD_KEY_PRESSED
    assert response.data == {"key": "a"}


@pytest.mark.asyncio
async def test_keyboard_text(ws_client: WebSocketGenerator):
    """Test keyboard text."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_KEYBOARD_TEXT_SENT,
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
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_KEYBOARD_TEXT_SENT
    assert response.data == {"text": "test"}


@pytest.mark.asyncio
async def test_media_control(ws_client: WebSocketGenerator):
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
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == "N/A"
    assert response.data == {}


@pytest.mark.asyncio
async def test_send_notification(ws_client: WebSocketGenerator):
    """Test send notification."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_NOTIFICATION_SENT,
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
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_NOTIFICATION_SENT
    assert response.data == {"title": "test", "message": "test"}


@pytest.mark.asyncio
async def test_open_path(ws_client: WebSocketGenerator):
    """Test open path."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_OPENED,
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
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_OPENED
    assert response.data == {"path": "test"}


@pytest.mark.asyncio
async def test_open_url(ws_client: WebSocketGenerator):
    """Test open url."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_OPENED,
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
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_OPENED
    assert response.data == {"url": "test"}


@pytest.mark.asyncio
async def test_power_control(ws_client: WebSocketGenerator):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_POWER_SLEEPING,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_sleep(
        request_id=REQUEST_ID,
    )
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_POWER_SLEEPING
    assert response.data == {}


@pytest.mark.asyncio
async def test_power_hibernate(ws_client: WebSocketGenerator):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_POWER_HIBERNATING,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_hibernate(
        request_id=REQUEST_ID,
    )
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_POWER_HIBERNATING
    assert response.data == {}


@pytest.mark.asyncio
async def test_power_restart(ws_client: WebSocketGenerator):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_POWER_RESTARTING,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_restart(
        request_id=REQUEST_ID,
    )
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_POWER_RESTARTING
    assert response.data == {}


@pytest.mark.asyncio
async def test_power_shutdown(ws_client: WebSocketGenerator):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_POWER_SHUTTINGDOWN,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_shutdown(
        request_id=REQUEST_ID,
    )
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_POWER_SHUTTINGDOWN
    assert response.data == {}


@pytest.mark.asyncio
async def test_power_lock(ws_client: WebSocketGenerator):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_POWER_LOCKING,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_lock(
        request_id=REQUEST_ID,
    )
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_POWER_LOCKING
    assert response.data == {}


@pytest.mark.asyncio
async def test_power_logout(ws_client: WebSocketGenerator):
    """Test power control."""
    websocket_client = await _get_websocket_client(
        ws_client,
        Response(
            id=REQUEST_ID,
            type=TYPE_POWER_LOGGINGOUT,
            data={},
        ),
    )
    assert websocket_client.connected is True
    response = await websocket_client.power_logout(
        request_id=REQUEST_ID,
    )
    assert isinstance(response, Response)
    assert response.id == REQUEST_ID
    assert response.type == TYPE_POWER_LOGGINGOUT
    assert response.data == {}
