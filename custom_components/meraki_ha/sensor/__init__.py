"""Sensor platform for the Meraki Home Assistant integration.

This module is responsible for setting up and initializing various sensor
entities that represent data points from Meraki devices and networks.
It discovers devices and networks using data provided by the central
`MerakiDataUpdateCoordinator` and creates corresponding sensor entities.
"""
import logging
from typing import Any, Dict, List, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Import specific sensor entity classes
from custom_components.meraki_ha.sensor.connected_clients import MerakiConnectedClientsSensor
from custom_components.meraki_ha.sensor.device_status import MerakiDeviceStatusSensor
from custom_components.meraki_ha.sensor.network_clients import MerakiNetworkClientCountSensor
from custom_components.meraki_ha.sensor.radio_settings import MerakiRadioSettingsSensor
from custom_components.meraki_ha.sensor.ssid import create_ssid_sensors # Function to create multiple SSID-related sensors
from custom_components.meraki_ha.sensor.ssid_availability import MerakiSSIDAvailabilitySensor
from custom_components.meraki_ha.sensor.uplink_status import MerakiUplinkStatusSensor

# Import from parent directory for constants and coordinator type
from custom_components.meraki_ha.const import ATTR_SSIDS, DATA_COORDINATOR, DOMAIN # ATTR_SSIDS for device-specific SSIDs
from custom_components.meraki_ha.coordinators.base_coordinator import MerakiDataUpdateCoordinator # Corrected import path

