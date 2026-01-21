"""Helper function for setting up all switch entities."""

import logging
from typing import cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from ..const import (
    CONF_ENABLE_VLAN_MANAGEMENT,
)
<<<<<<< HEAD
from ..core.api.client import MerakiAPIClient
from ..meraki_data_coordinator import MerakiDataCoordinator
from ..types import MerakiVlan
from .access_point_leds import MerakiAPLEDSwitch
=======
from ..coordinator import MerakiDataUpdateCoordinator
from ..core.api.client import MerakiAPIClient
from ..types import MerakiVlan
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from .camera_controls import AnalyticsSwitch
from .meraki_ssid_device_switch import (
    MerakiSSIDBroadcastSwitch,
    MerakiSSIDEnabledSwitch,
)
from .mt40_power_outlet import MerakiMt40PowerOutlet
from .vlan_dhcp import MerakiVLANDHCPSwitch

_LOGGER = logging.getLogger(__name__)


def _setup_vlan_switches(
    config_entry: ConfigEntry,
<<<<<<< HEAD
    coordinator: MerakiDataCoordinator,
=======
    coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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
<<<<<<< HEAD
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
=======
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
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    return entities


def _setup_ssid_switches(
    config_entry: ConfigEntry,
<<<<<<< HEAD
    coordinator: MerakiDataCoordinator,
=======
    coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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
<<<<<<< HEAD
    coordinator: MerakiDataCoordinator,
=======
    coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    added_entities: set[str],
) -> list[Entity]:
    """Set up camera-specific switches."""
    entities: list[Entity] = []
    devices = coordinator.data.get("devices", [])
    for device_info in devices:
<<<<<<< HEAD
        if device_info.get("productType", "").startswith("camera"):
            serial = device_info["serial"]
=======
        if (device_info.product_type or "").startswith("camera"):
            serial = device_info.serial
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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
<<<<<<< HEAD
    coordinator: MerakiDataCoordinator,
=======
    coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    added_entities: set[str],
    meraki_client: "MerakiAPIClient",
) -> list[Entity]:
    """Set up MT40 power outlet switches."""
    entities: list[Entity] = []
    devices = coordinator.data.get("devices", [])
    for device_info in devices:
<<<<<<< HEAD
        if device_info.get("model", "").startswith("MT40"):
            serial = device_info["serial"]
=======
        if (device_info.model or "").startswith("MT40"):
            serial = device_info.serial
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            unique_id = f"{serial}_outlet_switch"
            if unique_id not in added_entities:
                entities.append(
                    MerakiMt40PowerOutlet(
                        coordinator, device_info, config_entry, meraki_client
                    )
                )
                added_entities.add(unique_id)
    return entities


<<<<<<< HEAD
def _setup_ap_led_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
    added_entities: set[str],
) -> list[Entity]:
    """Set up AP LED switches."""
    entities: list[Entity] = []
    networks = coordinator.data.get("networks", [])
    for network in networks:
        if "wireless" in network.get("productTypes", []):
            unique_id = f"meraki_{network['id']}_ap_leds"
            if unique_id not in added_entities:
                entities.append(
                    MerakiAPLEDSwitch(
                        coordinator,
                        config_entry,
                        network,
                    )
                )
                added_entities.add(unique_id)
    return entities


def async_setup_switches(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
=======
def async_setup_switches(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    meraki_client: "MerakiAPIClient",
) -> list[Entity]:
    """Set up all switch entities from the central coordinator."""
    entities: list[Entity] = []
    added_entities: set[str] = set()

    if not coordinator.data:
        _LOGGER.warning("Coordinator has no data; skipping switch setup.")
        return entities

    entities.extend(_setup_vlan_switches(config_entry, coordinator, added_entities))
    entities.extend(_setup_ssid_switches(config_entry, coordinator, added_entities))
    entities.extend(_setup_camera_switches(config_entry, coordinator, added_entities))
    entities.extend(
        _setup_mt40_switches(config_entry, coordinator, added_entities, meraki_client)
    )
<<<<<<< HEAD
    entities.extend(_setup_ap_led_switches(config_entry, coordinator, added_entities))
=======
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    return entities
