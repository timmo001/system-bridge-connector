"""Test the http client module."""

from aiohttp import web
import pytest

from systembridgeconnector.http_client import HTTPClient

from . import API_HOST, API_PORT, TOKEN, ClientSessionGenerator


async def _json_response(_: web.Request):
    """Return a json response."""
    return web.json_response({"test": "test"})


async def _text_response(_: web.Request):
    """Return a text response."""
    return web.Response(text="test")


async def _get_http_client(aiohttp_client: ClientSessionGenerator) -> HTTPClient:
    """Return a HTTP client."""
    app = web.Application()
    app.router.add_delete("/test/json", _json_response)
    app.router.add_get("/test/json", _json_response)
    app.router.add_get("/test/text", _text_response)
    app.router.add_post("/test/json", _json_response)
    app.router.add_put("/test/json", _json_response)

    client = await aiohttp_client(
        app,
        server_kwargs={
            "port": API_PORT,
        },
    )

    return HTTPClient(
        api_host=API_HOST,
        api_port=API_PORT,
        token=TOKEN,
        session=client.session,
    )


@pytest.mark.asyncio
async def test_delete(aiohttp_client: ClientSessionGenerator):
    """Test the delete method."""
    client = await _get_http_client(aiohttp_client)
    response_json = await client.delete("/test/json", None)
    assert isinstance(response_json, dict)
    assert response_json == {"test": "test"}


@pytest.mark.asyncio
async def test_get(aiohttp_client: ClientSessionGenerator):
    """Test the get method."""
    client = await _get_http_client(aiohttp_client)
    response_json = await client.get("/test/json")
    assert isinstance(response_json, dict)
    assert response_json == {"test": "test"}

    response_text = await client.get("/test/text")
    assert response_text == "test"


@pytest.mark.asyncio
async def test_post(aiohttp_client: ClientSessionGenerator):
    """Test the post method."""
    client = await _get_http_client(aiohttp_client)
    response_json = await client.post("/test/json", None)
    assert isinstance(response_json, dict)
    assert response_json == {"test": "test"}


@pytest.mark.asyncio
async def test_put(aiohttp_client: ClientSessionGenerator):
    """Test the put method."""
    client = await _get_http_client(aiohttp_client)
    response_json = await client.put("/test/json", None)
    assert isinstance(response_json, dict)
    assert response_json == {"test": "test"}
