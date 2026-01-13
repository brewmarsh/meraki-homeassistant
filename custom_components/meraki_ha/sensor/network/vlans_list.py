"""Platform for Meraki VLAN list sensors."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

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
from ...types import MerakiNetwork


class VlansListSensor(MerakiNetworkEntity, SensorEntity):
    """Representation of a sensor that lists all VLANs in a network."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        config_entry: ConfigEntry,
        network_data: MerakiNetwork,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_data)
        self._attr_unique_id = f"{network_data['id']}_vlans"
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
        vlans = self.coordinator.data.get("vlans", {}).get(self._network["id"], [])
        self._vlan_list = [
            vlan.get("name") or f"VLAN {vlan.get('id')}" for vlan in vlans
        ]
        self._attr_native_value = len(vlans)
        self.async_write_ha_state()
