"""Platform for Meraki VLAN list sensors."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.entities.meraki_network_entity import MerakiNetworkEntity
from ...core.utils.naming_utils import format_entity_name
=======
from ...core.entities.meraki_network_entity import MerakiNetworkEntity
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
from ...types import MerakiNetwork


class VlansListSensor(MerakiNetworkEntity, SensorEntity):
    """Representation of a sensor that lists all VLANs in a network."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
        config_entry: ConfigEntry,
        network_data: MerakiNetwork,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_data)
<<<<<<< HEAD
        self._attr_unique_id = f"{network_data.id}_vlans"
=======
        self._attr_unique_id = f"{network_data['id']}_vlans"
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
        self._attr_name = "VLANs"
        self._vlan_list: list[str] = []
        self._attr_native_value = 0

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {"vlans": self._vlan_list}

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
<<<<<<< HEAD
        vlans = self.coordinator.data.get("vlans", {}).get(self._network.id, [])
=======
        vlans = self.coordinator.data.get("vlans", {}).get(self._network["id"], [])
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
        self._vlan_list = [
            vlan.get("name") or f"VLAN {vlan.get('id')}" for vlan in vlans
        ]
        self._attr_native_value = len(vlans)
        self.async_write_ha_state()
