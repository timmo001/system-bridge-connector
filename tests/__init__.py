"""Setup for tests."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import asdict
from json import dumps, loads
from typing import Any, Final

from aiohttp import web
from aiohttp.test_utils import TestClient

from systembridgeconnector.const import EventKey, EventSubType, EventType
from systembridgemodels.fixtures.media_files import FIXTURE_MEDIA_FILES
from systembridgemodels.media_directories import MediaDirectory
from systembridgemodels.media_files import MediaFile, MediaFiles
from systembridgemodels.modules import Module, ModulesData
from systembridgemodels.notification import Notification
from systembridgemodels.request import Request
from systembridgemodels.response import Response

API_HOST: Final[str] = "127.0.0.1"
API_PORT: Final[int] = 9170
REQUEST_ID: Final[str] = "test"
TOKEN: Final[str] = "abc123"
WEBSOCKET_PATH: Final[str] = "/api/websocket"

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
    if request.event == EventType.GET_DIRECTORIES:
        return Response(
            id=request.id,
            type=EventType.MEDIA_DIRECTORIES,
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

    return Response(
        id=request.id,
        type="response",
        data={"test": "test"},
    )


async def process_message(message_data: str) -> str:
    """Process a message."""
    message_dict = loads(message_data)
    request = Request(**message_dict)
    return dumps(await process_request(request))
