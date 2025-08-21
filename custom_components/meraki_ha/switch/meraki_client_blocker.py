"""Switch entity for blocking/unblocking Meraki clients."""

import logging
from typing import Any, Dict

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory

from ..core.coordinators.client_firewall_coordinator import (
    ClientFirewallCoordinator,
    FIREWALL_RULE_COMMENT,
)
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiClientBlockerSwitch(
    CoordinatorEntity[ClientFirewallCoordinator], SwitchEntity
):
    """Representation of a Meraki Client Blocker switch entity."""

    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ClientFirewallCoordinator,
        config_entry: ConfigEntry,
        client_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki Client Blocker switch entity."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._client_data = client_data
        self._client_ip = client_data["ip"]
        self._client_mac = client_data["mac"]
        self._vlan = client_data.get("vlan")
        self._ssid = client_data.get("ssid")

        self.entity_description = SwitchEntityDescription(
            key=f"client_blocker_{self._client_mac}",
            name="Internet Access",
            icon="mdi:web-cancel",
        )

        self._attr_unique_id = f"meraki-client-{self._client_mac}-blocker"
        self._update_internal_state()

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        return {"vlan": self._vlan, "ssid": self._ssid}

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information to link this entity to the client device."""
        return resolve_device_info(
            entity_data=self._client_data,
            config_entry=self._config_entry,
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and self.coordinator.data is not None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch based on firewall rules."""
        if self.coordinator.data:
            rules = (
                self.coordinator.data.get("l7_firewall_rules", {}).get("rules", [])
            )
            self._attr_is_on = any(
                r.get("value") == self._client_ip
                and r.get("comment") == FIREWALL_RULE_COMMENT
                for r in rules
            )
        else:
            self._attr_is_on = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (block the client)."""
        await self.coordinator.async_block_client(self._client_ip)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (unblock the client)."""
        await self.coordinator.async_unblock_client(self._client_ip)
