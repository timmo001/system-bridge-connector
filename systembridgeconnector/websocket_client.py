"""WebSocket Client."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import asdict
import socket
from typing import Any
from uuid import uuid4

import aiohttp

from systembridgemodels.const import MODEL_MAP, MODEL_RESPONSE
from systembridgemodels.keyboard_key import KeyboardKey
from systembridgemodels.keyboard_text import KeyboardText
from systembridgemodels.media_control import MediaControl
from systembridgemodels.media_directories import MediaDirectory
from systembridgemodels.media_files import MediaFile, MediaFiles
from systembridgemodels.media_get_file import MediaGetFile
from systembridgemodels.media_get_files import MediaGetFiles
from systembridgemodels.modules import GetData, RegisterDataListener
from systembridgemodels.notification import Notification
from systembridgemodels.open_path import OpenPath
from systembridgemodels.open_url import OpenUrl
from systembridgemodels.request import Request
from systembridgemodels.response import Response
from systembridgemodels.update import Update

from .base import Base
from .const import (
    EVENT_DATA,
    EVENT_ID,
    EVENT_MESSAGE,
    EVENT_MODULE,
    EVENT_SUBTYPE,
    EVENT_TYPE,
    SUBTYPE_BAD_TOKEN,
    SUBTYPE_LISTENER_ALREADY_REGISTERED,
    TYPE_APPLICATION_UPDATE,
    TYPE_DATA_GET,
    TYPE_DATA_LISTENER_REGISTERED,
    TYPE_DATA_UPDATE,
    TYPE_DIRECTORIES,
    TYPE_ERROR,
    TYPE_EXIT_APPLICATION,
    TYPE_FILE,
    TYPE_FILES,
    TYPE_GET_DATA,
    TYPE_GET_DIRECTORIES,
    TYPE_GET_FILE,
    TYPE_GET_FILES,
    TYPE_KEYBOARD_KEY_PRESSED,
    TYPE_KEYBOARD_KEYPRESS,
    TYPE_KEYBOARD_TEXT,
    TYPE_KEYBOARD_TEXT_SENT,
    TYPE_MEDIA_CONTROL,
    TYPE_NOTIFICATION,
    TYPE_NOTIFICATION_SENT,
    TYPE_OPEN,
    TYPE_OPENED,
    TYPE_POWER_HIBERNATE,
    TYPE_POWER_HIBERNATING,
    TYPE_POWER_LOCK,
    TYPE_POWER_LOCKING,
    TYPE_POWER_LOGGINGOUT,
    TYPE_POWER_LOGOUT,
    TYPE_POWER_RESTART,
    TYPE_POWER_RESTARTING,
    TYPE_POWER_SHUTDOWN,
    TYPE_POWER_SHUTTINGDOWN,
    TYPE_POWER_SLEEP,
    TYPE_POWER_SLEEPING,
    TYPE_REGISTER_DATA_LISTENER,
)
from .exceptions import (
    AuthenticationException,
    BadMessageException,
    ConnectionClosedException,
    ConnectionErrorException,
)


class WebSocketClient(Base):
    """WebSocket Client."""

    def __init__(
        self,
        api_host: str,
        api_port: int,
        token: str,
    ) -> None:
        """Initialise."""
        super().__init__()
        self._api_host = api_host
        self._api_port = api_port
        self._token = token
        self._responses: dict[str, tuple[asyncio.Future[Response], str | None]] = {}
        self._session: aiohttp.ClientSession | None = None
        self._websocket: aiohttp.ClientWebSocketResponse | None = None

    @property
    def connected(self) -> bool:
        """Get connection state."""
        return self._websocket is not None and not self._websocket.closed

    async def _send_message(
        self,
        event: str,
        request_id: str,
        data: dict[str, Any],
        wait_for_response: bool,
        response_type: str | None = None,
    ) -> Response:
        """Send a message to the WebSocket."""
        if not self.connected or self._websocket is None:
            raise ConnectionClosedException("Connection is closed")

        request = Request(
            token=self._token,
            id=request_id,
            event=event,
            data=data,
        )

        future: asyncio.Future[Response] = asyncio.get_running_loop().create_future()
        self._responses[request.id] = future, response_type
        await self._websocket.send_json(asdict(request))
        self._logger.debug("Sent message: %s", request)
        print("Sent message:", request)

        if wait_for_response:
            try:
                # if the future is already done, return the result
                if future.done():
                    self._logger.info("Future is done: %s", request.id)
                    print("Future is done:", request.id)
                    return future.result()
                # if the future is cancelled, return a cancelled response
                if future.cancelled():
                    self._logger.info("Future is cancelled: %s", request.id)
                    print("Future is cancelled")
                    return Response(
                        id=request.id,
                        type="N/A",
                        message="Message cancelled",
                        subtype=None,
                        module=None,
                        data={},
                    )
                # otherwise, await the future
                self._logger.info(
                    "Awaiting future: %s (%s)",
                    request.id,
                    response_type,
                )
                print(
                    "Awaiting future:",
                    request.id,
                    response_type,
                )
                return await future
            finally:
                self._responses.pop(request.id)
        return Response(
            id=request.id,
            type="N/A",
            message="Message sent",
            subtype=None,
            module=None,
            data={},
        )

    async def close(
        self,
        keep_session_active: bool = False,
    ) -> None:
        """Close connection."""
        self._logger.info("Closing WebSocket connection")
        if self._websocket is not None:
            await self._websocket.close()
        if self._session is not None and not keep_session_active:
            await self._session.close()

    async def connect(
        self,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Connect to server."""
        if session:
            self._session = session
        else:
            self._logger.info("Creating new aiohttp client session")
            self._session = aiohttp.ClientSession()
        url = f"ws://{self._api_host}:{self._api_port}/api/websocket"
        self._logger.info(
            "Connecting to WebSocket: %s (aiohttp: %s)",
            url,
            aiohttp.__version__,
        )
        try:
            self._websocket = await self._session.ws_connect(url=url, heartbeat=30)
        except (
            aiohttp.WSServerHandshakeError,
            aiohttp.ClientConnectionError,
            socket.gaierror,
        ) as error:
            self._logger.warning(
                "Failed to connect to WebSocket: %s - %s",
                error.__class__.__name__,
                error,
            )
            raise ConnectionErrorException from error
        self._logger.info("Connected to WebSocket")

    async def application_update(
        self,
        model: Update,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Update application."""
        self._logger.info("Updating application")
        return await self._send_message(
            TYPE_APPLICATION_UPDATE,
            request_id,
            asdict(model),
            wait_for_response=False,
        )

    async def exit_backend(
        self,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Exit backend."""
        self._logger.info("Exiting backend")
        return await self._send_message(
            TYPE_EXIT_APPLICATION,
            request_id,
            {},
            wait_for_response=False,
        )

    async def get_data(
        self,
        model: GetData,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Get data from server."""
        self._logger.info("Getting data from server: %s", model)
        print("Getting data from server:", model)
        return await self._send_message(
            TYPE_GET_DATA,
            request_id,
            asdict(model),
            wait_for_response=True,
            response_type=TYPE_DATA_GET,
        )

    async def get_directories(
        self,
        request_id: str = uuid4().hex,
    ) -> list[MediaDirectory]:
        """Get directories."""
        print("Getting directories..")
        self._logger.info("Getting directories..")
        response = await self._send_message(
            TYPE_GET_DIRECTORIES,
            request_id,
            {},
            wait_for_response=True,
            response_type=TYPE_DIRECTORIES,
        )
        return [
            MediaDirectory(
                key=getattr(directory, "key"),
                path=getattr(directory, "path"),
            )
            for directory in response.data
        ]

    async def get_files(
        self,
        model: MediaGetFiles,
        request_id: str = uuid4().hex,
    ) -> MediaFiles:
        """Get files."""
        self._logger.info("Getting files: %s", model)
        response = await self._send_message(
            TYPE_GET_FILES,
            request_id,
            asdict(model),
            wait_for_response=True,
            response_type=TYPE_FILES,
        )

        files = getattr(response.data, "files")
        path = getattr(response.data, "path")
        return MediaFiles(
            files=files if files is not None else [],
            path=path if path is not None else "",
        )

    async def get_file(
        self,
        model: MediaGetFile,
        request_id: str = uuid4().hex,
    ) -> MediaFile:
        """Get files."""
        self._logger.info("Getting file: %s", model)
        response = await self._send_message(
            TYPE_GET_FILE,
            request_id,
            asdict(model),
            wait_for_response=True,
            response_type=TYPE_FILE,
        )
        return MediaFile(
            name=getattr(response.data, "name"),
            path=getattr(response.data, "path"),
            fullpath=getattr(response.data, "fullpath"),
            size=getattr(response.data, "size"),
            last_accessed=getattr(response.data, "last_accessed"),
            created=getattr(response.data, "created"),
            modified=getattr(response.data, "modified"),
            is_directory=getattr(response.data, "is_directory"),
            is_file=getattr(response.data, "is_file"),
            is_link=getattr(response.data, "is_link"),
            mime_type=getattr(response.data, "mime_type"),
        )

    async def register_data_listener(
        self,
        model: RegisterDataListener,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Register data listener."""
        self._logger.info("Registering data listener: %s", model)
        return await self._send_message(
            TYPE_REGISTER_DATA_LISTENER,
            request_id,
            asdict(model),
            wait_for_response=True,
            response_type=TYPE_DATA_LISTENER_REGISTERED,
        )

    async def keyboard_keypress(
        self,
        model: KeyboardKey,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Keyboard keypress."""
        self._logger.info("Press key: %s", model)
        return await self._send_message(
            TYPE_KEYBOARD_KEYPRESS,
            request_id,
            asdict(model),
            wait_for_response=True,
            response_type=TYPE_KEYBOARD_KEY_PRESSED,
        )

    async def keyboard_text(
        self,
        model: KeyboardText,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Keyboard keypress."""
        self._logger.info("Enter text: %s", model)
        return await self._send_message(
            TYPE_KEYBOARD_TEXT,
            request_id,
            asdict(model),
            wait_for_response=True,
            response_type=TYPE_KEYBOARD_TEXT_SENT,
        )

    async def media_control(
        self,
        model: MediaControl,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Media control."""
        self._logger.info("Media control: %s", model)
        return await self._send_message(
            TYPE_MEDIA_CONTROL,
            request_id,
            asdict(model),
            wait_for_response=False,
        )

    async def send_notification(
        self,
        model: Notification,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Send notification."""
        self._logger.info("Send notification: %s", model)
        return await self._send_message(
            TYPE_NOTIFICATION,
            request_id,
            asdict(model),
            wait_for_response=True,
            response_type=TYPE_NOTIFICATION_SENT,
        )

    async def open_path(
        self,
        model: OpenPath,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Open path."""
        self._logger.info("Opening path: %s", model)
        return await self._send_message(
            TYPE_OPEN,
            request_id,
            asdict(model),
            wait_for_response=True,
            response_type=TYPE_OPENED,
        )

    async def open_url(
        self,
        model: OpenUrl,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Open url."""
        self._logger.info("Opening URL: %s", model)
        return await self._send_message(
            TYPE_OPEN,
            request_id,
            asdict(model),
            wait_for_response=True,
            response_type=TYPE_OPENED,
        )

    async def power_sleep(
        self,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Power sleep."""
        self._logger.info("Power sleep")
        return await self._send_message(
            TYPE_POWER_SLEEP,
            request_id,
            {},
            wait_for_response=True,
            response_type=TYPE_POWER_SLEEPING,
        )

    async def power_hibernate(
        self,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Power hibernate."""
        self._logger.info("Power hibernate")
        return await self._send_message(
            TYPE_POWER_HIBERNATE,
            request_id,
            {},
            wait_for_response=True,
            response_type=TYPE_POWER_HIBERNATING,
        )

    async def power_restart(
        self,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Power restart."""
        self._logger.info("Power restart")
        return await self._send_message(
            TYPE_POWER_RESTART,
            request_id,
            {},
            wait_for_response=True,
            response_type=TYPE_POWER_RESTARTING,
        )

    async def power_shutdown(
        self,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Power shutdown."""
        self._logger.info("Power shutdown")
        return await self._send_message(
            TYPE_POWER_SHUTDOWN,
            request_id,
            {},
            wait_for_response=True,
            response_type=TYPE_POWER_SHUTTINGDOWN,
        )

    async def power_lock(
        self,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Power lock."""
        self._logger.info("Power lock")
        return await self._send_message(
            TYPE_POWER_LOCK,
            request_id,
            {},
            wait_for_response=True,
            response_type=TYPE_POWER_LOCKING,
        )

    async def power_logout(
        self,
        request_id: str = uuid4().hex,
    ) -> Response:
        """Power logout."""
        self._logger.info("Power logout")
        return await self._send_message(
            TYPE_POWER_LOGOUT,
            request_id,
            {},
            wait_for_response=True,
            response_type=TYPE_POWER_LOGGINGOUT,
        )

    async def listen(
        self,
        callback: Callable[[str, Any], Awaitable[None]] | None = None,
        accept_other_types: bool = False,
    ) -> None:
        """Listen for messages and map to modules."""

        async def _callback_message(message: dict) -> None:
            """Message Callback."""
            self._logger.debug("New message: %s", message[EVENT_TYPE])

            if (
                message.get(EVENT_ID) is not None
                and (response_tuple := self._responses.get(message[EVENT_ID]))
                is not None
            ):
                future, response_type = response_tuple
                if response_type is not None and response_type != message[EVENT_TYPE]:
                    self._logger.info(
                        "Response type '%s' does not match requested type '%s'.",
                        message[EVENT_TYPE],
                        response_type,
                    )
                else:
                    response = Response(**message)

                    if (
                        response.type == TYPE_DATA_UPDATE
                        and response.module is not None
                        and message[EVENT_DATA] is not None
                    ):
                        # Find model from module
                        model = MODEL_MAP.get(message[EVENT_MODULE])
                        if model is None:
                            self._logger.warning(
                                "Unknown model: %s", message[EVENT_MODULE]
                            )
                        else:
                            self._logger.debug(
                                "Mapping data to model: %s", model.__name__
                            )
                            if isinstance(message[EVENT_DATA], list):
                                response.data = [
                                    model(**data) for data in message[EVENT_DATA]
                                ]
                            else:
                                response.data = model(**message[EVENT_DATA])

                    self._logger.info("Response: %s", response)

                    try:
                        future.set_result(response)
                    except asyncio.InvalidStateError:
                        self._logger.debug(
                            "Future already set for response ID: %s",
                            message[EVENT_ID],
                        )

            if message[EVENT_TYPE] == TYPE_ERROR:
                if message[EVENT_SUBTYPE] == SUBTYPE_LISTENER_ALREADY_REGISTERED:
                    self._logger.debug(message)
                elif (
                    message[EVENT_SUBTYPE] == SUBTYPE_BAD_TOKEN
                    or message[EVENT_SUBTYPE] == "BAD_API_KEY"
                ):
                    self._logger.error(message)
                    raise AuthenticationException(message[EVENT_MESSAGE])
                else:
                    self._logger.warning("Error message: %s", message)
            elif (
                message[EVENT_TYPE] == TYPE_DATA_UPDATE
                and message[EVENT_DATA] is not None
            ):
                self._logger.debug(
                    "New data for: %s\n%s", message[EVENT_MODULE], message[EVENT_DATA]
                )
                model = MODEL_MAP.get(message[EVENT_MODULE])
                if model is None:
                    self._logger.warning("Unknown model: %s", message[EVENT_MODULE])
                elif callback is not None:
                    await callback(
                        message[EVENT_MODULE],
                        [model(**data) for data in message[EVENT_DATA]]
                        if isinstance(message[EVENT_DATA], list)
                        else model(**message[EVENT_DATA]),
                    )
            else:
                self._logger.debug("Other message: %s", message[EVENT_TYPE])
                if accept_other_types:
                    model = MODEL_MAP.get(EVENT_TYPE, MODEL_MAP[MODEL_RESPONSE])
                    if model is not None and callback is not None:
                        await callback(
                            message[EVENT_TYPE],
                            model(**message),
                        )

        await self.listen_for_messages(callback=_callback_message)

    async def listen_for_messages(
        self,
        callback: Callable[[dict[Any, Any]], Awaitable[None]],
    ) -> None:
        """Listen for messages."""
        if not self.connected:
            raise ConnectionClosedException("Connection is closed")

        self._logger.info("Listen for messages")
        if self._websocket is not None:
            while not self._websocket.closed:
                message = await self.receive_message()
                if isinstance(message, dict):
                    await callback(message)

    async def receive_message(self) -> dict | None:
        """Receive message."""
        if not self.connected or self._websocket is None:
            raise ConnectionClosedException("Connection is closed")

        try:
            message = await self._websocket.receive()
        except RuntimeError:
            return None

        if message.type == aiohttp.WSMsgType.ERROR:
            raise ConnectionErrorException(self._websocket.exception())

        if message.type in (
            aiohttp.WSMsgType.CLOSE,
            aiohttp.WSMsgType.CLOSED,
            aiohttp.WSMsgType.CLOSING,
        ):
            raise ConnectionClosedException("Connection closed to server")

        if message.type == aiohttp.WSMsgType.TEXT:
            message_json = message.json()

            if message_json[EVENT_TYPE] == TYPE_ERROR and (
                message_json[EVENT_SUBTYPE] == SUBTYPE_BAD_TOKEN
                or message_json[EVENT_SUBTYPE] == "BAD_API_KEY"
            ):
                raise AuthenticationException(message_json[EVENT_MESSAGE])

            return message_json

        raise BadMessageException(f"Unknown message type: {message.type}")
