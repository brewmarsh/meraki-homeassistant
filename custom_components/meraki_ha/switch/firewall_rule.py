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
        """
        Initialize the switch.

        Args:
        ----
            coordinator: The data update coordinator.
            config_entry: The config entry.
            network_id: The ID of the network.
            rule: The firewall rule.
            rule_index: The index of the rule.

        """
        super().__init__(coordinator, config_entry, network_id, rule, rule_index)
        if not self._network_id:
            raise ValueError("Network ID cannot be None for a firewall rule entity")
        self._attr_unique_id = get_firewall_rule_entity_id(
            self._network_id,
            self._rule_index,
        )
        self._attr_has_entity_name = True
        self._attr_name = self._rule.comment or f"Rule {self._rule_index + 1}"
        self._update_internal_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch."""
        if self.coordinator.is_pending(self.unique_id):
            _LOGGER.debug(
                "Not updating state for %s because a pending update is registered",
                self.unique_id,
            )
            return
        self._attr_is_on = self._rule.policy == "allow"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self._network_id in self.coordinator.data.get("l3_firewall_rules", {}):
            rules = self.coordinator.data["l3_firewall_rules"][self._network_id]
            # rules is a list of MerakiFirewallRule objects
            if isinstance(rules, list) and len(rules) > self._rule_index:
                self._rule = cast(MerakiFirewallRule, rules[self._rule_index])
                self._update_internal_state()
                self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """
        Turn the switch on.

        Args:
        ----
            **kwargs: Additional arguments.

        """
        self._attr_is_on = True
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)
        if self._network_id in self.coordinator.data.get("l3_firewall_rules", {}):
            rules_objects = self.coordinator.data["l3_firewall_rules"][self._network_id]
            if (
                isinstance(rules_objects, list)
                and len(rules_objects) > self._rule_index
            ):
                # We need to send dicts to the API
                # Convert all rule objects to dicts
                import dataclasses

                rules_dicts = [dataclasses.asdict(r) for r in rules_objects]

                # Update the specific rule
                rules_dicts[self._rule_index]["policy"] = "allow"

                await self.coordinator.api.appliance.update_l3_firewall_rules(
                    network_id=self._network_id,
                    rules=rules_dicts,
                )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """
        Turn the switch off.

        Args:
        ----
            **kwargs: Additional arguments.

        """
        self._attr_is_on = False
        self.async_write_ha_state()
        self.coordinator.register_pending_update(self.unique_id)
        if self._network_id in self.coordinator.data.get("l3_firewall_rules", {}):
            rules_objects = self.coordinator.data["l3_firewall_rules"][self._network_id]
            if (
                isinstance(rules_objects, list)
                and len(rules_objects) > self._rule_index
            ):
                # We need to send dicts to the API
                import dataclasses

                rules_dicts = [dataclasses.asdict(r) for r in rules_objects]

                rules_dicts[self._rule_index]["policy"] = "deny"

                await self.coordinator.api.appliance.update_l3_firewall_rules(
                    network_id=self._network_id,
                    rules=rules_dicts,
                )
