"""Switch entity for blocking/unblocking Meraki clients."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..core.coordinators.ssid_firewall_coordinator import SsidFirewallCoordinator
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiClientBlockerSwitch(
    CoordinatorEntity,  # type: ignore[type-arg]
    SwitchEntity,
):
    """Representation of a Meraki Client Blocker switch entity."""

    coordinator: SsidFirewallCoordinator
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
        self._client_ip = client_data.get("ip")
        self._client_mac = client_data["mac"]

        self.entity_description = SwitchEntityDescription(
            key=f"client_blocker_{self._client_mac}",
            name="Internet Access",
            icon="mdi:web-cancel",
        )

        self._attr_unique_id = f"meraki-client-{self._client_mac}-blocker"
        self._update_internal_state()

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
        return super().available and self.coordinator.data is not None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch based on firewall rules."""
        if not self.coordinator.data or not self._client_ip:
            self._attr_is_on = False
            return

        rules = self.coordinator.data.get("rules", [])
        is_blocked = any(
            rule.get("policy") == "deny" and self._client_ip in rule.get("value", "")
            for rule in rules
        )
        self._attr_is_on = is_blocked

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (block the client)."""
        if not self._client_ip:
            raise HomeAssistantError("Client IP address is not available.")
        try:
            await self.coordinator.async_block_client(self._client_ip)
        except Exception as e:
            _LOGGER.error(
                "Failed to block client %s: %s",
                self._client_mac,
                e,
            )
            raise HomeAssistantError(
                f"Failed to block client {self._client_mac}: {e}"
            ) from e

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (unblock the client)."""
        if not self._client_ip:
            raise HomeAssistantError("Client IP address is not available.")
        try:
            await self.coordinator.async_unblock_client(self._client_ip)
        except Exception as e:
            _LOGGER.error(
                "Failed to unblock client %s: %s",
                self._client_mac,
                e,
            )
            raise HomeAssistantError(
                f"Failed to unblock client {self._client_mac}: {e}"
            ) from e
