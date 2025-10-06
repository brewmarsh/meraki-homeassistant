"""Helper function for setting up all switch entities."""

import logging
from typing import List, Set, cast

from homeassistant.core import HomeAssistant
from ..types import MerakiVlan
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity

from ..coordinator import MerakiDataUpdateCoordinator
from .vlan_dhcp import MerakiVLANDHCPSwitch
from .camera_controls import AnalyticsSwitch
from .meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
)
from ..const import (
    CONF_ENABLE_VLAN_MANAGEMENT,
)
from .mt40_power_outlet import MerakiMt40PowerOutlet


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


def _setup_camera_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: Set[str],
) -> List[Entity]:
    """Set up camera-specific switches."""
    entities: List[Entity] = []
    devices = coordinator.data.get("devices", [])
    for device_info in devices:
        if device_info.get("productType", "").startswith("camera"):
            serial = device_info["serial"]
            # Analytics Switch
            unique_id = f"{serial}_analytics_switch"
            if unique_id not in added_entities:
                entities.append(
                    AnalyticsSwitch(
                        coordinator, coordinator.api, device_info
                    )
                )
                added_entities.add(unique_id)
    return entities


def _setup_mt40_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: Set[str],
    meraki_client: "MerakiAPIClient",
) -> List[Entity]:
    """Set up MT40 power outlet switches."""
    entities: List[Entity] = []
    devices = coordinator.data.get("devices", [])
    for device_info in devices:
        if device_info.get("model", "").startswith("MT40"):
            serial = device_info["serial"]
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
) -> List[Entity]:
    """Set up all switch entities from the central coordinator."""
    entities: List[Entity] = []
    added_entities: Set[str] = set()

    if not coordinator.data:
        _LOGGER.warning("Coordinator has no data; skipping switch setup.")
        return entities

    entities.extend(_setup_vlan_switches(config_entry, coordinator, added_entities))
    entities.extend(_setup_ssid_switches(config_entry, coordinator, added_entities))
    entities.extend(_setup_camera_switches(config_entry, coordinator, added_entities))
    entities.extend(
        _setup_mt40_switches(config_entry, coordinator, added_entities, meraki_client)
    )

    return entities
