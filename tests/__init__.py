"""Setup for tests."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import asdict
from json import dumps, loads
import logging
from typing import Any, Final

from aiohttp import web
from aiohttp.test_utils import TestClient

from systembridgeconnector.const import EventKey, EventSubType, EventType
from systembridgemodels.fixtures.media_files import FIXTURE_MEDIA_FILES
from systembridgemodels.fixtures.modules.battery import FIXTURE_BATTERY
from systembridgemodels.fixtures.modules.cpu import FIXTURE_CPU
from systembridgemodels.fixtures.modules.disks import FIXTURE_DISKS
from systembridgemodels.fixtures.modules.displays import FIXTURE_DISPLAYS
from systembridgemodels.fixtures.modules.gpus import FIXTURE_GPUS
from systembridgemodels.fixtures.modules.media import FIXTURE_MEDIA
from systembridgemodels.fixtures.modules.memory import FIXTURE_MEMORY
from systembridgemodels.fixtures.modules.networks import FIXTURE_NETWORKS
from systembridgemodels.fixtures.modules.processes import FIXTURE_PROCESSES
from systembridgemodels.fixtures.modules.sensors import FIXTURE_SENSORS
from systembridgemodels.fixtures.modules.system import FIXTURE_SYSTEM
from systembridgemodels.media_directories import MediaDirectory
from systembridgemodels.media_files import MediaFile, MediaFiles
from systembridgemodels.modules import Module, ModulesData
from systembridgemodels.notification import Notification
from systembridgemodels.request import Request
from systembridgemodels.response import Response

_LOGGER = logging.getLogger(__name__)

API_HOST: Final[str] = "127.0.0.1"
API_PORT: Final[int] = 9170
TOKEN: Final[str] = "abc123"

WEBSOCKET_PATH: Final[str] = "/api/websocket"

REQUEST_ID: Final[str] = "test"

MODULES_DATA = ModulesData(
    battery=FIXTURE_BATTERY,
    cpu=FIXTURE_CPU,
    disks=FIXTURE_DISKS,
    displays=FIXTURE_DISPLAYS,
    gpus=FIXTURE_GPUS,
    media=FIXTURE_MEDIA,
    memory=FIXTURE_MEMORY,
    networks=FIXTURE_NETWORKS,
    processes=FIXTURE_PROCESSES,
    sensors=FIXTURE_SENSORS,
    system=FIXTURE_SYSTEM,
)

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


async def process_request(request: Request) -> Response:
    """Process a request."""
    _LOGGER.info("Event: %s", request.event)

    if request.event == EventType.GET_DATA:
        return Response(
            id=request.id,
            type=EventType.DATA_GET,
            data=request.data,
        )
    elif request.event == EventType.GET_DIRECTORIES:
        return Response(
            id=request.id,
            type=EventType.DIRECTORIES,
            data=asdict(
                MediaDirectory(
                    key="documents",
                    path="/home/user/documents",
                )
            ),
        )
    elif request.event == EventType.GET_FILES:
        return Response(
            id=request.id,
            type=EventType.FILES,
            data=asdict(FIXTURE_MEDIA_FILES),
        )
    elif request.event == EventType.GET_FILE:
        return Response(
            id=request.id,
            type=EventType.FILE,
            data=asdict(
                FIXTURE_MEDIA_FILES.files[0],
            ),
        )
    elif request.event == EventType.REGISTER_DATA_LISTENER:
        return Response(
            id=request.id,
            type=EventType.DATA_LISTENER_REGISTERED,
            data=request.data,
        )
    elif request.event == EventType.KEYBOARD_KEYPRESS:
        return Response(
            id=request.id,
            type=EventType.KEYBOARD_KEY_PRESSED,
            data=request.data,
        )
    elif request.event == EventType.KEYBOARD_TEXT:
        return Response(
            id=request.id,
            type=EventType.KEYBOARD_TEXT_SENT,
            data=request.data,
        )
    elif request.event == EventType.NOTIFICATION:
        return Response(
            id=request.id,
            type=EventType.NOTIFICATION_SENT,
            data=request.data,
        )
    elif request.event == EventType.OPEN:
        return Response(
            id=request.id,
            type=EventType.OPENED,
            data=request.data,
        )
    elif request.event == EventType.POWER_SLEEP:
        return Response(
            id=request.id,
            type=EventType.POWER_SLEEPING,
            data=request.data,
        )
    elif request.event == EventType.POWER_HIBERNATE:
        return Response(
            id=request.id,
            type=EventType.POWER_HIBERNATING,
            data=request.data,
        )
    elif request.event == EventType.POWER_RESTART:
        return Response(
            id=request.id,
            type=EventType.POWER_RESTARTING,
            data=request.data,
        )
    elif request.event == EventType.POWER_SHUTDOWN:
        return Response(
            id=request.id,
            type=EventType.POWER_SHUTTINGDOWN,
            data=request.data,
        )
    elif request.event == EventType.POWER_LOCK:
        return Response(
            id=request.id,
            type=EventType.POWER_LOCKING,
            data=request.data,
        )
    elif request.event == EventType.POWER_LOGOUT:
        return Response(
            id=request.id,
            type=EventType.POWER_LOGGINGOUT,
            data=request.data,
        )

    return Response(
        id=request.id,
        type=EventType.ERROR,
        subtype=EventSubType.UNKNOWN_EVENT,
        data=request.data,
    )


async def process_message(message_data: str) -> str:
    """Process a message."""
    message_dict = loads(message_data)
    _LOGGER.debug("Message: %s", message_dict)
    request = Request(**message_dict)
    _LOGGER.debug("Request: %s", request)
    response = await process_request(request)
    _LOGGER.debug("Response: %s", response)
    return dumps(asdict(response))
