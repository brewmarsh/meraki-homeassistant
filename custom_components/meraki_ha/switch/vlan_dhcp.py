"""Switch for a Meraki VLAN's DHCP handling."""

from __future__ import annotations

import logging
from typing import Any, Dict

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..coordinator import MerakiDataUpdateCoordinator
from ..core.entities.meraki_vlan_entity import MerakiVLANEntity
from ..core.utils.entity_id_utils import get_vlan_entity_id
from ..types import MerakiVlan

_LOGGER = logging.getLogger(__name__)


class MerakiVLANDHCPSwitch(MerakiVLANEntity, SwitchEntity):
    """Representation of a Meraki VLAN's DHCP handling switch."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        vlan: MerakiVlan,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        assert self._network_id, "Network ID cannot be None for a VLAN entity"
        vlan_id = self._vlan.get("id")
        assert vlan_id, "VLAN ID should not be None here"
        self._attr_unique_id = get_vlan_entity_id(
            self._network_id, vlan_id, "dhcp_handling"
        )
        self._attr_name = f"{self._vlan['name']} DHCP"
        self._update_internal_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch."""
        if self.coordinator.is_pending(self.unique_id):
            _LOGGER.debug(
                "Not updating state for %s because a pending update is registered",
                self.unique_id,
            )
            return
        self._attr_is_on = self._vlan.get("dhcpHandling") == "Run a DHCP server"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        vlans = self.coordinator.data.get("vlans", {}).get(self._network_id, [])
        for vlan in vlans:
            if vlan["id"] == self._vlan["id"]:
                self._vlan = vlan
                break
        self._update_internal_state()
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        self._attr_is_on = True
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)
        await self.coordinator.api.appliance.update_network_vlan(
            network_id=self._network_id,
            vlan_id=self._vlan["id"],
            dhcpHandling="Run a DHCP server",
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        self._attr_is_on = False
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)
        await self.coordinator.api.appliance.update_network_vlan(
            network_id=self._network_id,
            vlan_id=self._vlan["id"],
            dhcpHandling="Do not respond to DHCP requests",
        )
