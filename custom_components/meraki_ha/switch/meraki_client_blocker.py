"""Switch entity for blocking/unblocking Meraki clients."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory

from ..core.api.client import MerakiAPIClient
from ..core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)

FIREWALL_RULE_COMMENT = "Managed by Home Assistant Meraki Integration"


class MerakiClientBlockerSwitch(CoordinatorEntity[MerakiDataCoordinator], SwitchEntity):
    """Representation of a Meraki Client Blocker switch entity."""

    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        network_id: str,
        client_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki Client Blocker switch entity."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry
        self._network_id = network_id
        self._client_data = client_data
        self._client_mac = client_data["mac"]

        self.entity_description = SwitchEntityDescription(
            key=f"client_blocker_{self._client_mac}",
            name="Internet Access",
            icon="mdi:web-cancel",
        )

        self._attr_unique_id = f"meraki-client-{self._client_mac}-blocker"
        self._update_internal_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information to link this entity to the client device."""
        # This assumes that client devices are already created elsewhere.
        # If not, we would need to create them here.
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
        # This is complex. We need to check if a blocking rule exists for this client.
        # For now, we'll assume the switch is off (not blocked) by default.
        # A proper implementation would fetch the firewall rules and check for a rule
        # that blocks this client's IP.
        self._attr_is_on = False  # Placeholder

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (block the client)."""
        await self._update_firewall_rule(block=True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (unblock the client)."""
        await self._update_firewall_rule(block=False)

    async def _update_firewall_rule(self, block: bool) -> None:
        """Add or remove a firewall rule to block the client."""
        try:
            # Get the current L7 firewall rules
            ruleset = (
                await self._meraki_client.appliance.get_network_appliance_firewall_l7_firewall_rules(
                    networkId=self._network_id
                )
            )
            rules = ruleset.get("rules", [])

            # Filter out our managed rules for this client
            new_rules = [
                r
                for r in rules
                if not (
                    r.get("comment") == FIREWALL_RULE_COMMENT
                    and self._client_data["ip"] in r.get("value", "")
                )
            ]

            if block:
                # Add a new rule to block this client
                new_rules.append(
                    {
                        "policy": "deny",
                        "type": "host",
                        "value": self._client_data["ip"],
                        "comment": FIREWALL_RULE_COMMENT,
                    }
                )

            # Update the firewall rules
            await self._meraki_client.appliance.update_network_appliance_firewall_l7_firewall_rules(
                networkId=self._network_id, rules=new_rules
            )

            self._attr_is_on = block
            self.async_write_ha_state()
            await self.coordinator.async_request_refresh()

        except Exception as e:
            _LOGGER.error(
                "Failed to update firewall rule for client %s: %s",
                self._client_mac,
                e,
            )
            raise HomeAssistantError(
                f"Failed to update firewall rule for client {self._client_mac}: {e}"
            ) from e
