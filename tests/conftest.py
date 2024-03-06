from dataclasses import asdict

from aiohttp import ClientWebSocketResponse, web
import pytest
from pytest_socket import disable_socket

from systembridgemodels.response import Response

from . import API_PORT, REQUEST_ID, URL, ClientSessionGenerator, WebSocketGenerator


def pytest_runtest_setup():
    """Disable socket."""
    disable_socket()


@pytest.fixture
async def ws_client(
    aiohttp_client: ClientSessionGenerator,
    response: Response = Response(
        id=REQUEST_ID,
        type="TEST",
        data={"test": "test"},
    ),
) -> WebSocketGenerator:
    """Websocket client fixture connected to websocket server."""

    async def create_client(
        _: web.Request,
    ) -> ClientWebSocketResponse:
        """Create a websocket client."""
        app = web.Application()
        client = await aiohttp_client(
            app,
            server_kwargs={
                "port": API_PORT,
            },
        )

        websocket = await client.ws_connect(URL)
        _ = await websocket.receive_json()

        await websocket.send_json(asdict(response))

        return websocket

    return create_client
