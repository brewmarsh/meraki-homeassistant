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
        self._vlans_cache: list[str] = []
        self._attr_native_value = 0
        self._update_state()

    def _update_state(self) -> None:
        """Update the state based on coordinator data."""
        self._vlans_cache = []
        self._attr_native_value = 0

        if not self._network:
            return

        vlans_data = self.coordinator.data.get("vlans", {})
        if not isinstance(vlans_data, dict):
            return

        vlans = vlans_data.get(self._network.id, [])
        if not isinstance(vlans, list):
            return

        self._attr_native_value = len(vlans)

        for vlan in vlans:
            if isinstance(vlan, dict) and "id" in vlan:
                self._vlans_cache.append(
                    vlan.get("name") or f"VLAN {vlan.get('id')}"
                )
            elif hasattr(vlan, "id"):
                name = getattr(vlan, "name", None) or f"VLAN {vlan.id}"
                self._vlans_cache.append(name)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attrs = super().extra_state_attributes
        attrs["vlans"] = self._vlans_cache
        return attrs

    @property
    def native_value(self) -> int:
        """Return the number of VLANs."""
        return self._attr_native_value
