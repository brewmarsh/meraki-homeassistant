"""
Switch Port Service

This module defines the SwitchPortService class, which is responsible for
handling business logic related to switch ports.
"""
from __future__ import annotations
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..core.repository import MerakiRepository

_LOGGER = logging.getLogger(__name__)


class SwitchPortService:
    """A service for handling switch port logic."""

    def __init__(self, repository: MerakiRepository) -> None:
        """Initialize the SwitchPortService."""
        self._repository = repository

    async def async_get_ports_statuses(self, serial: str) -> list[dict[str, Any]] | None:
        """
        Get statuses for all ports of a switch.

        Args:
            serial: The serial number of the switch.

        Returns:
            A list of port statuses, or None if an error occurred.
        """
        return await self._repository.async_get_switch_port_statuses(serial)
