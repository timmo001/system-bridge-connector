"""Test the websocket client module."""

# import asyncio
# from typing import Any
# from unittest.mock import patch

# import aiohttp
# import pytest
# from syrupy.assertion import SnapshotAssertion

# from systembridgeconnector.const import EventKey, EventType
# from systembridgeconnector.exceptions import (
#     ConnectionClosedException,
#     ConnectionErrorException,
# )
# from systembridgeconnector.websocket_client import WebSocketClient
# from systembridgemodels.keyboard_key import KeyboardKey
# from systembridgemodels.keyboard_text import KeyboardText
# from systembridgemodels.media_control import MediaControl
# from systembridgemodels.media_get_file import MediaGetFile
# from systembridgemodels.media_get_files import MediaGetFiles
# from systembridgemodels.modules import (
#     GetData,
#     Module,
#     ModulesData,
#     RegisterDataListener,
# )
# from systembridgemodels.notification import Notification
# from systembridgemodels.open_path import OpenPath
# from systembridgemodels.open_url import OpenUrl
# from systembridgemodels.response import Response
# from systembridgemodels.update import Update

# from . import API_HOST, API_PORT, REQUEST_ID, TOKEN, WebSocketGenerator

# modules_data = ModulesData()
