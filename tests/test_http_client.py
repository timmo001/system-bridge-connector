"""Test the http client module."""

import asyncio
from unittest.mock import patch

import pytest

from systembridgeconnector.exceptions import (
    AuthenticationException,
    BadRequestException,
    ConnectionErrorException,
)
from systembridgeconnector.http_client import HTTPClient

from . import API_HOST, API_PORT, TOKEN, ClientSessionGenerator


async def _get_http_client(http_client: ClientSessionGenerator) -> HTTPClient:
    """Return a HTTP client."""
    client = await http_client()

    return HTTPClient(
        api_host=API_HOST,
        api_port=API_PORT,
        token=TOKEN,
        session=client.session,
    )


@pytest.mark.asyncio
async def test_delete(http_client: ClientSessionGenerator):
    """Test the delete method."""
    client = await _get_http_client(http_client)
    response_json = await client.delete("/test/json", None)
    assert isinstance(response_json, dict)
    assert response_json == {"test": "test"}


@pytest.mark.asyncio
async def test_get(http_client: ClientSessionGenerator):
    """Test the get method."""
    client = await _get_http_client(http_client)
    response_json = await client.get("/test/json")
    assert isinstance(response_json, dict)
    assert response_json == {"test": "test"}

    response_text = await client.get("/test/text")
    assert response_text == "test"


@pytest.mark.asyncio
async def test_post(http_client: ClientSessionGenerator):
    """Test the post method."""
    client = await _get_http_client(http_client)
    response_json = await client.post("/test/json", None)
    assert isinstance(response_json, dict)
    assert response_json == {"test": "test"}


@pytest.mark.asyncio
async def test_put(http_client: ClientSessionGenerator):
    """Test the put method."""
    client = await _get_http_client(http_client)
    response_json = await client.put("/test/json", None)
    assert isinstance(response_json, dict)
    assert response_json == {"test": "test"}


@pytest.mark.asyncio
async def test_bad_request(http_client: ClientSessionGenerator):
    """Test the bad request response."""
    client = await _get_http_client(http_client)
    with pytest.raises(BadRequestException):
        await client.get("/test/badrequest")


@pytest.mark.asyncio
async def test_not_found(http_client: ClientSessionGenerator):
    """Test the not found response."""
    client = await _get_http_client(http_client)
    with pytest.raises(ConnectionErrorException):
        await client.get("/test/notfound")


@pytest.mark.asyncio
async def test_unauthorised(http_client: ClientSessionGenerator):
    """Test the unauthorised response."""
    client = await _get_http_client(http_client)
    with pytest.raises(AuthenticationException):
        await client.get("/test/unauthorised")


@pytest.mark.asyncio
async def test_timeout(http_client: ClientSessionGenerator):
    """Test the timeout."""
    client = await _get_http_client(http_client)
    with patch(
        "aiohttp.client.ClientSession.request",
        side_effect=asyncio.TimeoutError,
    ), pytest.raises(ConnectionErrorException):
        await client.get("/test/json")


@pytest.mark.asyncio
async def test_connection_error(http_client: ClientSessionGenerator):
    """Test the connection error."""
    client = await _get_http_client(http_client)
    with patch(
        "aiohttp.client.ClientSession.request",
        side_effect=ConnectionResetError,
    ), pytest.raises(ConnectionErrorException):
        await client.get("/test/json")
