"""
Network Hub.

This module defines the NetworkHub class, which is responsible for
processing and managing data for a specific Meraki network.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...types import MerakiDevice, MerakiNetwork
    from ..coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class NetworkHub:
    """A hub for processing data for a specific network."""

    def __init__(
        self, coordinator: MerakiDataUpdateCoordinator, network_id: str
    ) -> None:
        """Initialize the NetworkHub."""
        self._coordinator = coordinator
        self.network_id = network_id

    @property
    def network_info(self) -> MerakiNetwork | None:
        """Return the network information dictionary."""
        return self._coordinator.get_network(self.network_id)

    @property
    def devices(self) -> list[MerakiDevice]:
        """Return a list of devices in this network."""
        if self._coordinator.data and self._coordinator.data.get("devices"):
            return [
                d
                for d in self._coordinator.data["devices"]
                if d.get("networkId") == self.network_id
            ]
        return []

    @property
    def ssids(self) -> list[dict[str, Any]]:
        """Return a list of SSIDs in this network."""
        if self._coordinator.data and self._coordinator.data.get("ssids"):
            return [
                s
                for s in self._coordinator.data["ssids"]
                if s.get("networkId") == self.network_id
            ]
        return []

    async def async_update_data(self) -> None:
        """
        Update network-specific data.

        This method is a placeholder. The hub's properties directly
        access the latest data from the coordinator, so a separate
        update method for the hub itself is not strictly necessary
        unless more complex, stateful processing is required.
        """
        _LOGGER.debug("Updating network hub data for %s", self.network_id)
        # No data to update here directly, as properties pull from the coordinator
        pass
