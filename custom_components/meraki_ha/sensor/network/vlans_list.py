"""Platform for Meraki VLAN list sensors."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ...coordinator import MerakiDataUpdateCoordinator
from ...core.entities.meraki_network_entity import MerakiNetworkEntity
from ...types import MerakiNetwork


class VlansListSensor(MerakiNetworkEntity, SensorEntity):
    """Representation of a sensor that lists all VLANs in a network."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_data: MerakiNetwork,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_data)
        self._attr_unique_id = f"{network_data['id']}_vlans"
        self._attr_name = "VLANs"
        self._attr_native_value: list[str] = []

    @property
    def native_value(self) -> int:
        """Return the number of VLANs."""
        return len(self._attr_native_value)

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {"vlans": self._attr_native_value}

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        vlans = self.coordinator.data.get("vlans", {}).get(self._network["id"], [])
        self._attr_native_value = [
            vlan.get("name") for vlan in vlans if vlan.get("name")
        ]
        self.async_write_ha_state()
