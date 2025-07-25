"""Sensor for Meraki network information."""

import logging
from typing import Any, Dict

from ....entities import MerakiNetworkEntity

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkInfoSensor(MerakiNetworkEntity):
    """Representation of a Meraki Network Information Sensor."""

    _attr_icon = "mdi:information-outline"

    def __init__(
        self,
        coordinator,
        network_data: Dict[str, Any],
    ) -> None:
        """Initialize the network info sensor."""
        super().__init__(
            coordinator=coordinator,
            network_data=network_data,
            name="Network Information",
            unique_id_suffix="network_info",
        )
        self._update_state()

    def _update_state(self) -> None:
        """Update the state of the sensor."""
        current_network_data = self._get_network_data()

        if not current_network_data:
            self._attr_native_value = "Unknown"
            self._attr_extra_state_attributes = {}
            _LOGGER.debug(
                "Network %s not found in coordinator data for network info sensor.",
                self._network_id,
            )
            return

        self._attr_native_value = current_network_data.get("name", self._network_id)

        attributes = {
            "hostname": current_network_data.get("name"),
            "notes": current_network_data.get("notes"),
            "network_id": current_network_data.get("id"),
            "organization_id": current_network_data.get("organizationId"),
            "product_types": current_network_data.get("productTypes"),
            "tags": current_network_data.get("tags", []),
            "time_zone": current_network_data.get("timeZone"),
            "url": current_network_data.get("url"),
        }

        self._attr_extra_state_attributes = {
            k: v for k, v in attributes.items() if v is not None
        }
