"""
Device Control Service.

This module defines the DeviceControlService class, which is responsible for
handling device-specific control actions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from ..core.repository import MerakiRepository

_LOGGER = MerakiLoggers.MAIN


class DeviceControlService:
    """A service for controlling Meraki devices."""

    def __init__(self, repository: MerakiRepository) -> None:
        """Initialize the DeviceControlService."""
        self._repository = repository

    async def async_reboot(self, serial: str) -> dict[str, Any] | None:
        """
        Reboot a device.

        Args:
        ----
            serial: The serial number of the device to reboot.

        Returns
        -------
            A dictionary containing the API response, or None if an error occurred.

        """
        _LOGGER.info("Requesting reboot for device %s", serial)
        return await self._repository.async_reboot_device(serial)
