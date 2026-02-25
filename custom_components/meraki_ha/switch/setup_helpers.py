"""Helper function for setting up all switch entities."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const_conf import (
    CONF_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_TRAFFIC_SHAPING,
    CONF_ENABLE_VLAN_MANAGEMENT,
    CONF_ENABLE_VPN_MANAGEMENT,
)
from ..coordinator import MerakiDataUpdateCoordinator
from ..core.api.client import MerakiAPIClient
from ..core.models.network import MerakiTrafficShaping, MerakiVpn
from ..core.utils.entity_id_utils import get_firewall_rule_entity_id
from .camera_controls import AnalyticsSwitch
from .firewall_rule import MerakiFirewallRuleSwitch
from .meraki_ssid_device_switch import (
    MerakiSSIDBroadcastSwitch,
    MerakiSSIDEnabledSwitch,
)
from .mt40_power_outlet import MerakiMt40PowerOutlet
from .traffic_shaping import MerakiTrafficShapingSwitch
from .vlan_dhcp import MerakiVLANDHCPSwitch
from .vpn import MerakiVPNSwitch

_LOGGER = logging.getLogger(__name__)


def _setup_firewall_rule_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
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
    coordinator: MerakiDataUpdateCoordinator,
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
    coordinator: MerakiDataUpdateCoordinator,
    config_entry: ConfigEntry,
    network_id: str,
    rules: list[dict[str, Any]],
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


def _setup_traffic_shaping_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up traffic shaping switches."""
    if not config_entry.options.get(CONF_ENABLE_TRAFFIC_SHAPING):
        return
    entities = _build_traffic_shaping_entities(
        coordinator, coordinator.data, config_entry, added_entities
    )
    if entities:
        async_add_entities(entities)


