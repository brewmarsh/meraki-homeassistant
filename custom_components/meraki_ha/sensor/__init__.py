"""Sensor platform for the Meraki Home Assistant integration.

This platform sets up various sensor entities for Meraki devices and SSIDs,
including device status, client counts, network information, and SSID-specific
details like availability and channel usage. It uses data coordinators to
fetch and manage data from the Meraki API.
"""

import logging
from typing import Optional  # Added Optional
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import (
    DOMAIN,
    DATA_COORDINATOR,
    DATA_SSID_DEVICES_COORDINATOR,
    DATA_CLIENT,
)
from ..core.coordinators.device import MerakiDeviceCoordinator
from ..core.coordinators.network import MerakiNetworkCoordinator
from ..core.api.client import MerakiAPIClient
from ..sensor_registry import (
    COMMON_DEVICE_SENSORS,
    get_sensors_for_device_type,
)
from .network.ssid import create_ssid_sensors
from .org.org_device_type_clients import MerakiOrgDeviceTypeClientsSensor
from .org.org_clients import (
    MerakiOrganizationSSIDClientsSensor,
    MerakiOrganizationWirelessClientsSensor,
    MerakiOrganizationApplianceClientsSensor,
)
from .network.network_clients import MerakiNetworkClientsSensor
from .network.network_identity import MerakiNetworkIdentitySensor
from .network.meraki_network_info import MerakiNetworkInfoSensor
from .device.appliance_port import MerakiAppliancePortSensor
from .device.firmware_status import MerakiFirmwareStatusSensor
from .device.camera_rtsp_url import MerakiCameraRTSPUrlSensor
from ..core.utils.naming_utils import format_device_name


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki sensor entities from a config entry."""
    entities = []
    added_entities = set()

    # Get the entry specific data store
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Get the main data coordinator for physical devices
    device_coordinator: MerakiDeviceCoordinator = entry_data.get("device_coordinator")
    network_coordinator: MerakiNetworkCoordinator = entry_data.get(
        "network_coordinator"
    )

    # Retrieve the MerakiAPIClient instance
    meraki_api_client: Optional[MerakiAPIClient] = entry_data.get(DATA_CLIENT)

    if not meraki_api_client:
        _LOGGER.error(
            "Meraki API client not found in entry_data. Cannot set up network client sensors."
        )

    # --- Physical Device Sensor Setup ---
    if device_coordinator and device_coordinator.data:
        physical_devices = device_coordinator.data.get("devices", [])
        for device_info in physical_devices:
            serial = device_info.get("serial")
            if not serial:
                _LOGGER.warning(
                    f"Skipping device with missing serial: {device_info.get('name', 'Unnamed Device with no Serial')}"
                )
                continue

            original_device_name = device_info.get("name")
            if not original_device_name:
                model_str = device_info.get("model", "Device")
                fallback_name = f"Meraki {model_str} {serial}"
                device_info["name"] = fallback_name

            device_info["name"] = format_device_name(
                device_info, config_entry.options
            )
            for sensor_class in COMMON_DEVICE_SENSORS:
                unique_id = f"{serial}_{sensor_class.__name__}"
                if unique_id not in added_entities:
                    try:
                        entities.append(
                            sensor_class(device_coordinator, device_info, config_entry)
                        )
                        added_entities.add(unique_id)
                    except Exception as e:
                        _LOGGER.error(
                            "Meraki HA: Error adding common sensor %s for %s: %s",
                            sensor_class.__name__,
                            device_info.get("name", serial),
                            e,
                        )

            # Add productType-specific sensors
            product_type = device_info.get("productType")

            if product_type:
                sensors_for_type = get_sensors_for_device_type(product_type)
                # if not sensors_for_type: # Removed: Redundant log, handled by empty list iteration
                #   pass
                for sensor_class in sensors_for_type:
                    unique_id = f"{serial}_{sensor_class.__name__}"
                    if unique_id not in added_entities:
                        try:
                            entities.append(
                                sensor_class(device_coordinator, device_info)
                            )
                            added_entities.add(unique_id)
                        except Exception as e:
                            _LOGGER.error(
                                "Meraki HA: Error adding sensor %s for %s (productType: %s): %s",
                                sensor_class.__name__,
                                device_info.get("name", serial),
                                product_type,
                                e,
                            )

                # Camera-specific sensors are now handled by the SENSOR_REGISTRY.
                # The generic loop for `sensors_for_type` will add them if product_type is "camera".
            else:
                _LOGGER.warning(  # Changed to warning as this might be unexpected
                    "Meraki HA: No productType found for device %s (Serial: %s), skipping productType-specific sensors.",
                    device_info.get("name"),  # Use guaranteed name
                    serial,
                )

    else:
        _LOGGER.warning(
            "Main coordinator not available or has no data; skipping physical device sensors."
        )

    # --- Network-specific Sensor Setup ---
    if network_coordinator and network_coordinator.data and meraki_api_client:
        networks = network_coordinator.data.get("networks", [])
        for network_data in networks:
            network_id = network_data.get("id")
            network_name = network_data.get("name", f"Unnamed Network {network_id}")
            if not network_name:
                network_name = f"Meraki Network {network_id}"

            if not network_id:
                _LOGGER.warning(
                    "Skipping network with missing ID for client sensor: %s",
                    network_data.get("name", "Unnamed Network"),
                )
                continue
            unique_id = f"meraki_network_clients_{network_id}"
            if unique_id not in added_entities:
                try:
                    entities.append(
                        MerakiNetworkClientsSensor(
                            network_coordinator, network_id, network_name
                        )
                    )
                    added_entities.add(unique_id)
                except Exception as e:
                    _LOGGER.error(
                        "Meraki HA: Error adding network clients sensor for %s (ID: %s): %s",
                        network_name,
                        network_id,
                        e,
                    )
            unique_id = f"meraki_network_identity_{network_id}"
            if unique_id not in added_entities:
                try:
                    entities.append(
                        MerakiNetworkIdentitySensor(
                            network_coordinator, network_data, config_entry
                        )
                    )
                    added_entities.add(unique_id)
                except Exception as e:
                    _LOGGER.error(
                        "Meraki HA: Error adding network identity sensor for %s (ID: %s): %s",
                        network_name,
                        network_id,
                        e,
                    )
            unique_id = f"{network_id}_network_info"
            if unique_id not in added_entities:
                try:
                    entities.append(
                        MerakiNetworkInfoSensor(
                            network_coordinator, network_data, config_entry
                        )
                    )
                    added_entities.add(unique_id)
                except Exception as e:
                    _LOGGER.error(
                        "Meraki HA: Error adding network info sensor for %s (ID: %s): %s",
                        network_name,
                        network_id,
                        e,
                    )

    elif not meraki_api_client:
        _LOGGER.warning(
            "Meraki API client not available; skipping MerakiNetworkClientsSensor setup."
        )
    elif not network_coordinator or not network_coordinator.data:
        _LOGGER.warning(
            "Main coordinator not available or has no data; skipping all network-specific sensors."
        )

    if device_coordinator and device_coordinator.data:
        for device in device_coordinator.data.get("devices", []):
            if device.get("productType") == "appliance":
                for port in device.get("ports", []):
                    if f"{device['serial']}_port_{port['number']}" not in added_entities:
                        entities.append(MerakiAppliancePortSensor(device_coordinator, device, port))
                        added_entities.add(f"{device['serial']}_port_{port['number']}")
            if device.get("productType") == "camera":
                if f"{device['serial']}_rtsp_url" not in added_entities:
                    entities.append(MerakiCameraRTSPUrlSensor(device_coordinator, device))
                    added_entities.add(f"{device['serial']}_rtsp_url")
            if f"{device['serial']}_firmware_status" not in added_entities:
                entities.append(MerakiFirmwareStatusSensor(device_coordinator, device))
                added_entities.add(f"{device['serial']}_firmware_status")

    if entities:
        async_add_entities(entities)
    return True
