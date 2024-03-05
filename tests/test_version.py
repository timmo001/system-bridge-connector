"""Test the version module."""

# import asyncio
# from unittest.mock import AsyncMock, patch

# from aiohttp import ClientSession
# import pytest

# from systembridgeconnector.version import SUPPORTED_VERSION, Version

# from . import API_HOST, API_PORT, TOKEN

# @pytest.fixture
# def mock_session():
#     """Mock aiohttp.ClientSession."""
#     mocker = AiohttpClientMocker()

#     with patch(
#         "aiohttp.ClientSession",
#         side_effect=lambda *args, **kwargs: mocker.create_session(
#             asyncio.get_event_loop()
#         ),
#     ):
#         yield mocker


# version = Version(
#     API_HOST,
#     API_PORT,
#     TOKEN,
#     mock_session,
# )


# @pytest.mark.asyncio
# async def test_check_supported():
#     """Test check_supported."""
#     with patch(
#         "systembridgeconnector.http_client.HTTPClient.get",
#         new_callable=AsyncMock,
#     ) as mock_get:
#         mock_get.return_value = {
#             "version": SUPPORTED_VERSION,
#         }

#         result = await version.check_supported()
#         assert result is True


# @pytest.mark.asyncio
# async def test_check_version_2():
#     """Test check_version 2."""
#     with patch(
#         "systembridgeconnector.http_client.HTTPClient.get",
#         new_callable=AsyncMock,
#     ) as mock_get:
#         mock_get.return_value = {
#             "version": "2.0.0",
#         }
#         result = await version.check_version_2()
#         assert result == "2.0.0"


# @pytest.mark.asyncio
# async def test_check_version_3():
#     """Test check_version 3."""
#     with patch(
#         "systembridgeconnector.http_client.HTTPClient.get",
#         new_callable=AsyncMock,
#     ) as mock_get:
#         mock_get.return_value = {
#             "version": "3.0.0",
#         }
#         result = await version.check_version_3()
#         assert result == "3.0.0"
