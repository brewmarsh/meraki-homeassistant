"""Helper function for setting up all switch entities."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from ..const import (
    CONF_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_TRAFFIC_SHAPING,
    CONF_ENABLE_VLAN_MANAGEMENT,
)
from ..coordinator import MerakiDataUpdateCoordinator
from ..core.api.client import MerakiAPIClient
from ..core.utils.entity_id_utils import get_firewall_rule_entity_id
from ..types import MerakiTrafficShaping, MerakiVlan
from .camera_controls import AnalyticsSwitch
from .firewall_rule import MerakiFirewallRuleSwitch
from .meraki_ssid_device_switch import (
    MerakiSSIDBroadcastSwitch,
    MerakiSSIDEnabledSwitch,
)
from .mt40_power_outlet import MerakiMt40PowerOutlet
from .traffic_shaping import MerakiTrafficShapingSwitch
from .vlan_dhcp import MerakiVLANDHCPSwitch

_LOGGER = logging.getLogger(__name__)


def _setup_firewall_rule_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
) -> list[Entity]:
    """Set up firewall rule switches."""
    if not config_entry.options.get(CONF_ENABLE_FIREWALL_RULES):
        return []

    entities: list[Entity] = []
    # Structure is {network_id: [rule1, rule2, ...]}
    rules_by_network = coordinator.data.get("l3_firewall_rules", {})
    for network_id, rules in rules_by_network.items():
        if not isinstance(rules, list):
            continue

        for index, rule in enumerate(rules):
            # We use index because rules might not have unique IDs
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


def _setup_traffic_shaping_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
) -> list[Entity]:
    """Set up traffic shaping switches."""
    if not config_entry.options.get(CONF_ENABLE_TRAFFIC_SHAPING):
        return []

    entities: list[Entity] = []
    traffic_shaping_by_network = coordinator.data.get("traffic_shaping", {})
    for network_id, traffic_shaping in traffic_shaping_by_network.items():
        if not isinstance(traffic_shaping, MerakiTrafficShaping):
            continue

        unique_id = f"{network_id}_traffic_shaping_switch"
        if unique_id not in added_entities:
            entities.append(
                MerakiTrafficShapingSwitch(
                    coordinator,
                    config_entry,
                    network_id,
                    traffic_shaping,
                )
            )
            added_entities.add(unique_id)
    return entities


def _setup_vlan_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
) -> list[Entity]:
    """Set up VLAN switches."""
    if not config_entry.options.get(CONF_ENABLE_VLAN_MANAGEMENT):
        return []
    entities: list[Entity] = []
    vlans_by_network = coordinator.data.get("vlans", {})
    for network_id, vlans in vlans_by_network.items():
        if not isinstance(vlans, list):
            continue
        for vlan in vlans:
            if not isinstance(vlan, MerakiVlan):
                continue

            vlan_id = vlan.id
            if not vlan_id:
                continue

            unique_id = f"meraki_vlan_{network_id}_{vlan_id}_dhcp"
            if unique_id not in added_entities:
                entities.append(
                    MerakiVLANDHCPSwitch(
                        coordinator,
                        config_entry,
                        network_id,
                        vlan,
                    )
                )
                added_entities.add(unique_id)
    return entities


def _setup_ssid_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
) -> list[Entity]:
    """Set up SSID switches."""
    entities: list[Entity] = []
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


def _setup_camera_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
) -> list[Entity]:
    """Set up camera-specific switches."""
    entities: list[Entity] = []
    devices = coordinator.data.get("devices", [])
    for device_info in devices:
        if (device_info.product_type or "").startswith("camera"):
            serial = device_info.serial
            # Analytics Switch
            unique_id = f"{serial}_analytics_switch"
            if unique_id not in added_entities:
                entities.append(
                    AnalyticsSwitch(coordinator, coordinator.api, device_info)
                )
                added_entities.add(unique_id)
    return entities


def _setup_mt40_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
    meraki_client: "MerakiAPIClient",
) -> list[Entity]:
    """Set up MT40 power outlet switches."""
    entities: list[Entity] = []
    devices = coordinator.data.get("devices", [])
    for device_info in devices:
        if (device_info.model or "").startswith("MT40"):
            serial = device_info.serial
            unique_id = f"{serial}_outlet_switch"
            if unique_id not in added_entities:
                entities.append(
                    MerakiMt40PowerOutlet(
                        coordinator, device_info, config_entry, meraki_client
                    )
                )
                added_entities.add(unique_id)
    return entities


def async_setup_switches(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    meraki_client: "MerakiAPIClient",
) -> list[Entity]:
    """Set up all switch entities from the central coordinator."""
    entities: list[Entity] = []
    added_entities: set[str] = set()

    if not coordinator.data:
        _LOGGER.warning("Coordinator has no data; skipping switch setup.")
        return entities

    entities.extend(_setup_vlan_switches(config_entry, coordinator, added_entities))
    entities.extend(
        _setup_firewall_rule_switches(config_entry, coordinator, added_entities)
    )
    entities.extend(
        _setup_traffic_shaping_switches(config_entry, coordinator, added_entities)
    )
    entities.extend(_setup_ssid_switches(config_entry, coordinator, added_entities))
    entities.extend(_setup_camera_switches(config_entry, coordinator, added_entities))
    entities.extend(
        _setup_mt40_switches(config_entry, coordinator, added_entities, meraki_client)
    )

    return entities
