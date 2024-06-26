"""Version."""

from __future__ import annotations

from aiohttp import ClientSession
from packaging.version import parse

from systembridgemodels.modules.system import System

from .base import Base
from .exceptions import ConnectionErrorException
from .http_client import HTTPClient

SUPPORTED_VERSION = "4.0.2"


class Version(Base):
    """Version."""

    def __init__(
        self,
        api_host: str,
        api_port: int,
        token: str,
        session: ClientSession | None = None,
    ) -> None:
        """Initialise the client."""
        super().__init__()
        self._http_client = HTTPClient(
            api_host,
            api_port,
            token,
            session,
        )

    async def check_supported(self) -> bool:
        """Check if the system is running a supported version."""
        if (
            await self.check_version_2() is None
            and (version := await self.check_version()) is not None
        ):
            return parse(version) >= parse(SUPPORTED_VERSION)
        return False

    async def check_version_2(self) -> str | None:
        """Check if the system version for v2.x.x versions."""
        try:
            information = await self._http_client.get("/information")
            if (
                information
                and information.get("version")
                and (
                    information.get("version").startswith("2")
                    or information.get("version").startswith("v2")
                )
            ):
                return information["version"]
        except ConnectionErrorException as exception:
            error: dict = exception.args[0]
            if (
                error is not None  # pylint: disable=invalid-sequence-index
                and error["status"] == 404  # pylint: disable=invalid-sequence-index
            ):
                return None
            raise exception

    async def check_version(self) -> str | None:
        """Check the system version for 3.x.x and above."""
        try:
            response = await self._http_client.get("/api/data/system")
            system = System(**response)
            if (
                system
                and system.version is not None
                and parse(system.version) >= parse("3.0.0")
            ):
                return system.version
        except ConnectionErrorException as exception:
            error: dict = exception.args[0]
            if (
                error is not None  # pylint: disable=invalid-sequence-index
                and error["status"] == 404  # pylint: disable=invalid-sequence-index
            ):
                return None
            raise exception
