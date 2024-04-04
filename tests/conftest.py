"""Fixtures for testing."""

from aiohttp import web
from aiohttp.test_utils import TestClient
import pytest

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
from systembridgemodels.modules import ModulesData

from . import API_PORT, ClientSessionGenerator


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


# async def _websocket_response(
#     request: web.Request,
#     response: Response,
# ) -> web.WebSocketResponse:
#     """Return a websocket response."""
#     ws = web.WebSocketResponse()
#     await ws.prepare(request)
#     await ws.send_json(asdict(response))
#     await ws.close()
#     return ws


# def pytest_runtest_setup():
#     """Disable socket."""
#     pytest_socket.socket_allow_hosts(["127.0.0.1"])
#     pytest_socket.disable_socket(allow_unix_socket=True)


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


# @pytest.fixture
# async def ws_client(
#     aiohttp_client: ClientSessionGenerator,
#     response: Response,
#     socket_enabled: None,
# ) -> WebSocketGenerator:
#     """Websocket client fixture connected to websocket server."""

#     async def create_client(response: Response = response) -> MockClientWebSocket:
#         """Create a websocket client."""
#         app = web.Application()

#         # Add websocket route at /api/websocket
#         app.router.add_route(
#             "GET",
#             WEBSOCKET_PATH,
#             lambda request: _websocket_response(request, response),
#         )
#         client = await aiohttp_client(
#             app,
#             server_kwargs={
#                 "port": API_PORT,
#             },
#         )

#         websocket = await client.ws_connect(WEBSOCKET_PATH)

#         wrapped_websocket = cast(MockClientWebSocket, websocket)
#         wrapped_websocket.client = client
#         return wrapped_websocket

#     return create_client


# @pytest.fixture(name="response")
# def ws_response() -> Response:
#     """Return a response."""
#     return Response(
#         id="test",
#         type="TEST",
#         data={"test": "test"},
#     )


@pytest.fixture
def mock_modules_data() -> ModulesData:
    """Return a mock ModulesData."""
    return ModulesData(
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
