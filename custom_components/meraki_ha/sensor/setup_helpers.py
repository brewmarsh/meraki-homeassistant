"""Helper function for setting up all sensor entities."""

import logging
from typing import List, Set, cast

from homeassistant.core import HomeAssistant
from ..types import MerakiVlan
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity

from ..core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ..sensor_registry import (
    COMMON_SENSORS_COORD_DEV_CONF,
    get_sensors_for_device_type,
)
from .network.network_clients import MerakiNetworkClientsSensor
from .network.network_identity import MerakiNetworkIdentitySensor
from .network.meraki_network_info import MerakiNetworkInfoSensor
from .device.appliance_port import MerakiAppliancePortSensor
from .network.vlan import MerakiVLANSubnetSensor, MerakiVLANApplianceIpSensor
from .device.appliance_uplink import MerakiApplianceUplinkSensor
from .client_tracker import ClientTrackerDeviceSensor, MerakiClientSensor
from ..const import CONF_ENABLE_DEVICE_TRACKER

_LOGGER = logging.getLogger(__name__)


def _setup_device_sensors(
    config_entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
    added_entities: Set[str],
) -> List[Entity]:
    """Set up device-specific sensors."""
    entities: List[Entity] = []
    devices = coordinator.data.get("devices", [])
    for device_info in devices:
        serial = device_info.get("serial")
        if not serial:
            _LOGGER.warning("Skipping device with missing serial.")
            continue

        device_info["name"] = device_info.get("name") or f"Meraki Device {serial}"

        # Common sensors with (coordinator, device_info, config_entry)
        for sensor_class in COMMON_SENSORS_COORD_DEV_CONF:
            unique_id = f"{serial}_{sensor_class.__name__}"
            if unique_id not in added_entities:
                entities.append(sensor_class(coordinator, device_info, config_entry))
                added_entities.add(unique_id)

        product_type = device_info.get("productType")
        if product_type:
            # Sensors with (coordinator, device_info, config_entry)
            for sensor_class in get_sensors_for_device_type(product_type, True):
                unique_id = f"{serial}_{sensor_class.__name__}"
                if unique_id not in added_entities:
                    entities.append(
                        sensor_class(coordinator, device_info, config_entry)
                    )
                    added_entities.add(unique_id)

            # Sensors with (coordinator, device_info)
            for sensor_class in get_sensors_for_device_type(product_type, False):
                unique_id = f"{serial}_{sensor_class.__name__}"
                if unique_id not in added_entities:
                    entities.append(sensor_class(coordinator, device_info))
                    added_entities.add(unique_id)

        # Appliance port sensors
        if product_type == "appliance":
            for port in device_info.get("ports", []):
                unique_id = f"{serial}_port_{port['number']}"
                if unique_id not in added_entities:
                    entities.append(
                        MerakiAppliancePortSensor(coordinator, device_info, port)
                    )
                    added_entities.add(unique_id)
    return entities


def _setup_network_sensors(
    config_entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
    added_entities: Set[str],
) -> List[Entity]:
    """Set up network-specific sensors."""
    entities: List[Entity] = []
    networks = coordinator.data.get("networks", [])
    for network_data in networks:
        network_id = network_data.get("id")
        if not network_id:
            continue

        # Network Identity Sensor
        unique_id = f"meraki_network_identity_{network_id}"
        if unique_id not in added_entities:
            entities.append(
                MerakiNetworkIdentitySensor(coordinator, network_data, config_entry)
            )
            added_entities.add(unique_id)

        # Network Info Sensor
        unique_id = f"{network_id}_network_info"
        if unique_id not in added_entities:
            entities.append(
                MerakiNetworkInfoSensor(coordinator, network_data, config_entry)
            )
            added_entities.add(unique_id)
    return entities


def _setup_client_tracker_sensors(
    config_entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
) -> List[Entity]:
    """Set up client tracker sensors."""
    if not config_entry.options.get(CONF_ENABLE_DEVICE_TRACKER, True):
        return []

    entities: List[Entity] = []
    clients = coordinator.data.get("clients", [])
    if clients:
        # Add the main device sensor for the tracker
        entities.append(ClientTrackerDeviceSensor(coordinator))
        # Add a sensor for each client
        for client_data in clients:
            if "mac" in client_data:
                entities.append(
                    MerakiClientSensor(coordinator, config_entry, client_data)
                )
    return entities


def _setup_vlan_sensors(
    config_entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
    added_entities: Set[str],
) -> List[Entity]:
    """Set up VLAN sensors."""
    entities: List[Entity] = []
    vlans_by_network = coordinator.data.get("vlans", {})
    for network_id, vlans in vlans_by_network.items():
        if not isinstance(vlans, list):
            continue
        for vlan in vlans:
            if isinstance(vlan, dict) and vlan.get("enabled", False):
                vlan_id = vlan.get("id")
                if not vlan_id:
                    continue

                unique_id_subnet = f"meraki_vlan_{network_id}_{vlan_id}_subnet"
                if unique_id_subnet not in added_entities:
                    entities.append(
                        MerakiVLANSubnetSensor(
                            coordinator,
                            config_entry,
                            network_id,
                            cast(MerakiVlan, vlan),
                        )
                    )
                    added_entities.add(unique_id_subnet)

                unique_id_ip = f"meraki_vlan_{network_id}_{vlan_id}_appliance_ip"
                if unique_id_ip not in added_entities:
                    entities.append(
                        MerakiVLANApplianceIpSensor(
                            coordinator,
                            config_entry,
                            network_id,
                            cast(MerakiVlan, vlan),
                        )
                    )
                    added_entities.add(unique_id_ip)
    return entities


def _setup_uplink_sensors(
    config_entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
    added_entities: Set[str],
) -> List[Entity]:
    """Set up appliance uplink sensors."""
    entities: List[Entity] = []
    appliance_uplinks = coordinator.data.get("appliance_uplink_statuses", [])
    devices = coordinator.data.get("devices", [])
    for uplink_status in appliance_uplinks:
        serial = uplink_status.get("serial")
        if not serial:
            continue

        device_info = coordinator.get_device(serial)
        if not device_info:
            continue

        for uplink in uplink_status.get("uplinks", []):
            interface = uplink.get("interface")
            if not interface:
                continue

            unique_id = f"{serial}_uplink_{interface}"
            if unique_id not in added_entities:
                entities.append(
                    MerakiApplianceUplinkSensor(
                        coordinator, device_info, config_entry, uplink
                    )
                )
                added_entities.add(unique_id)
    return entities


def async_setup_sensors(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
) -> List[Entity]:
    """Set up all sensor entities from the central coordinator."""
    entities: List[Entity] = []
    added_entities: Set[str] = set()

    if not coordinator.data:
        _LOGGER.warning("Coordinator has no data; skipping sensor setup.")
        return entities

    entities.extend(_setup_device_sensors(config_entry, coordinator, added_entities))
    entities.extend(_setup_network_sensors(config_entry, coordinator, added_entities))
    entities.extend(_setup_client_tracker_sensors(config_entry, coordinator))
    entities.extend(_setup_vlan_sensors(config_entry, coordinator, added_entities))
    entities.extend(_setup_uplink_sensors(config_entry, coordinator, added_entities))

    return entities
