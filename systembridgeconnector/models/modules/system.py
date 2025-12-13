"""System."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ..helpers import filter_unexpected_fields


class RunMode(StrEnum):
    """Run Mode."""

    STANDALONE = "standalone"


@filter_unexpected_fields
@dataclass(slots=True)
class SystemUser:
    """System User."""

    name: str
    active: bool
    terminal: str
    host: str
    started: int
    pid: float


@filter_unexpected_fields
@dataclass(slots=True)
class System:
    """System."""

    boot_time: int
    fqdn: str
    hostname: str
    kernel_version: str
    ip_address_4: str
    mac_address: str
    platform_version: str
    platform: str
    uptime: int
    users: list[SystemUser]
    uuid: str
    version: str
    camera_usage: list[str] | None = None
    ip_address_6: str | None = None
    pending_reboot: bool | None = None
    power_usage: float | None = None
    run_mode: RunMode | None = None
    version_latest_url: str | None = None
    version_latest: str | None = None
    version_newer_available: bool | None = None