# Obsolete imports for MerakiAPIClient and get_network_ids_and_names are removed.

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki sensor entities from a configuration entry.

    This function is called by Home Assistant to initialize sensor entities.
    It retrieves device, network, and SSID information from the central
    `MerakiDataUpdateCoordinator`. Based on this data, it creates various
    sensor entities for device status, client counts, radio settings,
    SSID availability, uplink status, etc.

    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry for this Meraki integration instance.
        async_add_entities: Callback function to add entities to Home Assistant.
    """
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        DATA_COORDINATOR # Key to access the coordinator in hass.data
    ]

    # Ensure coordinator data is available before proceeding with sensor setup.
    if coordinator.data is None:
        _LOGGER.error(
            "Meraki coordinator data is not available. Cannot set up Meraki sensor platform for entry_id: %s.",
            config_entry.entry_id
        )
        return

    created_sensors: List[SensorEntity] = []
    # Device data, including tags and MR-specific details, comes from the coordinator.
    devices: List[Dict[str, Any]] = coordinator.data.get("devices", [])
    _LOGGER.debug("Found %d devices in coordinator data for Meraki sensor setup.", len(devices))

    for device_info in devices:
        device_serial = device_info.get("serial")
        device_name = device_info.get("name", f"Unknown Meraki Device ({device_serial or 'No Serial'})")
        device_model = device_info.get("model", "")

        if not device_serial:
            _LOGGER.warning(
                "Skipping sensor setup for a device with no serial number. Device data: %s", device_info
            )
            continue

        _LOGGER.debug(
            "Processing device for sensors: Name='%s', Serial='%s', Model='%s'",
            device_name, device_serial, device_model,
        )

        # Add common device status sensor for all devices.
        created_sensors.append(MerakiDeviceStatusSensor(coordinator, device_info))

        # Add sensors specific to MR (Wireless AP) or GR (Gateway with AP) models.
        # These models have wireless capabilities.
        if device_model.upper().startswith(("MR", "GR")):
            _LOGGER.debug("Adding wireless-specific (MR/GR) sensors for device: %s", device_name)
            created_sensors.append(MerakiConnectedClientsSensor(coordinator, device_info))
            created_sensors.append(MerakiRadioSettingsSensor(coordinator, device_info))

            # Process SSIDs associated with this wireless device.
            # The `ATTR_SSIDS` key in `device_info` (e.g., "ssids_on_device") is populated
            # by the DataAggregator if SSIDs are directly linked to devices in the aggregated data.
            # If SSIDs are globally available, they might be fetched from `coordinator.data.get("ssids")`
            # and then filtered by network or tags if necessary.
            # Current structure implies SSIDs relevant to a device are nested or linked.
            # Assuming `ATTR_SSIDS` ('ssids') in `coordinator.data` holds all SSIDs,
            # and they need to be matched to devices if not directly nested.
            # For this review, assuming the existing logic of `device_info.get(ATTR_SSIDS, [])`
            # is correct based on how `DataAggregator` structures data.
            # If `ATTR_SSIDS` is meant to be a global list, the logic here would differ.
            # Let's clarify: `ATTR_SSIDS` refers to SSIDs *configured on* a device (e.g. for APs).
            # The `coordinator.data` will have a top-level "ssids" key from `DataAggregator`.
            # The `device_info` from `coordinator.data.get("devices")` should contain a list of
            # SSIDs that are relevant to *that specific device* if `DataAggregator` structures it that way.
            # The current `device_info.get(ATTR_SSIDS, [])` implies SSIDs are directly part of the device dictionary.
            # This is consistent if DataAggregator adds an 'ssids_on_device' or similar key.
            
            # Let's assume `ATTR_SSIDS` refers to a key within `device_info` that lists SSIDs for that device.
            # This is populated by `DataAggregator` if it links SSIDs to specific devices.
            ssids_configured_on_device: List[Dict[str, Any]] = device_info.get(ATTR_SSIDS, [])
            if ssids_configured_on_device:
                for ssid_info_on_device in ssids_configured_on_device:
                    ssid_name = ssid_info_on_device.get("name", "Unknown SSID")
                    _LOGGER.debug(
                        "Creating sensors for SSID '%s' on device '%s'", ssid_name, device_name,
                    )
                    # `create_ssid_sensors` generates sensors like status, auth mode, etc.
                    created_sensors.extend(
                        create_ssid_sensors(coordinator, device_info, ssid_info_on_device)
                    )
                    # `MerakiSSIDAvailabilitySensor` checks if this specific SSID is broadcasting.
                    created_sensors.append(
                        MerakiSSIDAvailabilitySensor(coordinator, device_info, ssid_info_on_device)
                    )
            else:
                _LOGGER.debug("No specific SSIDs found under device '%s' for detailed sensor setup. "
                              "Global SSID sensors might still be created if applicable.", device_name)

        # Add sensors specific to MX (Security Appliance) models.
        elif device_model.upper().startswith("MX"):
            _LOGGER.debug("Adding security appliance (MX) specific sensors for device: %s", device_name)
            created_sensors.append(MerakiUplinkStatusSensor(coordinator, device_info))

    # Add sensors that are network-wide (not tied to a specific device).
    # Network information is sourced directly from `coordinator.data["networks"]`.
    networks_data: Optional[List[Dict[str, Any]]] = coordinator.data.get("networks")

    if networks_data:
        _LOGGER.debug("Processing %d networks for network-wide client count sensors.", len(networks_data))
        for network_info in networks_data:
            network_id = network_info.get("id")
            network_name = network_info.get("name", f"Unknown Network ({network_id or 'No ID'})")
            if not network_id:
                _LOGGER.warning("Skipping network client count sensor for a network with no ID. Network data: %s", network_info)
                continue
            
            # Create a sensor to count total clients per network.
            created_sensors.append(
                MerakiNetworkClientCountSensor(coordinator, network_id, network_name)
            )
    else:
        _LOGGER.warning(
            "No network information available in coordinator.data. "
            "Cannot set up network-wide client count sensors for entry_id: %s.",
            config_entry.entry_id
        )

    if created_sensors:
        async_add_entities(created_sensors)
        _LOGGER.debug("Added %d Meraki sensor entities for entry_id: %s.", len(created_sensors), config_entry.entry_id)
    else:
        _LOGGER.info("No Meraki sensor entities were created for entry_id: %s.", config_entry.entry_id)
