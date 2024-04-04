"""Fixtures for testing."""

from aiohttp import web
from aiohttp.test_utils import TestClient
import pytest

from systembridgeconnector.http_client import HTTPClient
from systembridgeconnector.websocket_client import WebSocketClient
from systembridgemodels.modules import ModulesData

from . import (
    _LOGGER,
    API_HOST,
    API_PORT,
    MODULES_DATA,
    TOKEN,
    ClientSessionGenerator,
    bad_request_response,
    json_response,
    process_message,
    text_response,
    unauthorised_response,
)


@pytest.fixture(name="mock_http_client_session")
def mock_http_client_session_generator(
    aiohttp_client: ClientSessionGenerator,
    socket_enabled: None,
) -> ClientSessionGenerator:
    """Return a client session."""

    async def create_client() -> TestClient:
        """Create a client session."""
        app = web.Application()
        app.router.add_delete("/test/json", json_response)
        app.router.add_get("/test/badrequest", bad_request_response)
        app.router.add_get("/test/json", json_response)
        app.router.add_get("/test/text", text_response)
        app.router.add_get("/test/unauthorised", unauthorised_response)
        app.router.add_post("/test/json", json_response)
        app.router.add_put("/test/json", json_response)

        return await aiohttp_client(
            app,
            server_kwargs={
                "port": API_PORT,
            },
        )

    return create_client


@pytest.fixture
async def mock_http_client(
    mock_http_client_session: ClientSessionGenerator,
) -> HTTPClient:
    """Return a HTTP client."""
    client = await mock_http_client_session()

    return HTTPClient(
        api_host=API_HOST,
        api_port=API_PORT,
        token=TOKEN,
        session=client.session,
    )


@pytest.fixture
def mock_modules_data() -> ModulesData:
    """Return a mock ModulesData."""
    return MODULES_DATA


@pytest.fixture(name="mock_websocket_session")
async def mock_websocket_session_generator(
    aiohttp_client: ClientSessionGenerator,
    socket_enabled: None,
) -> ClientSessionGenerator:
    """Return a websocket client."""

    async def create_client() -> TestClient:
        """Create a client session."""
        app = web.Application()
        app.router.add_get("/api/websocket", websocket_response)

        return await aiohttp_client(
            app,
            server_kwargs={
                "port": API_PORT,
            },
        )

    async def websocket_response(request) -> web.WebSocketResponse:
        """Return a websocket response."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                response = await process_message(msg.data)
                _LOGGER.info(response)
                await ws.send_str(response)
                _LOGGER.debug("Sent text message")
            elif msg.type == web.WSMsgType.BINARY:
                await ws.send_bytes(msg.data)
                _LOGGER.debug("Sent binary message")
            elif msg.type == web.WSMsgType.CLOSE:
                await ws.close()
                _LOGGER.debug("WebSocket closed")

        return ws

    return create_client


@pytest.fixture
async def mock_websocket_client(
    mock_websocket_session: ClientSessionGenerator,
) -> WebSocketClient:
    """Return a websocket client."""
    client = await mock_websocket_session()
    ws = await client.ws_connect("/api/websocket")

    return WebSocketClient(
        api_host=API_HOST,
        api_port=API_PORT,
        token=TOKEN,
        session=client.session,
        websocket=ws,
        can_close_session=True,
    )
