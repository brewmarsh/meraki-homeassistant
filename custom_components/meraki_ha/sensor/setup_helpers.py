"""Helper function for setting up all sensor entities."""

import logging
import inspect
from typing import List, Set

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity

from ..core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ..sensor_registry import (
    COMMON_DEVICE_SENSORS,
    get_sensors_for_device_type,
)
from .network.network_clients import MerakiNetworkClientsSensor
from .network.network_identity import MerakiNetworkIdentitySensor
from .network.meraki_network_info import MerakiNetworkInfoSensor
from .device.appliance_port import MerakiAppliancePortSensor
from .device.switch_port import MerakiSwitchPortSensor
from .network.ssid import create_ssid_sensors
from .client_tracker import ClientTrackerDeviceSensor, MerakiClientSensor
from ..const import CONF_ENABLE_DEVICE_TRACKER

_LOGGER = logging.getLogger(__name__)


def async_setup_sensors(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiDataCoordinator,
) -> List[Entity]:
    """Set up all sensor entities from the central coordinator."""
    entities = []
    added_entities: Set[str] = set()

    if not coordinator.data:
        _LOGGER.warning("Coordinator has no data; skipping sensor setup.")
        return entities

    # Set up device-specific sensors
    devices = coordinator.data.get("devices", [])
    for device_info in devices:
        serial = device_info.get("serial")
        if not serial:
            _LOGGER.warning("Skipping device with missing serial.")
            continue

        device_info["name"] = device_info.get("name") or f"Meraki Device {serial}"

        # Common sensors for all devices
        for sensor_class in COMMON_DEVICE_SENSORS:
            unique_id = f"{serial}_{sensor_class.__name__}"
            if unique_id not in added_entities:
                # Check if the sensor class requires config_entry
                sig = inspect.signature(sensor_class.__init__)
                if "config_entry" in sig.parameters:
                    entities.append(
                        sensor_class(coordinator, device_info, config_entry)
                    )
                else:
                    entities.append(sensor_class(coordinator, device_info))
                added_entities.add(unique_id)

        # Product-type specific sensors
        product_type = device_info.get("productType")
        if product_type:
            for sensor_class in get_sensors_for_device_type(product_type):
                unique_id = f"{serial}_{sensor_class.__name__}"
                if unique_id not in added_entities:
                    sig = inspect.signature(sensor_class.__init__)
                    if "config_entry" in sig.parameters:
                        entities.append(
                            sensor_class(coordinator, device_info, config_entry)
                        )
                    else:
                        entities.append(sensor_class(coordinator, device_info))
                    added_entities.add(unique_id)

        # Appliance port sensors
        if product_type == "appliance":
            for port in device_info.get("ports", []):
                unique_id = f"{serial}_port_{port['number']}"
                if unique_id not in added_entities:
                    entities.append(MerakiAppliancePortSensor(coordinator, device_info, port))
                    added_entities.add(unique_id)

        # Switch port sensors
        if product_type == "switch":
            for port in device_info.get("ports_statuses", []):
                unique_id = f"{serial}_port_{port['portId']}"
                if unique_id not in added_entities:
                    entities.append(
                        MerakiSwitchPortSensor(coordinator, device_info, config_entry, port)
                    )
                    added_entities.add(unique_id)

    # Set up network-specific sensors
    networks = coordinator.data.get("networks", [])
    for network_data in networks:
        network_id = network_data.get("id")
        if not network_id:
            continue

        network_name = network_data.get("name", f"Unnamed Network {network_id}")

        # Network Clients Sensor
        unique_id = f"meraki_network_clients_{network_id}"
        if unique_id not in added_entities:
            entities.append(MerakiNetworkClientsSensor(coordinator, network_id, network_name))
            added_entities.add(unique_id)

        # Network Identity Sensor
        unique_id = f"meraki_network_identity_{network_id}"
        if unique_id not in added_entities:
            entities.append(MerakiNetworkIdentitySensor(coordinator, network_data, config_entry))
            added_entities.add(unique_id)

        # Network Info Sensor
        unique_id = f"{network_id}_network_info"
        if unique_id not in added_entities:
            entities.append(MerakiNetworkInfoSensor(coordinator, network_data, config_entry))
            added_entities.add(unique_id)

    # Set up SSID-specific sensors
    ssids = coordinator.data.get("ssids", [])
    for ssid_data in ssids:
        if "networkId" in ssid_data and "number" in ssid_data:
            entities.extend(create_ssid_sensors(coordinator, config_entry, ssid_data))

    # Set up Client Tracker sensors
    if config_entry.options.get(CONF_ENABLE_DEVICE_TRACKER, True):
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
