"""Sensor for Meraki network information."""

from __future__ import annotations

import logging
from typing import Any

from ....coordinator import MerakiDataUpdateCoordinator
from ....core.entities.network import MerakiNetworkEntity

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkInfoSensor(MerakiNetworkEntity):
    """Representation of a Meraki Network Information Sensor."""

    _attr_icon = "mdi:information-outline"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        network_id: str,
    ) -> None:
        """
        Initialize the network info sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            network_id: The ID of the network.

        """
        super().__init__(
            coordinator=coordinator,
            network_id=network_id,
            name="Network Information",
            unique_id_suffix="network_info",
        )

    @property
    def native_value(self) -> str | None:
        """Return the network name."""
        return self.network_data.get("name") if self.network_data else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self.network_data:
            return {}
        return {
            "hostname": self.network_data.get("name"),
            "notes": self.network_data.get("notes"),
            "network_id": self.network_data.get("id"),
            "organization_id": self.network_data.get("organizationId"),
            "product_types": self.network_data.get("productTypes"),
            "tags": self.network_data.get("tags", []),
            "time_zone": self.network_data.get("timeZone"),
            "url": self.network_data.get("url"),
        }
