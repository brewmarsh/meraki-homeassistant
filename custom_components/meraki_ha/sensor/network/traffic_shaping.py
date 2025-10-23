"""Platform for Meraki traffic shaping sensors."""

from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.entities.meraki_network_entity import MerakiNetworkEntity


class TrafficShapingSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], MerakiNetworkEntity, SensorEntity
):
    """Representation of a sensor that shows traffic shaping settings."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id)
        self._attr_unique_id = f"{network_id}-traffic-shaping"
        self._attr_name = "Traffic Shaping"
        self._attr_native_value = "Unknown"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return self._attr_native_value

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        traffic_shaping = self.coordinator.data.get("traffic_shaping", {}).get(
            self.network_id, {}
        )
        if traffic_shaping.get("enabled"):
            self._attr_native_value = "Enabled"
        else:
            self._attr_native_value = "Disabled"
        self.async_write_ha_state()
