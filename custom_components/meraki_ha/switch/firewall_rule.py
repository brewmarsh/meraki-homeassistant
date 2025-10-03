"""Switch for a Meraki L3 Firewall Rule."""

from __future__ import annotations

import logging
from typing import Any, cast

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..coordinator import MerakiDataUpdateCoordinator
from ..core.entities.meraki_firewall_rule_entity import MerakiFirewallRuleEntity
from ..core.utils.entity_id_utils import get_firewall_rule_entity_id
from ..types import MerakiFirewallRule

_LOGGER = logging.getLogger(__name__)


class MerakiFirewallRuleSwitch(MerakiFirewallRuleEntity, SwitchEntity):
    """Representation of a Meraki L3 Firewall Rule switch."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        rule: MerakiFirewallRule,
        rule_index: int,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, config_entry, network_id, rule, rule_index)
        assert self._network_id, "Network ID cannot be None for a firewall rule entity"
        self._attr_unique_id = get_firewall_rule_entity_id(
            self._network_id, self._rule_index
        )
        self._attr_name = self._rule.get("comment", f"Rule {self._rule_index + 1}")
        self._update_internal_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch."""
        if self.coordinator.is_pending(self.unique_id):
            _LOGGER.debug(
                "Not updating state for %s because a pending update is registered",
                self.unique_id,
            )
            return
        self._attr_is_on = self._rule.get("policy") == "allow"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        rules = (
            self.coordinator.data.get("l3_firewall_rules", {})
            .get(self._network_id, {})
            .get("rules", [])
        )
        if len(rules) > self._rule_index:
            self._rule = cast(MerakiFirewallRule, rules[self._rule_index])
            self._update_internal_state()
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        self._attr_is_on = True
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)
        rules = (
            self.coordinator.data.get("l3_firewall_rules", {})
            .get(self._network_id, {})
            .get("rules", [])
        )
        rules[self._rule_index]["policy"] = "allow"
        await self.coordinator.api.appliance.update_l3_firewall_rules(
            network_id=self._network_id, rules=rules
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        self._attr_is_on = False
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)
        rules = (
            self.coordinator.data.get("l3_firewall_rules", {})
            .get(self._network_id, {})
            .get("rules", [])
        )
        rules[self._rule_index]["policy"] = "deny"
        await self.coordinator.api.appliance.update_l3_firewall_rules(
            network_id=self._network_id, rules=rules
        )
