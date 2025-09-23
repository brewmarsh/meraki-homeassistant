"""Helper function for setting up all switch entities."""

import logging
from typing import List, Set, cast

from homeassistant.core import HomeAssistant
from ..types import MerakiVlan
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity

from ..coordinator import MerakiDataUpdateCoordinator
from .vlan_dhcp import MerakiVLANDHCPSwitch
from .firewall_rule import MerakiFirewallRuleSwitch
from ..types import MerakiFirewallRule
from .vpn import MerakiVPNSwitch
from .meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
)
from ..const import (
    CONF_ENABLE_VLAN_MANAGEMENT,
    CONF_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_VPN,
)
from ..sensor.network.network_identity import MerakiNetworkIdentitySensor


_LOGGER = logging.getLogger(__name__)


def _setup_vlan_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: Set[str],
) -> List[Entity]:
    """Set up VLAN switches."""
    if not config_entry.options.get(CONF_ENABLE_VLAN_MANAGEMENT):
        return []
    entities: List[Entity] = []
    vlans_by_network = coordinator.data.get("vlans", {})
    for network_id, vlans in vlans_by_network.items():
        if not isinstance(vlans, list):
            continue
        for vlan in vlans:
            if isinstance(vlan, dict):
                vlan_id = vlan.get("id")
                if not vlan_id:
                    continue

                unique_id = f"meraki_vlan_{network_id}_{vlan_id}_dhcp"
                if unique_id not in added_entities:
                    entities.append(
                        MerakiVLANDHCPSwitch(
                            coordinator,
                            config_entry,
                            network_id,
                            cast(MerakiVlan, vlan),
                        )
                    )
                    added_entities.add(unique_id)
    return entities


def _setup_firewall_rule_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: Set[str],
) -> List[Entity]:
    """Set up firewall rule switches."""
    if not config_entry.options.get(CONF_ENABLE_FIREWALL_RULES):
        return []
    entities: List[Entity] = []
    rules_by_network = coordinator.data.get("l3_firewall_rules", {})
    for network_id, rules_data in rules_by_network.items():
        if not isinstance(rules_data, dict):
            continue
        rules = rules_data.get("rules", [])
        if not isinstance(rules, list):
            continue
        for i, rule in enumerate(rules):
            if isinstance(rule, dict):
                unique_id = f"meraki_firewall_rule_{network_id}_{i}"
                if unique_id not in added_entities:
                    entities.append(
                        MerakiFirewallRuleSwitch(
                            coordinator,
                            config_entry,
                            network_id,
                            cast(MerakiFirewallRule, rule),
                            i,
                        )
                    )
                    added_entities.add(unique_id)
    return entities


def _setup_vpn_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: Set[str],
) -> List[Entity]:
    """Set up VPN switches."""
    if not config_entry.options.get(CONF_ENABLE_VPN):
        return []
    entities: List[Entity] = []
    networks = coordinator.data.get("networks", [])
    for network in networks:
        network_id = network.get("id")
        if not network_id:
            continue
        if "appliance" not in network.get("productTypes", []):
            continue

        vpn_status = coordinator.data.get("vpn_status", {}).get(network_id)
        if not vpn_status:
            continue

        unique_id = f"vpn_{network_id}"
        if unique_id not in added_entities:
            entities.append(
                MerakiVPNSwitch(
                    coordinator,
                    config_entry,
                    network,
                )
            )
            added_entities.add(unique_id)
    return entities


def _setup_ssid_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: Set[str],
) -> List[Entity]:
    """Set up SSID switches."""
    entities: List[Entity] = []
    ssids = coordinator.data.get("ssids", [])
    for ssid in ssids:
        ssid_number = ssid.get("number")
        if ssid_number is None:
            continue

        # Enabled Switch
        unique_id = f"ssid-{ssid['networkId']}-{ssid_number}-enabled-switch"
        if unique_id not in added_entities:
            entities.append(
                MerakiSSIDEnabledSwitch(
                    coordinator,
                    coordinator.api,
                    config_entry,
                    ssid,
                )
            )
            added_entities.add(unique_id)

        # Broadcast Switch
        unique_id = f"ssid-{ssid['networkId']}-{ssid_number}-broadcast-switch"
        if unique_id not in added_entities:
            entities.append(
                MerakiSSIDBroadcastSwitch(
                    coordinator,
                    coordinator.api,
                    config_entry,
                    ssid,
                )
            )
            added_entities.add(unique_id)
    return entities


def async_setup_switches(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
) -> List[Entity]:
    """Set up all switch entities from the central coordinator."""
    entities: List[Entity] = []
    added_entities: Set[str] = set()

    if not coordinator.data:
        _LOGGER.warning("Coordinator has no data; skipping switch setup.")
        return entities

    entities.extend(_setup_vlan_switches(config_entry, coordinator, added_entities))
    entities.extend(
        _setup_firewall_rule_switches(config_entry, coordinator, added_entities)
    )
    entities.extend(_setup_vpn_switches(config_entry, coordinator, added_entities))
    entities.extend(_setup_ssid_switches(config_entry, coordinator, added_entities))

    return entities
