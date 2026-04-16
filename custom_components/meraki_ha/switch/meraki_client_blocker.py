"""Switch entity for blocking/unblocking Meraki clients."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo

from ..core.coordinators.ssid_firewall_coordinator import SsidFirewallCoordinator
from ..entity import MerakiSwitch
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiClientBlockerSwitch(MerakiSwitch):
    """Representation of a Meraki Client Blocker switch entity."""

    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        firewall_coordinator: SsidFirewallCoordinator,
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the Meraki Client Blocker switch entity."""
        super().__init__(firewall_coordinator)
        self._config_entry = config_entry
        self._client_data = client_data
        self._client_mac = client_data["mac"]
        self._network_id = client_data.get("networkId")

        self.entity_description = SwitchEntityDescription(
            key=f"client_blocker_{self._client_mac}",
            name="Internet Access",
            icon="mdi:web",
        )

        self._attr_unique_id = f"meraki-client-{self._client_mac}-blocker"
        self._update_internal_state()

    coordinator: SsidFirewallCoordinator

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information to link this entity to the client device."""
        return resolve_device_info(
            entity_data=self._client_data,
            config_entry=self._config_entry,
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.data is not None and super().available

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.coordinator.data is None:
            return
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch based on client policy."""
        if self.coordinator.is_pending(self.entity_description.key):
            return

        # Default to client_data policy or Normal if not known
        device_policy = self._client_data.get("devicePolicy", "Normal")

        if self.coordinator.data:
            clients = self.coordinator.data.get("clients", [])
            for client in clients:
                if client.get("mac") == self._client_mac:
                    device_policy = client.get("devicePolicy", "Normal")
                    break

        # ON = Normal (Internet Allowed), OFF = Blocked
        self._attr_is_on = device_policy == "Normal"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (unblock the client)."""
        if not self._network_id:
            raise HomeAssistantError("Network ID is not available.")

        old_state = self._attr_is_on
        self._attr_is_on = True
        self.async_write_ha_state()

        try:
            await self.coordinator.async_unblock_client(
                self._client_mac, self._network_id
            )
        except Exception as e:
            self._attr_is_on = old_state
            self.async_write_ha_state()
            _LOGGER.error("Failed to unblock client %s: %s", self._client_mac, e)
            raise HomeAssistantError(
                f"Failed to allow internet for {self._client_mac}: {e}"
            ) from e

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (block the client)."""
        if not self._network_id:
            raise HomeAssistantError("Network ID is not available.")

        old_state = self._attr_is_on
        self._attr_is_on = False
        self.async_write_ha_state()

        try:
            await self.coordinator.async_block_client(
                self._client_mac, self._network_id
            )
        except Exception as e:
            self._attr_is_on = old_state
            self.async_write_ha_state()
            _LOGGER.error("Failed to block client %s: %s", self._client_mac, e)
            raise HomeAssistantError(
                f"Failed to block internet for {self._client_mac}: {e}"
            ) from e
