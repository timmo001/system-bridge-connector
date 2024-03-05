"""Test the http client module."""

from aiohttp import ClientSession, web
import pytest

from systembridgeconnector.http_client import HTTPClient

from . import API_HOST, API_PORT, TOKEN, ClientSessionGenerator


async def _test_response(_: web.Request):
    """Return a test response."""
    return web.json_response({"test": "test"})


async def _http_client(aiohttp_client: ClientSessionGenerator) -> HTTPClient:
    """Return a HTTP client."""
    app = web.Application()
    app.router.add_delete("/", _test_response)
    app.router.add_get("/", _test_response)

    client = await aiohttp_client(app)

    return HTTPClient(
        api_host=API_HOST,
        api_port=API_PORT,
        token=TOKEN,
        session=client.session,
    )


@pytest.mark.asyncio
async def test_delete(aiohttp_client: ClientSessionGenerator):
    """Test the delete method."""
    client = await _http_client(aiohttp_client)
    response = await client.delete("/", None)
    assert response is not None

    status = await response.status
    assert status == 200

    data = await response.json()
    assert data == {"test": "test"}


@pytest.mark.asyncio
async def test_get(aiohttp_client: ClientSessionGenerator):
    """Test the get method."""
    client = await _http_client(aiohttp_client)
    response = await client.get("/")
    assert response is not None

    status = await response.status
    assert status == 200

    data = await response.json()
    assert data == {"test": "test"}
