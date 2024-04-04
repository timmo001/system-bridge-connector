"""Test the version module."""

from dataclasses import asdict
from unittest.mock import AsyncMock, patch

import pytest

from systembridgeconnector.exceptions import ConnectionErrorException
from systembridgeconnector.version import SUPPORTED_VERSION, Version
from systembridgemodels.modules.system import System

from . import API_HOST, API_PORT, TOKEN, ClientSessionGenerator

system = System(
    boot_time=0,
    fqdn="",
    hostname="",
    ip_address_4="",
    mac_address="",
    platform_version="",
    platform="",
    uptime=0,
    users=[],
    uuid="",
    version=SUPPORTED_VERSION,
)


@pytest.mark.asyncio
async def test_check_supported(mock_http_client_session: ClientSessionGenerator):
    """Test check supported."""
    client = await mock_http_client_session()
    version = Version(
        api_host=API_HOST,
        api_port=API_PORT,
        token=TOKEN,
        session=client.session,
    )

    with patch(
        "systembridgeconnector.http_client.HTTPClient.get",
        new_callable=AsyncMock,
    ) as mock_get:
        # Test supported version is supported
        system.version = SUPPORTED_VERSION
        mock_get.return_value = asdict(system)
        assert await version.check_supported() is True

        # Test future version is supported
        system.version = "100.0.0"
        mock_get.return_value = asdict(system)
        assert await version.check_supported() is True

        # Test 3.0.0 version is not supported
        system.version = "3.0.0"
        mock_get.return_value = asdict(system)
        assert await version.check_supported() is False

        # Test 2.0.0 version is not supported
        system.version = "2.0.0"
        mock_get.return_value = asdict(system)
        assert await version.check_supported() is False


@pytest.mark.asyncio
async def test_check_version_2(mock_http_client_session: ClientSessionGenerator):
    """Test check version 2."""
    client = await mock_http_client_session()
    version = Version(
        api_host=API_HOST,
        api_port=API_PORT,
        token=TOKEN,
        session=client.session,
    )

    with patch(
        "systembridgeconnector.http_client.HTTPClient.get",
        new_callable=AsyncMock,
    ) as mock_get:
        system.version = "2.0.0"
        mock_get.return_value = asdict(system)
        result = await version.check_version_2()
        assert result == "2.0.0"


async def test_check_version_2_connection_error(mock_http_client_session: ClientSessionGenerator):
    """Test check version 2 connection error."""
    client = await mock_http_client_session()
    version = Version(
        api_host=API_HOST,
        api_port=API_PORT,
        token=TOKEN,
        session=client.session,
    )

    with patch(
        "systembridgeconnector.http_client.HTTPClient.get",
        side_effect=ConnectionErrorException(
            {
                "status": 404,
                "message": "Not Found",
            },
        ),
    ):
        result = await version.check_version_2()
        assert result is None

    with patch(
        "systembridgeconnector.http_client.HTTPClient.get",
        side_effect=ConnectionErrorException(
            {
                "status": 500,
                "message": "Internal Server Error",
            },
        ),
    ), pytest.raises(ConnectionErrorException):
        await version.check_version_2()


@pytest.mark.asyncio
async def test_check_version(mock_http_client_session: ClientSessionGenerator):
    """Test check version."""
    client = await mock_http_client_session()
    version = Version(
        api_host=API_HOST,
        api_port=API_PORT,
        token=TOKEN,
        session=client.session,
    )

    with patch(
        "systembridgeconnector.http_client.HTTPClient.get",
        new_callable=AsyncMock,
    ) as mock_get:
        system.version = "3.0.0"
        mock_get.return_value = asdict(system)
        result = await version.check_version()
        assert result == "3.0.0"


@pytest.mark.asyncio
async def test_check_version_connection_error(mock_http_client_session: ClientSessionGenerator):
    """Test check version connection error."""
    client = await mock_http_client_session()
    version = Version(
        api_host=API_HOST,
        api_port=API_PORT,
        token=TOKEN,
        session=client.session,
    )

    with patch(
        "systembridgeconnector.http_client.HTTPClient.get",
        side_effect=ConnectionErrorException(
            {
                "status": 404,
                "message": "Not Found",
            },
        ),
    ):
        result = await version.check_version()
        assert result is None

    with patch(
        "systembridgeconnector.http_client.HTTPClient.get",
        side_effect=ConnectionErrorException(
            {
                "status": 500,
                "message": "Internal Server Error",
            },
        ),
    ), pytest.raises(ConnectionErrorException):
        await version.check_version()
