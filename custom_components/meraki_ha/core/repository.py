"""Meraki Repository.

This module defines the MerakiRepository class, which is responsible for
interacting with the Meraki API client and handling data processing.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiRepository:
    """A repository for accessing Meraki data."""

    def __init__(self, api_client: MerakiAPIClient) -> None:
        """Initialize the MerakiRepository."""
        self._api_client = api_client

    async def async_reboot_device(self, serial: str) -> dict[str, Any] | None:
        """Reboot a device.

        Args:
            serial: The serial number of the device to reboot.

        Returns:
            A dictionary containing the API response, or None if an error occurred.

        """
        try:
            response = await self._api_client.async_reboot_device(serial)
            return response
        except Exception as e:
            _LOGGER.error("Failed to reboot device %s: %s", serial, e)
            return None

    async def async_get_switch_port_statuses(
        self, serial: str
    ) -> list[dict[str, Any]] | None:
        """Get statuses for all ports of a switch.

        Args:
            serial: The serial number of the switch.

        Returns:
            A list of port statuses, or None if an error occurred.

        """
        try:
            response = await self._api_client.async_get_switch_port_statuses(serial)
            return response
        except Exception as e:
            _LOGGER.error("Failed to get switch port statuses for %s: %s", serial, e)
            return None
