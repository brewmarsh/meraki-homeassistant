"""Helper function for setting up all sensor entities."""

import logging
from typing import TYPE_CHECKING, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from ..const import (
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_VLAN_MANAGEMENT,
)
from ..coordinator import MerakiDataUpdateCoordinator
from ..sensor_registry import (
    COMMON_SENSORS_COORD_DEV_CONF,
    get_sensors_for_device_type,
)
from ..types import MerakiVlan
from .client_tracker import ClientTrackerDeviceSensor, MerakiClientSensor
from .device.appliance_port import MerakiAppliancePortSensor
from .device.appliance_uplink import MerakiApplianceUplinkSensor
from .device.rtsp_url import MerakiRtspUrlSensor
from .network.vlan import (
    MerakiVLANIDSensor,
    MerakiVLANIPv4EnabledSensor,
    MerakiVLANIPv4InterfaceSensor,
    MerakiVLANIPv4UplinkSensor,
    MerakiVLANIPv6EnabledSensor,
    MerakiVLANIPv6InterfaceSensor,
    MerakiVLANIPv6UplinkSensor,
)
from .network.vlans_list import VlansListSensor
from .setup_mt_sensors import async_setup_mt_sensors
from .ssid.connected_clients import MerakiSsidConnectedClientsSensor

if TYPE_CHECKING:
    from ..services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


def _setup_device_sensors(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
    camera_service: "CameraService",
) -> list[Entity]:
    """Set up device-specific sensors."""
    entities: list[Entity] = []
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
                entities.append(sensor_class(coordinator, device_info))
                added_entities.add(unique_id)

        product_type = device_info.get("productType")
        if product_type and product_type.startswith("camera"):
            unique_id = f"{serial}_rtsp_url"
            if unique_id not in added_entities:
                entities.append(
                    MerakiRtspUrlSensor(coordinator, device_info, config_entry)
                )
                added_entities.add(unique_id)

        if product_type:
            # Sensors with (coordinator, device_info, config_entry)
            for sensor_class in get_sensors_for_device_type(product_type, True):
                unique_id = f"{serial}_{sensor_class.__name__}"
                if unique_id not in added_entities:
                    entities.append(
                        sensor_class(coordinator, device_info)
                    )
                    added_entities.add(unique_id)

            # Sensors with (coordinator, device_info)
            for sensor_class in get_sensors_for_device_type(product_type, False):
                unique_id = f"{serial}_{sensor_class.__name__}"
                if unique_id not in added_entities:
                    entities.append(sensor_class(coordinator, device_info))  # type: ignore[call-arg]
                    added_entities.add(unique_id)

        # Appliance port sensors
        if product_type == "appliance":
            for port in device_info.get("ports", []):
                unique_id = f"{serial}_port_{port['number']}"
                if unique_id not in added_entities:
                    entities.append(
                        MerakiAppliancePortSensor(coordinator, device_info, config_entry, port)
                    )
                    added_entities.add(unique_id)

        # MT sensor setup
        if product_type == "sensor":
            entities.extend(async_setup_mt_sensors(coordinator, device_info))

    return entities


def _setup_network_sensors(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
) -> list[Entity]:
    """Set up network-specific sensors."""
    entities: list[Entity] = []
    networks = coordinator.data.get("networks", [])
    for network_data in networks:
        network_id = network_data.get("id")
        if not network_id:
            continue

        # VLANs List Sensor
        if config_entry.options.get(
            CONF_ENABLE_VLAN_MANAGEMENT
        ) and coordinator.data.get("vlans", {}).get(network_id):
            unique_id = f"{network_id}_vlans_list"
            if unique_id not in added_entities:
                entities.append(
                    VlansListSensor(coordinator, config_entry, network_data)
                )
                added_entities.add(unique_id)
    return entities


