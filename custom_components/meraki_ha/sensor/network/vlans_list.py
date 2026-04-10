"""Platform for Meraki VLAN list sensors."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory

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

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attrs = super().extra_state_attributes
        vlan_list = []
        if self._network:
            vlans_data = self.coordinator.data.get("vlans", {})
            if isinstance(vlans_data, dict):
                vlans = vlans_data.get(self._network.id, [])
                if isinstance(vlans, list):
                    for vlan in vlans:
                        if isinstance(vlan, dict) and "id" in vlan:
                            vlan_list.append(
                                vlan.get("name") or f"VLAN {vlan.get('id')}"
                            )
                        elif hasattr(vlan, "id"):
                            name = getattr(vlan, "name", None) or f"VLAN {vlan.id}"
                            vlan_list.append(name)
        attrs["vlans"] = vlan_list
        return attrs

    @property
    def native_value(self) -> int:
        """Return the number of VLANs."""
        if not self._network:
            return 0
        vlans_data = self.coordinator.data.get("vlans", {})
        if not isinstance(vlans_data, dict):
            return 0
        vlans = vlans_data.get(self._network.id, [])
        if not isinstance(vlans, list):
            return 0
        return len(vlans)
