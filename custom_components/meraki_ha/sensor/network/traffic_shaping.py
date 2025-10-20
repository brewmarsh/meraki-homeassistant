from __future__ import annotations

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ...coordinator import MerakiDataUpdateCoordinator
from ...core.entities.meraki_network_entity import MerakiNetworkEntity

_LOGGER = logging.getLogger(__name__)


class MerakiTrafficShapingSensor(MerakiNetworkEntity, SensorEntity):
    """Representation of a Meraki network's traffic shaping sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_data)
        self._attr_unique_id = f"network_{self._network_id}_traffic_shaping"
        self._attr_name = "Traffic Shaping"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        traffic_shaping = self.coordinator.data.get("traffic_shaping", {}).get(
            self._network_id, {}
        )
        if traffic_shaping:
            self._attr_native_value = (
                "Enabled" if traffic_shaping.get("enabled") else "Disabled"
            )
            self._attr_extra_state_attributes = {
                "rules": traffic_shaping.get("rules", [])
            }
        else:
            self._attr_native_value = "Unknown"
            self._attr_extra_state_attributes = {"rules": []}

        self.async_write_ha_state()
