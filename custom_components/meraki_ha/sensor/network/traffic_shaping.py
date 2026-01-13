"""Platform for Meraki traffic shaping sensors."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

<<<<<<< HEAD
<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.entities.meraki_network_entity import MerakiNetworkEntity
=======
<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.entities.meraki_network_entity import MerakiNetworkEntity
=======
from ...core.entities.meraki_network_entity import MerakiNetworkEntity
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
from ...core.entities.meraki_network_entity import MerakiNetworkEntity
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
from ...types import MerakiNetwork


class TrafficShapingSensor(MerakiNetworkEntity, SensorEntity):
    """Representation of a sensor that shows traffic shaping settings."""

    def __init__(
        self,
<<<<<<< HEAD
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        config_entry: ConfigEntry,
        network_id: str,
    ) -> None:
        """Initialize the sensor."""
        network: MerakiNetwork | None = next(
            (net for net in coordinator.data["networks"] if net["id"] == network_id),
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
