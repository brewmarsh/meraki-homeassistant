"""
Switch Port Service.

This module defines the SwitchPortService class, which is responsible for
handling business logic related to switch ports.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from ..core.repository import MerakiRepository

_LOGGER = MerakiLoggers.SWITCH


class SwitchPortService:
    """A service for handling switch port logic."""

    def __init__(self, repository: MerakiRepository) -> None:
        """Initialize the SwitchPortService."""
        self._repository = repository

    async def async_get_ports_statuses(
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
        return await self._repository.async_get_switch_port_statuses(serial)

    async def async_get_port_status(self, serial: str, port_id: str) -> str | None:
        """
        Get the status for a specific port.

        Args:
        ----
            serial: The serial number of the switch.
            port_id: The ID of the port.

        Returns
        -------
            The status of the port ('Connected' or 'Disconnected'), or None if
            not found.

        """
        statuses = await self.async_get_ports_statuses(serial)
        if statuses:
            for port in statuses:
                if port.get("portId") == port_id:
                    return port.get("status")
        return None

    async def async_get_port_speed(self, serial: str, port_id: str) -> str | None:
        """
        Get the speed for a specific port.

        Args:
        ----
            serial: The serial number of the switch.
            port_id: The ID of the port.

        Returns
        -------
            The speed of the port, or None if not found.

        """
        statuses = await self.async_get_ports_statuses(serial)
        if statuses:
            for port in statuses:
                if port.get("portId") == port_id:
                    return port.get("speed")
        return None
