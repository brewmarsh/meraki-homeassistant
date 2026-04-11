"""Sensor for Meraki network information."""

from __future__ import annotations

import logging
from typing import Any

from ....core.entities.meraki_network_entity import MerakiNetworkEntity
from ...coordinators import MerakiMainCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkInfoSensor(MerakiNetworkEntity):
    """Representation of a Meraki Network Information Sensor."""

    _attr_icon = "mdi:information-outline"

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        network_id: str,
    ) -> None:
        """
        Initialize the network info sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            network_id: The ID of the network.

        """
        network = coordinator.get_network(network_id)
        if not network:
            # Handle the case where network is not found
            raise ValueError(f"Network {network_id} not found")

        super().__init__(
            coordinator=coordinator,
            config_entry=coordinator.config_entry,  # type: ignore[arg-type]
            network=network,
        )
        self._attr_name = "Network Information"
        self._attr_unique_id = f"{network_id}_network_info"

    @property
    def native_value(self) -> str | None:
        """Return the network name."""
        if not self._network:
            return None
        return self._network.name

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self._network:
            return {}

        return {
            "hostname": self._network.name,
            "notes": self._network.notes,
            "network_id": self._network.id,
            "organization_id": self._network.organization_id,
            "product_types": self._network.product_types,
            "tags": self._network.tags,
            "time_zone": self._network.time_zone,
            "url": getattr(self._network, "url", None),
        }
