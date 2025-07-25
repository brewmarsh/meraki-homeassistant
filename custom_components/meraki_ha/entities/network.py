"""Base network entity for Meraki networks."""

from __future__ import annotations

from typing import Any, Dict

from homeassistant.helpers.device_registry import DeviceInfo

from ...const import DOMAIN
from ...coordinators import MerakiDataUpdateCoordinator
from .base import MerakiEntity


class MerakiNetworkEntity(MerakiEntity):
    """Base entity for Meraki networks."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        network_data: Dict[str, Any],
        name: str,
        unique_id_suffix: str,
    ) -> None:
        """Initialize the network entity.

        Args:
            coordinator: The data update coordinator.
            network_data: Network data dictionary containing network information.
            name: The name of the entity.
            unique_id_suffix: Suffix to append to the network ID for a unique ID.
        """
        network_name = network_data.get("name", "Unknown Network")
        network_id = network_data.get("id", "")

        device_info = DeviceInfo(
            identifiers={(DOMAIN, network_id)},
            name=network_name,
            manufacturer="Cisco Meraki",
            model="Network",
        )

        super().__init__(
            coordinator=coordinator,
            name=name,
            unique_id=f"{network_id}_{unique_id_suffix}",
            device_info=device_info,
        )
        self._network_id = network_id

    def _get_network_data(self) -> Dict[str, Any] | None:
        """Get current network data from coordinator."""
        if not self.coordinator.data or "networks" not in self.coordinator.data:
            return None

        for network in self.coordinator.data["networks"]:
            if network.get("id") == self._network_id:
                return network

        return None