def _setup_client_tracker_sensors(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
) -> list[Entity]:
    """Set up client tracker sensors."""
    if not config_entry.options.get(CONF_ENABLE_DEVICE_TRACKER, True):
        return []

    entities: list[Entity] = []
    clients = coordinator.data.get("clients", [])
    if clients:
        # Add the main device sensor for the tracker
        entities.append(ClientTrackerDeviceSensor(coordinator, config_entry))
        # Add a sensor for each client
        for client_data in clients:
            if "mac" in client_data:
                entities.append(
                    MerakiClientSensor(coordinator, config_entry, client_data)
                )
    return entities


def _setup_vlan_sensors(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
) -> list[Entity]:
    """Set up VLAN sensors."""
    entities: list[Entity] = []
    vlans_by_network = coordinator.data.get("vlans", {})

    vlan_sensors = [
        (MerakiVLANIDSensor, "vlan_id"),
        (MerakiVLANIPv4EnabledSensor, "ipv4_enabled"),
        (MerakiVLANIPv4InterfaceSensor, "ipv4_interface_ip"),
        (MerakiVLANIPv4UplinkSensor, "ipv4_uplink"),
        (MerakiVLANIPv6EnabledSensor, "ipv6_enabled"),
        (MerakiVLANIPv6InterfaceSensor, "ipv6_interface_ip"),
        (MerakiVLANIPv6UplinkSensor, "ipv6_uplink"),
    ]

    for network_id, vlans in vlans_by_network.items():
        if not isinstance(vlans, list):
            continue
        for vlan in vlans:
            if isinstance(vlan, dict):
                vlan_id = vlan.get("id")
                if not vlan_id:
                    continue

                for sensor_class, suffix in vlan_sensors:
                    unique_id = f"meraki_vlan_{network_id}_{vlan_id}_{suffix}"
                    if unique_id not in added_entities:
                        entities.append(
                            sensor_class(
                                coordinator,
                                config_entry,
                                network_id,
                                cast(MerakiVlan, vlan),
                            )
                        )
                        added_entities.add(unique_id)
    return entities


def _setup_uplink_sensors(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
) -> list[Entity]:
    """Set up appliance uplink sensors."""
    entities: list[Entity] = []
    appliance_uplinks = coordinator.data.get("appliance_uplink_statuses", [])
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
                        coordinator, cast(dict, device_info), config_entry, uplink
                    )
                )
                added_entities.add(unique_id)
    return entities


def _setup_ssid_sensors(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
) -> list[Entity]:
    """Set up SSID-specific sensors."""
    entities: list[Entity] = []
    ssids = coordinator.data.get("ssids", [])
    for ssid_data in ssids:
        network_id = ssid_data.get("networkId")
        ssid_number = ssid_data.get("number")
        if not network_id or ssid_number is None:
            continue

        unique_id = f"{network_id}_{ssid_number}_connected_clients"
        if unique_id not in added_entities:
            entities.append(
                MerakiSsidConnectedClientsSensor(
                    coordinator, network_id, ssid_data, config_entry
                )
            )
            added_entities.add(unique_id)
    return entities


def async_setup_sensors(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    camera_service: "CameraService",
) -> list[Entity]:
    """Set up all sensor entities from the central coordinator."""
    entities: list[Entity] = []
    added_entities: set[str] = set()

    if not coordinator.data:
        _LOGGER.warning("Coordinator has no data; skipping sensor setup.")
        return entities

    entities.extend(
        _setup_device_sensors(config_entry, coordinator, added_entities, camera_service)
    )
    entities.extend(_setup_network_sensors(config_entry, coordinator, added_entities))
    entities.extend(_setup_client_tracker_sensors(config_entry, coordinator))
    entities.extend(_setup_vlan_sensors(config_entry, coordinator, added_entities))
    entities.extend(_setup_uplink_sensors(config_entry, coordinator, added_entities))
    entities.extend(_setup_ssid_sensors(config_entry, coordinator, added_entities))

    return entities
