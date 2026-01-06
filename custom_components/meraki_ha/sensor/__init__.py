<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
"""Sensor platform for the Meraki Home Assistant integration."""

import asyncio
import logging

from homeassistant.components.sensor import SensorEntity
<<<<<<< HEAD
=======
"""Sensor platform for the Meraki Home Assistant integration.

This platform sets up various sensor entities for Meraki devices and SSIDs,
including device status, client counts, network information, and SSID-specific
details like availability and channel usage. It uses data coordinators to
fetch and manage data from the Meraki API.
"""

import inspect
import logging
from typing import Optional  # Added Optional

>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

<<<<<<< HEAD
<<<<<<< HEAD
from ..const import DOMAIN
=======
from ..const import (
    DATA_CLIENT,
    DOMAIN,
)
from ..core.api.client import MerakiAPIClient
from ..core.utils.naming_utils import format_device_name
from ..meraki_data_coordinator import MerakiDataCoordinator
from ..sensor_registry import (
    COMMON_DEVICE_SENSORS,
    get_sensors_for_device_type,
)
from .device.appliance_port import MerakiAppliancePortSensor
from .device.rtsp_url import MerakiRtspUrlSensor as MerakiCameraRTSPUrlSensor
from .network.network_clients import MerakiNetworkClientsSensor

__all__ = [
    "async_setup_entry",
    "MerakiNetworkClientsSensor",
    "MerakiAppliancePortSensor",
    "MerakiCameraRTSPUrlSensor",
]

>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
from ..const import CONF_ENABLE_ORG_SENSORS, DOMAIN
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki sensor entities from a config entry."""
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    discovered_entities = entry_data.get("entities", [])
    sensor_entities = [e for e in discovered_entities if isinstance(e, SensorEntity)]

<<<<<<< HEAD
=======
    # Filter out organization sensors if disabled
    # Org sensors are typically identifiable by their unique_id starting with org prefix
    # or their class.
    # Based on inspection, org sensors are added to discovered_entities.
    # We can filter them here.

    if not config_entry.options.get(CONF_ENABLE_ORG_SENSORS, True):
        _LOGGER.debug("Organization sensors are disabled.")
        # Identify org sensors.
        # In MerakiOrganizationEntity, unique_id is f"{org_id}_{key}" usually.
        # Let's check the class name or module of the entity.
        filtered_entities = []
        for entity in sensor_entities:
            # Check if it is an org sensor
            # Using class name check or module check
            if "MerakiOrganization" in entity.__class__.__name__:
                _LOGGER.debug("Skipping organization sensor %s", entity.name)
                continue
            filtered_entities.append(entity)
        sensor_entities = filtered_entities

>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    if sensor_entities:
        _LOGGER.debug("Adding %d sensor entities", len(sensor_entities))
        chunk_size = 50
        for i in range(0, len(sensor_entities), chunk_size):
            chunk = sensor_entities[i : i + chunk_size]
            async_add_entities(chunk)
            if len(sensor_entities) > chunk_size:
                await asyncio.sleep(1)

<<<<<<< HEAD
=======
    entities = []
    added_entities = set()

    # Get the entry specific data store
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Get the main data coordinator for physical devices
    device_coordinator: MerakiDataCoordinator = entry_data.get("coordinator")
    # Network coordinator is no longer separate; use the main coordinator
    network_coordinator: MerakiDataCoordinator = entry_data.get("coordinator")

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
                sensors_for_type = get_sensors_for_device_type(product_type)
                # if not sensors_for_type: # Removed: Redundant log, handled by empty list iteration
                #   pass
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
                    if (
                        f"{device['serial']}_port_{port['number']}"
                        not in added_entities
                    ):
                        entities.append(
                            MerakiAppliancePortSensor(device_coordinator, device, port)
                        )
                        added_entities.add(f"{device['serial']}_port_{port['number']}")

    if entities:
        async_add_entities(entities)
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    return True
