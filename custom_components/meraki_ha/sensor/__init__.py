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
from ..coordinators.base_coordinator import MerakiDataUpdateCoordinator
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator
from ..api.meraki_api import MerakiAPIClient
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


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki sensor entities from a config entry."""
    entities = []

    # Get the entry specific data store
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Get the main data coordinator for physical devices
    main_coordinator: MerakiDataUpdateCoordinator = entry_data.get(DATA_COORDINATOR)

    # Retrieve the MerakiAPIClient instance
    meraki_api_client: Optional[MerakiAPIClient] = entry_data.get(DATA_CLIENT)

    if not meraki_api_client:
        _LOGGER.error(
            "Meraki API client not found in entry_data. Cannot set up network client sensors."
        )

    # --- Organization-level Sensor Setup ---
    if main_coordinator and main_coordinator.data:
        organization_id = main_coordinator.org_id
        org_name = main_coordinator.data.get("org_name", organization_id)

        entities.append(
            MerakiOrgDeviceTypeClientsSensor(
                coordinator=main_coordinator,
                organization_id=organization_id,
                organization_name=org_name,
            )
        )
        entities.append(
            MerakiOrganizationSSIDClientsSensor(
                coordinator=main_coordinator,
                org_id=organization_id,
                org_name=org_name,
            )
        )
        entities.append(
            MerakiOrganizationWirelessClientsSensor(
                coordinator=main_coordinator,
                org_id=organization_id,
                org_name=org_name,
            )
        )
        entities.append(
            MerakiOrganizationApplianceClientsSensor(
                coordinator=main_coordinator,
                org_id=organization_id,
                org_name=org_name,
            )
        )
    else:
        _LOGGER.warning(
            "Main coordinator not available or has no data; skipping organization-level sensors."
        )

    # --- Physical Device Sensor Setup ---
    if main_coordinator and main_coordinator.data:
        physical_devices = main_coordinator.data.get("devices", [])
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

            for sensor_class in COMMON_DEVICE_SENSORS:
                try:
                    entities.append(sensor_class(main_coordinator, device_info))
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
                    try:
                        entities.append(sensor_class(main_coordinator, device_info))
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
    if main_coordinator and main_coordinator.data and meraki_api_client:
        networks = main_coordinator.data.get("networks", [])
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
            try:
                entities.append(
                    MerakiNetworkClientsSensor(
                        main_coordinator, network_id, network_name
                    )
                )
                entities.append(
                    MerakiNetworkIdentitySensor(main_coordinator, network_data)
                )
                entities.append(MerakiNetworkInfoSensor(main_coordinator, network_data))
            except Exception as e:
                _LOGGER.error(
                    "Meraki HA: Error adding network sensors for %s (ID: %s): %s",
                    network_name,
                    network_id,
                    e,
                )

    elif not meraki_api_client:
        _LOGGER.warning(
            "Meraki API client not available; skipping MerakiNetworkClientsSensor setup."
        )
    elif not main_coordinator or not main_coordinator.data:
        _LOGGER.warning(
            "Main coordinator not available or has no data; skipping all network-specific sensors."
        )

    coordinators_map = entry_data.get("coordinators")
    ssid_coordinator: Optional[SSIDDeviceCoordinator] = None  # Initialize
    if coordinators_map:
        ssid_coordinator = coordinators_map.get(DATA_SSID_DEVICES_COORDINATOR)

    # --- SSID "Device" Sensor Setup ---
    if ssid_coordinator and ssid_coordinator.data:
        enabled_ssids_info_list = list(ssid_coordinator.data.values())
        for ssid_info_data in enabled_ssids_info_list:
            new_ssid_sensors = create_ssid_sensors(
                ssid_coordinator, ssid_info_data, ssid_info_data
            )
            entities.extend(new_ssid_sensors)
    else:
        _LOGGER.warning(
            "SSID coordinator (SSIDDeviceCoordinator) not available or has no data; skipping SSID sensors."
        )

    if entities:
        async_add_entities(entities)
    return True