def _build_traffic_shaping_entities(
    coordinator: MerakiDataUpdateCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build traffic shaping entities."""
    entities: list[SwitchEntity] = []
    traffic_shaping_by_network = data.get("traffic_shaping", {})
    for network_id, traffic_shaping in traffic_shaping_by_network.items():
        entity = _create_traffic_shaping_entity(
            coordinator, config_entry, network_id, traffic_shaping, added_entities
        )
        if entity:
            entities.append(entity)
    return entities


def _create_traffic_shaping_entity(
    coordinator: MerakiDataUpdateCoordinator,
    config_entry: ConfigEntry,
    network_id: str,
    traffic_shaping: Any,
    added_entities: set[str],
) -> SwitchEntity | None:
    """Create a single traffic shaping switch entity if not already added."""
    if not isinstance(traffic_shaping, MerakiTrafficShaping):
        return None

    unique_id = f"{network_id}_traffic_shaping_switch"
    if unique_id in added_entities:
        return None

    added_entities.add(unique_id)
    return MerakiTrafficShapingSwitch(
        coordinator,
        config_entry,
        network_id,
        traffic_shaping,
    )


def _setup_vpn_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up VPN switches."""
    if not config_entry.options.get(CONF_ENABLE_VPN_MANAGEMENT):
        return
    entities = _build_vpn_entities(
        coordinator, coordinator.data, config_entry, added_entities
    )
    if entities:
        async_add_entities(entities)


def _build_vpn_entities(
    coordinator: MerakiDataUpdateCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build VPN entities."""
    entities: list[SwitchEntity] = []
    vpn_status_by_network = data.get("vpn_status", {})
    for network_id, vpn_status in vpn_status_by_network.items():
        if isinstance(vpn_status, MerakiVpn):
            entity = _create_vpn_entity(
                coordinator, config_entry, network_id, added_entities
            )
            if entity:
                entities.append(entity)
    return entities


def _create_vpn_entity(
    coordinator: MerakiDataUpdateCoordinator,
    config_entry: ConfigEntry,
    network_id: str,
    added_entities: set[str],
) -> SwitchEntity | None:
    """Create a single VPN switch entity if not already added."""
    unique_id = f"vpn_{network_id}"
    if unique_id in added_entities:
        return None

    # We need to fetch the network object for the entity
    network = coordinator.get_network(network_id)
    if not network:
        return None

    added_entities.add(unique_id)
    return MerakiVPNSwitch(
        coordinator,
        config_entry,
        network,
    )


def _setup_vlan_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up VLAN switches."""
    if not config_entry.options.get(CONF_ENABLE_VLAN_MANAGEMENT):
        return
    entities = _build_vlan_entities(
        coordinator, coordinator.data, config_entry, added_entities
    )
    if entities:
        async_add_entities(entities)


def _build_vlan_entities(
    coordinator: MerakiDataUpdateCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build VLAN entities."""
    entities: list[SwitchEntity] = []
    vlans_by_network = data.get("vlans", {})
    for network_id, vlans in vlans_by_network.items():
        if isinstance(vlans, list):
            entities.extend(
                _create_vlan_entities(
                    coordinator, config_entry, network_id, vlans, added_entities
                )
            )
    return entities


def _create_vlan_entities(
    coordinator: MerakiDataUpdateCoordinator,
    config_entry: ConfigEntry,
    network_id: str,
    vlans: list[Any],
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Create VLAN entities for a network."""
    entities: list[SwitchEntity] = []
    for vlan in vlans:
        vlan_id = getattr(vlan, "id", None)
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
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SSID switches."""
    entities = _build_ssid_entities(
        coordinator, coordinator.data, config_entry, added_entities
    )
    if entities:
        async_add_entities(entities)


def _build_ssid_entities(
    coordinator: MerakiDataUpdateCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build SSID entities."""
    entities: list[SwitchEntity] = []
    ssids = data.get("ssids", [])
    for ssid in ssids:
        entities.extend(
            _build_ssid_pair(coordinator, data, config_entry, ssid, added_entities)
        )
    return entities


def _build_ssid_pair(
    coordinator: MerakiDataUpdateCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    ssid: dict[str, Any],
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build a pair of switches (enabled and broadcast) for an SSID."""
    ssid_number = ssid.get("number")
    if ssid_number is None:
        return []

    entities: list[SwitchEntity] = []
    rf_profile = _get_rf_profile(data, ssid.get("networkId"))

    # Enabled Switch
    unique_id = f"{ssid['networkId']}ssid{ssid_number}_enabled_switch"
    if unique_id not in added_entities:
        entities.append(
            MerakiSSIDEnabledSwitch(
                coordinator,
                coordinator.api,
                config_entry,
                ssid,
                rf_profile,
            )
        )
        added_entities.add(unique_id)

    # Broadcast Switch
    unique_id = f"{ssid['networkId']}ssid{ssid_number}_broadcast_switch"
    if unique_id not in added_entities:
        entities.append(
            MerakiSSIDBroadcastSwitch(
                coordinator,
                coordinator.api,
                config_entry,
                ssid,
                rf_profile,
            )
        )
        added_entities.add(unique_id)
    return entities


def _get_rf_profile(
    data: dict[str, Any],
    network_id: str | None,
) -> dict[str, Any] | None:
    """Find the RF profile for a network."""
    if not network_id or not data.get("rf_profiles"):
        return None
    network_rf_profiles = data["rf_profiles"].get(network_id)
    if network_rf_profiles:
        return next(iter(network_rf_profiles), None)
    return None


def _setup_camera_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up camera-specific switches."""
    entities = _build_camera_entities(coordinator, coordinator.data, added_entities)
    if entities:
        async_add_entities(entities)


def _build_camera_entities(
    coordinator: MerakiDataUpdateCoordinator,
    data: dict[str, Any],
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build camera-specific entities."""
    entities: list[SwitchEntity] = []
    devices = data.get("devices", [])
    for device_info in devices:
        entity = _create_camera_analytics_switch(
            coordinator, device_info, added_entities
        )
        if entity:
            entities.append(entity)
    return entities


def _create_camera_analytics_switch(
    coordinator: MerakiDataUpdateCoordinator,
    device_info: Any,
    added_entities: set[str],
) -> SwitchEntity | None:
    """Create a camera analytics switch if applicable and not already added."""
    if not (device_info.product_type or "").startswith("camera"):
        return None

    serial = device_info.serial
    unique_id = f"{serial}_analytics_switch"
    if unique_id in added_entities:
        return None

    added_entities.add(unique_id)
    return AnalyticsSwitch(coordinator, coordinator.api, device_info)


def _setup_mt40_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
    meraki_client: "MerakiAPIClient",
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MT40 power outlet switches."""
    entities = _build_mt40_entities(
        coordinator, coordinator.data, config_entry, added_entities, meraki_client
    )
    if entities:
        async_add_entities(entities)


def _build_mt40_entities(
    coordinator: MerakiDataUpdateCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    added_entities: set[str],
    meraki_client: "MerakiAPIClient",
) -> list[SwitchEntity]:
    """Build MT40 power outlet entities."""
    entities: list[SwitchEntity] = []
    devices = data.get("devices", [])
    for device_info in devices:
        entity = _create_mt40_outlet_switch(
            coordinator, device_info, config_entry, added_entities, meraki_client
        )
        if entity:
            entities.append(entity)
    return entities


def _create_mt40_outlet_switch(
    coordinator: MerakiDataUpdateCoordinator,
    device_info: Any,
    config_entry: ConfigEntry,
    added_entities: set[str],
    meraki_client: "MerakiAPIClient",
) -> SwitchEntity | None:
    """Create an MT40 power outlet switch if applicable and not already added."""
    if not (device_info.model or "").startswith("MT40"):
        return None

    serial = device_info.serial
    unique_id = f"{serial}_outlet_switch"
    if unique_id in added_entities:
        return None

    added_entities.add(unique_id)
    return MerakiMt40PowerOutlet(
        coordinator, device_info, config_entry, meraki_client
    )


def async_setup_switches(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    meraki_client: "MerakiAPIClient",
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all switch entities from the central coordinator."""
    added_entities: set[str] = set()

    if not coordinator.data:
        _LOGGER.warning("Coordinator has no data; skipping switch setup.")
        return

    _setup_vlan_switches(config_entry, coordinator, added_entities, async_add_entities)
    _setup_firewall_rule_switches(
        config_entry, coordinator, added_entities, async_add_entities
    )
    _setup_traffic_shaping_switches(
        config_entry, coordinator, added_entities, async_add_entities
    )
    _setup_vpn_switches(config_entry, coordinator, added_entities, async_add_entities)
    _setup_ssid_switches(config_entry, coordinator, added_entities, async_add_entities)
    _setup_camera_switches(
        config_entry, coordinator, added_entities, async_add_entities
    )
    _setup_mt40_switches(
        config_entry,
        coordinator,
        added_entities,
        meraki_client,
        async_add_entities,
    )
