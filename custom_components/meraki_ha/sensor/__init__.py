"""Sensor platform for the Meraki Home Assistant integration.

This platform sets up various sensor entities for Meraki devices and SSIDs,
including device status, client counts, network information, and SSID-specific
details like availability and channel usage. It uses data coordinators to
fetch and manage data from the Meraki API.
"""

from __future__ import annotations

import inspect
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import (
    DATA_CLIENT,
    DOMAIN,
)
from ..core.api.client import MerakiAPIClient
from ..core.utils.naming_utils import format_device_name
from ..sensor_registry import (
    COMMON_DEVICE_SENSORS,
    get_sensors_for_device_type,
)
from .device.appliance_port import MerakiAppliancePortSensor
from .device.rtsp_url import MerakiRtspUrlSensor as MerakiCameraRTSPUrlSensor
from .network.meraki_network_info import MerakiNetworkInfoSensor
from .network.network_clients import MerakiNetworkClientsSensor
from .network.network_identity import MerakiNetworkIdentitySensor

__all__ = [
    "async_setup_entry",
    "MerakiNetworkClientsSensor",
    "MerakiNetworkIdentitySensor",
    "MerakiNetworkInfoSensor",
    "MerakiAppliancePortSensor",
    "MerakiCameraRTSPUrlSensor",
]


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

    # Get the main data coordinator
    from ..meraki_data_coordinator import MerakiDataCoordinator

    coordinator: MerakiDataCoordinator | None = entry_data.get("coordinator")

    # Note: device_coordinator and network_coordinator were planned but not implemented
    # The main coordinator handles all data including devices and networks
    # Use main coordinator for both device and network data
    device_coordinator = coordinator  # Main coordinator has device data
    network_coordinator = coordinator  # Main coordinator has network data

    # Retrieve the MerakiAPIClient instance
    meraki_api_client: MerakiAPIClient | None = entry_data.get(DATA_CLIENT)

    # Retrieve the NetworkControlService instance
    network_control_service = entry_data.get("network_control_service")

    if not meraki_api_client:
        _LOGGER.error(
            "Meraki API client not found in entry_data. "
            "Cannot set up network client sensors."
        )

    # --- Physical Device Sensor Setup ---
    if device_coordinator and device_coordinator.data:
        physical_devices = device_coordinator.data.get("devices", [])
        for device_info in physical_devices:
            serial = device_info.get("serial")
            if not serial:
                _LOGGER.warning(
                    "Skipping device with missing serial: %s",
                    device_info.get("name", "Unnamed Device with no Serial"),
                )
                continue

            original_device_name = device_info.get("name")
            if not original_device_name:
                model_str = device_info.get("model", "Device")
                fallback_name = f"Meraki {model_str} {serial}"
                device_info["name"] = fallback_name

            formatted_name = format_device_name(device_info, config_entry.options)
            device_info_with_formatted_name = device_info.copy()
            device_info_with_formatted_name["name"] = formatted_name
            for sensor_class in COMMON_DEVICE_SENSORS:
                unique_id = f"{serial}_{sensor_class.__name__}"
                if unique_id not in added_entities:
                    try:
                        entities.append(
                            sensor_class(
                                device_coordinator,
                                device_info_with_formatted_name,
                                config_entry,
                            )
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
                sensors_for_type = get_sensors_for_device_type(product_type, True)
                # Redundant log removed: handled by empty list iteration
                for sensor_class in sensors_for_type:
                    unique_id = f"{serial}_{sensor_class.__name__}"
                    if unique_id not in added_entities:
                        try:
                            sig = inspect.signature(sensor_class.__init__)
                            if "config_entry" in sig.parameters:
                                entities.append(
                                    sensor_class(
                                        device_coordinator,
                                        device_info_with_formatted_name,
                                        config_entry,
                                    )
                                )
                            else:
                                entities.append(
                                    sensor_class(
                                        device_coordinator,
                                        device_info_with_formatted_name,
                                    )
                                )
                            added_entities.add(unique_id)
                        except Exception as e:
                            _LOGGER.error(
                                "Error adding sensor %s for %s (type: %s): %s",
                                sensor_class.__name__,
                                device_info.get("name", serial),
                                product_type,
                                e,
                            )

                # Camera sensors handled by SENSOR_REGISTRY via sensors_for_type loop
            else:
                _LOGGER.warning(
                    "No productType for device %s (Serial: %s), skipping sensors.",
                    device_info.get("name"),
                    serial,
                )

    else:
        _LOGGER.warning(
            "Main coordinator not available or has no data; "
            "skipping physical device sensors."
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
            if (
                unique_id not in added_entities
                and network_control_service
                and coordinator
            ):
                try:
                    entities.append(
                        MerakiNetworkClientsSensor(
                            coordinator,
                            config_entry,
                            network_data,
                            network_control_service,
                        )
                    )
                    added_entities.add(unique_id)
                except Exception as e:
                    _LOGGER.error(
                        "Error adding network clients sensor for %s (%s): %s",
                        network_name,
                        network_id,
                        e,
                    )
            unique_id = f"meraki_network_identity_{network_id}"
            if unique_id not in added_entities and coordinator:
                try:
                    entities.append(
                        MerakiNetworkIdentitySensor(
                            coordinator, network_data, config_entry
                        )
                    )
                    added_entities.add(unique_id)
                except Exception as e:
                    _LOGGER.error(
                        "Error adding network identity sensor for %s (%s): %s",
                        network_name,
                        network_id,
                        e,
                    )
            unique_id = f"{network_id}_network_info"
            if unique_id not in added_entities and coordinator:
                try:
                    entities.append(
                        MerakiNetworkInfoSensor(coordinator, network_data, config_entry)
                    )
                    added_entities.add(unique_id)
                except Exception as e:
                    _LOGGER.error(
                        "Error adding network info sensor for %s (%s): %s",
                        network_name,
                        network_id,
                        e,
                    )

    elif not meraki_api_client:
        _LOGGER.warning(
            "Meraki API client not available; skipping network client sensors."
        )
    elif not network_coordinator or not network_coordinator.data:
        _LOGGER.warning(
            "Main coordinator not available; skipping network-specific sensors."
        )

    if coordinator and coordinator.data:
        for device in coordinator.data.get("devices", []):
            if device.get("productType") == "appliance":
                for port in device.get("ports", []):
                    if (
                        f"{device['serial']}_port_{port['number']}"
                        not in added_entities
                    ):
                        entities.append(
                            MerakiAppliancePortSensor(coordinator, device, port)
                        )
                        added_entities.add(f"{device['serial']}_port_{port['number']}")

    if entities:
        async_add_entities(entities)
    return True
