"""
Meraki Repository.

This module defines the MerakiRepository class, which is responsible for
interacting with the Meraki API client and handling data processing.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .errors import ApiClientCommunicationError

if TYPE_CHECKING:
    from .api.client import MerakiApiClientProtocol

_LOGGER = logging.getLogger(__name__)


class MerakiRepository:
    """A repository for accessing Meraki data."""

    def __init__(self, api_client: MerakiApiClientProtocol) -> None:
        """Initialize the MerakiRepository."""
        self._api_client = api_client

    async def async_reboot_device(self, serial: str) -> dict[str, Any] | None:
        """
        Reboot a device.

        Args:
        ----
            serial: The serial number of the device to reboot.

        Returns
        -------
            A dictionary containing the API response, or None if an error occurred.

        """
        try:
            response = await self._api_client.async_reboot_device(serial)
            return response
        except ApiClientCommunicationError as e:
            _LOGGER.error("Failed to reboot device %s: %s", serial, e)
            return None

    async def async_get_switch_port_statuses(
        self, serial: str
    ) -> list[dict[str, Any]] | None:
        """
        Get statuses for all ports of a switch.

        Args:
        ----
            serial: The serial number of the switch.

        Returns
        -------
            A list of port statuses, or None if an error occurred.

        """
        try:
            response = await self._api_client.async_get_switch_port_statuses(serial)
            return response
        except ApiClientCommunicationError as e:
            _LOGGER.error("Failed to get switch port statuses for %s: %s", serial, e)
            return None

    async def async_cycle_switch_ports(
        self, serial: str, ports: list[str]
    ) -> dict[str, Any] | None:
        """
        Cycle a set of switch ports.

        Args:
        ----
            serial: The serial number of the switch.
            ports: A list of port IDs to cycle.

        Returns
        -------
            A dictionary containing the API response, or None if an error occurred.

        """
        try:
            response = await self._api_client.async_cycle_switch_ports(serial, ports)
            return response
        except Exception as e:
            _LOGGER.error("Failed to cycle switch ports for %s: %s", serial, e)
            return None

    async def async_get_appliance_ports(
        self, network_id: str
    ) -> list[dict[str, Any]] | None:
        """
        Get all ports of an appliance.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            A list of ports, or None if an error occurred.

        """
        try:
            response = await self._api_client.appliance.get_appliance_ports(network_id)
            return response
        except ApiClientCommunicationError as e:
            _LOGGER.error(
                "Failed to get appliance ports for network %s: %s", network_id, e
            )
            return None

    async def async_update_vpn_status(
        self, network_id: str, mode: str
    ) -> dict[str, Any] | None:
        """
        Update the site-to-site VPN status for a network.

        Args:
        ----
            network_id: The ID of the network.
            mode: The new VPN mode.

        Returns
        -------
            A dictionary containing the API response, or None if an error occurred.

        """
        try:
            response = await self._api_client.appliance.update_vpn_status(
                network_id, mode
            )
            return response
        except ApiClientCommunicationError as e:
            _LOGGER.error(
                "Failed to update VPN status for network %s: %s", network_id, e
            )
            return None
