"""Fixtures for testing."""

from dataclasses import asdict
from typing import cast

from aiohttp import web
from aiohttp.test_utils import TestClient
import pytest
import pytest_socket

from systembridgemodels.response import Response

from . import (
    API_PORT,
    WEBSOCKET_PATH,
    ClientSessionGenerator,
    MockClientWebSocket,
    WebSocketGenerator,
)


async def _bad_request_response(_: web.Request):
    """Return a bad request response."""
    return web.json_response(
        {"test": "test"},
        status=400,
    )


async def _json_response(_: web.Request):
    """Return a json response."""
    return web.json_response({"test": "test"})


async def _text_response(_: web.Request):
    """Return a text response."""
    return web.Response(text="test")


async def _unauthorised_response(_: web.Request):
    """Return an unauthorised response."""
    return web.json_response(
        {"test": "test"},
        status=401,
    )


async def _websocket_response(
    request: web.Request,
    response: Response,
) -> web.WebSocketResponse:
    """Return a websocket response."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await ws.send_json(asdict(response))
    await ws.close()
    return ws


def pytest_runtest_setup():
    """Disable socket."""
    pytest_socket.socket_allow_hosts(["127.0.0.1"])
    pytest_socket.disable_socket(allow_unix_socket=True)


@pytest.fixture
def http_client(
    aiohttp_client: ClientSessionGenerator,
    socket_enabled: None,
) -> ClientSessionGenerator:
    """Return a client session."""

    async def create_client() -> TestClient:
        """Create a client session."""
        app = web.Application()
        app.router.add_delete("/test/json", _json_response)
        app.router.add_get("/test/badrequest", _bad_request_response)
        app.router.add_get("/test/json", _json_response)
        app.router.add_get("/test/text", _text_response)
        app.router.add_get("/test/unauthorised", _unauthorised_response)
        app.router.add_post("/test/json", _json_response)
        app.router.add_put("/test/json", _json_response)

        return await aiohttp_client(
            app,
            server_kwargs={
                "port": API_PORT,
            },
        )

    return create_client


@pytest.fixture
async def ws_client(
    aiohttp_client: ClientSessionGenerator,
    response: Response,
    socket_enabled: None,
) -> WebSocketGenerator:
    """Websocket client fixture connected to websocket server."""

    async def create_client(response: Response = response) -> MockClientWebSocket:
        """Create a websocket client."""
        app = web.Application()

        # Add websocket route at /api/websocket
        app.router.add_route(
            "GET",
            WEBSOCKET_PATH,
            lambda request: _websocket_response(request, response),
        )
        client = await aiohttp_client(
            app,
            server_kwargs={
                "port": API_PORT,
            },
        )

        websocket = await client.ws_connect(WEBSOCKET_PATH)

        wrapped_websocket = cast(MockClientWebSocket, websocket)
        wrapped_websocket.client = client
        return wrapped_websocket

    return create_client


@pytest.fixture(name="response")
def ws_response() -> Response:
    """Return a response."""
    return Response(
        id="test",
        type="TEST",
        data={"test": "test"},
    )
