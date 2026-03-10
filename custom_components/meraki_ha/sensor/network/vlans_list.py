"""Platform for Meraki VLAN list sensors."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback

from ...coordinators import MerakiMainCoordinator
from ...core.entities.meraki_network_entity import MerakiNetworkEntity
from ...core.models.network import MerakiNetwork


class VlansListSensor(MerakiNetworkEntity, SensorEntity):
    """Representation of a sensor that lists all VLANs in a network."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        config_entry: ConfigEntry,
        network_data: MerakiNetwork,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_data)
        self._attr_unique_id = f"meraki-network-{network_data.id}-vlans-list"
        self._attr_name = f"{network_data.name} VLANs"
        self._vlan_list: list[str] = []
        self._attr_native_value = 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attrs = super().extra_state_attributes
        attrs["vlans"] = self._vlan_list
        return attrs

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self._network:
            return
        vlans_data = self.coordinator.data.get("vlans", {})
        if not isinstance(vlans_data, dict):
            return
        vlans = vlans_data.get(self._network.id, [])
        if not isinstance(vlans, list):
            return

        self._vlan_list = [
            getattr(vlan, "name", None) or f"VLAN {vlan.id}"
            for vlan in vlans
            if vlan and hasattr(vlan, "id")
        ]
        self._attr_native_value = len(self._vlan_list)
        self.async_write_ha_state()
