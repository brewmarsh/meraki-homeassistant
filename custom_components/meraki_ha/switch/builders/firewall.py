"""Firewall rule switch builder."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.meraki_ha.const.integration import CONF_ENABLE_FIREWALL_RULES, from...coordinators import MerakiSwitchCoordinator
from ...core.models.network import MerakiFirewallRule
from ...core.utils.entity_id_utils import get_firewall_rule_entity_id
from ..firewall_rule import MerakiFirewallRuleSwitch

_LOGGER = logging.getLogger(__name__)


def setup_firewall_rule_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiSwitchCoordinator,
    added_entities: set[str],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up firewall rule switches."""
    if not config_entry.options.get(CONF_ENABLE_FIREWALL_RULES):
        return
    entities = _build_firewall_rule_entities(
        coordinator, coordinator.data, config_entry, added_entities
    )
    if entities:
        async_add_entities(entities)


def _build_firewall_rule_entities(
    coordinator: MerakiSwitchCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build firewall rule entities."""
    entities: list[SwitchEntity] = []
    rules_by_network = data.get("l3_firewall_rules", {})
    for network_id, rules in rules_by_network.items():
        if isinstance(rules, list):
            entities.extend(
                _create_firewall_rule_entities(
                    coordinator, config_entry, network_id, rules, added_entities
                )
            )
    return entities


def _create_firewall_rule_entities(
    coordinator: MerakiSwitchCoordinator,
    config_entry: ConfigEntry,
    network_id: str,
    rules: list[MerakiFirewallRule],
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Create firewall rule entities for a network."""
    entities: list[SwitchEntity] = []
    for index, rule in enumerate(rules):
        unique_id = get_firewall_rule_entity_id(network_id, index)
        if unique_id not in added_entities:
            entities.append(
                MerakiFirewallRuleSwitch(
                    coordinator,
                    config_entry,
                    network_id,
                    rule,
                    index,
                )
            )
            added_entities.add(unique_id)
    return entities
