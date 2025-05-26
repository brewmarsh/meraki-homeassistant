"""Sensor platform for the Meraki Home Assistant integration.

This module is responsible for setting up and initializing various sensor
entities that represent data points from Meraki devices and networks.
It discovers devices and networks through the central Meraki data coordinator
and creates corresponding sensor entities.
"""
import logging
from typing import Any, Dict, List, Optional # Added Any, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Import specific sensor entity classes
from .connected_clients import MerakiConnectedClientsSensor
from .device_status import MerakiDeviceStatusSensor
from .network_clients import MerakiNetworkClientCountSensor
from .radio_settings import MerakiRadioSettingsSensor
from .ssid import create_ssid_sensors # Function that creates multiple SSID-related sensors
from .ssid_availability import MerakiSSIDAvailabilitySensor
from .uplink_status import MerakiUplinkStatusSensor

# Import from parent directory for constants and coordinator
from ..const import ATTR_SSIDS, DATA_COORDINATOR, DOMAIN
from ..coordinator import MerakiDataUpdateCoordinator

# Assuming get_network_ids_and_names is a utility function from the meraki_api package
# It should be imported if used, or its functionality incorporated/mocked if not central.
# For this exercise, we assume it's a valid import path.
# from ..meraki_api.networks import get_network_ids_and_names # Removed
from ..meraki_api._api_client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki sensor entities based on a config entry.

    This function is called by Home Assistant to initialize sensor entities.
    It retrieves device and network information from the central Meraki data
    coordinator and creates various sensor entities for different aspects of
    the Meraki setup (device status, client counts, radio settings, SSIDs, etc.).

    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry for this Meraki integration instance.
        async_add_entities: Callback function to add entities to Home Assistant.
    """
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        DATA_COORDINATOR
    ]

    # Ensure coordinator data is available before proceeding
    if coordinator.data is None:
        _LOGGER.error(
            "Meraki coordinator data is not available. Cannot set up sensor platform."
        )
        return

    created_sensors: List[SensorEntity] = []
    devices: List[Dict[str, Any]] = coordinator.data.get("devices", [])
    _LOGGER.debug("Found %d devices in coordinator data for sensor setup.", len(devices))

    for device_info in devices: # Use more descriptive variable name
        device_serial = device_info.get("serial")
        device_name = device_info.get("name", "Unknown Meraki Device")
        device_model = device_info.get("model", "")

        if not device_serial:
            _LOGGER.warning(
                "Skipping sensor setup for device with no serial: %s", device_name
            )
            continue

        _LOGGER.debug(
            "Processing device for sensors: Name='%s', Serial='%s', Model='%s'",
            device_name,
            device_serial,
            device_model,
        )

        # Add common device status sensor
        created_sensors.append(MerakiDeviceStatusSensor(coordinator, device_info))

        # Add sensors specific to MR (Wireless AP) or GR (Gateway with AP) models
        if device_model.upper().startswith(("MR", "GR")):
            _LOGGER.debug("Adding MR/GR specific sensors for '%s'", device_name)
            created_sensors.append(
                MerakiConnectedClientsSensor(coordinator, device_info)
            )
            created_sensors.append(MerakiRadioSettingsSensor(coordinator, device_info))

            # Process SSIDs associated with this wireless device
            # Assuming ATTR_SSIDS in device_info is a list of SSID dicts
            # This structure depends on how MerakiDataUpdateCoordinator populates device data.
            ssids_on_device: List[Dict[str, Any]] = device_info.get(ATTR_SSIDS, [])
            if ssids_on_device:
                for ssid_info in ssids_on_device:
                    ssid_name = ssid_info.get("name", "Unknown SSID")
                    _LOGGER.debug(
                        "Creating SSID sensors for '%s' on device '%s'",
                        ssid_name,
                        device_name,
                    )
                    # create_ssid_sensors is expected to return a list of sensor entities
                    created_sensors.extend(
                        create_ssid_sensors(coordinator, device_info, ssid_info)
                    )
                    created_sensors.append(
                        MerakiSSIDAvailabilitySensor(coordinator, device_info, ssid_info)
                    )
            else:
                _LOGGER.debug("No SSIDs found directly under device '%s' for sensor setup.", device_name)


        # Add sensors specific to MX (Security Appliance) models
        elif device_model.upper().startswith("MX"):
            _LOGGER.debug("Adding MX specific sensors for '%s'", device_name)
            created_sensors.append(MerakiUplinkStatusSensor(coordinator, device_info))

    # Add sensors that are network-wide (not tied to a specific device)
    # The function `get_network_ids_and_names` is assumed to be an async utility
    # that fetches basic network info. If this info is already in `coordinator.data["networks"]`,
    # that should be preferred to avoid extra API calls.
    
    # Prefer using network data from coordinator if available
    networks_data: Optional[List[Dict[str, Any]]] = coordinator.data.get("networks")
    
    if networks_data is None:
        _LOGGER.info("Network data not directly in coordinator, attempting API call for network list (sensor setup).")
        # Fallback to API call if not in coordinator.data (less ideal)
        api_client = MerakiAPIClient(api_key=coordinator.api_key, org_id=coordinator.org_id)
        networks_data = await api_client.networks.async_get_network_ids_and_names(
            organization_id=coordinator.org_id
        )

    if networks_data:
        _LOGGER.debug("Processing %d networks for network-wide sensors.", len(networks_data))
        for network_info in networks_data:
            network_id = network_info.get("id")
            network_name = network_info.get("name", "Unknown Network")
            if not network_id:
                _LOGGER.warning("Skipping network with no ID for client count sensor: %s", network_name)
                continue
            
            created_sensors.append(
                MerakiNetworkClientCountSensor(
                    coordinator, network_id, network_name
                )
            )
    else:
        _LOGGER.warning(
            "No network information available to set up network-wide client count sensors."
        )

    if created_sensors:
        async_add_entities(created_sensors)
        _LOGGER.info("Added %d Meraki sensor entities.", len(created_sensors))
    else:
        _LOGGER.info("No Meraki sensor entities were created.")
