"""Platform for Meraki traffic shaping sensors."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

<<<<<<< HEAD
from ...core.entities.meraki_network_entity import MerakiNetworkEntity
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.entities.meraki_network_entity import MerakiNetworkEntity
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from ...types import MerakiNetwork


class TrafficShapingSensor(MerakiNetworkEntity, SensorEntity):
    """Representation of a sensor that shows traffic shaping settings."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
=======
        coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        config_entry: ConfigEntry,
        network_id: str,
    ) -> None:
        """Initialize the sensor."""
        network: MerakiNetwork | None = next(
<<<<<<< HEAD
            (net for net in coordinator.data["networks"] if net["id"] == network_id),
=======
            (
                net
                for net in coordinator.data["networks"]
                if net.id == network_id
            ),
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            None,
        )
        assert network is not None

        super().__init__(coordinator, config_entry, network)
        self._attr_unique_id = f"{network_id}-traffic-shaping"
        self._attr_name = "Traffic Shaping"
        self._attr_native_value = "Unknown"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        traffic_shaping = self.coordinator.data.get("traffic_shaping", {}).get(
            self._network_id, {}
        )
        if traffic_shaping.get("enabled"):
            self._attr_native_value = "Enabled"
        else:
            self._attr_native_value = "Disabled"
        self.async_write_ha_state()
