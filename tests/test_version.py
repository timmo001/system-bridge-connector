"""Test the version module."""

from dataclasses import asdict
from unittest.mock import AsyncMock, patch

import pytest

from systembridgeconnector.version import SUPPORTED_VERSION, Version
from systembridgemodels.modules.system import System

from . import API_HOST, API_PORT, TOKEN, ClientSessionGenerator


@pytest.mark.asyncio
async def test_check_supported(http_client: ClientSessionGenerator):
    """Test check_supported."""
    client = await http_client()
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
        mock_get.return_value = asdict(
            System(
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
        )

        assert await version.check_supported() is True


@pytest.mark.asyncio
async def test_check_version_2(http_client: ClientSessionGenerator):
    """Test check_version 2."""
    client = await http_client()
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
        mock_get.return_value = asdict(
            System(
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
                version="2.0.0",
            )
        )
        result = await version.check_version_2()
        assert result == "2.0.0"


@pytest.mark.asyncio
async def test_check_version_3(http_client: ClientSessionGenerator):
    """Test check_version 3."""
    client = await http_client()
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
        mock_get.return_value = asdict(
            System(
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
                version="3.0.0",
            )
        )
        result = await version.check_version_3()
        assert result == "3.0.0"
