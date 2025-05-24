"""Sets up the sensor platform for the Meraki Home Assistant integration.

This module is responsible for initializing and adding all the sensor entities
that provide information from Meraki devices and networks. It iterates through
devices and networks discovered by the central `MerakiDataUpdateCoordinator`
and creates corresponding sensor entities.
"""

import logging
from typing import List

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity

from .device_status import MerakiDeviceStatusSensor
from .connected_clients import MerakiConnectedClientsSensor
from .radio_settings import MerakiRadioSettingsSensor
from .uplink_status import MerakiUplinkStatusSensor
from .network_clients import MerakiNetworkClientCountSensor
from .ssid import create_ssid_sensors
from .ssid_availability import MerakiSSIDAvailabilitySensor
from ..meraki_api.networks import get_network_ids_and_names
from ..const import DOMAIN, DATA_COORDINATOR, ATTR_SSIDS
from ..coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki sensor entities based on a config entry.

    This function is called by Home Assistant when a Meraki config entry is
    set up. It retrieves the central data coordinator and then iterates through
    the devices and networks managed by that coordinator to create and add
    the appropriate sensor entities.

    The types of sensors created depend on the device model or network properties:
    - All devices get a `MerakiDeviceStatusSensor`.
    - Wireless devices (MR/GR models) get `MerakiConnectedClientsSensor`,
      `MerakiRadioSettingsSensor`, and SSID-specific sensors (via `create_ssid_sensors`
      and `MerakiSSIDAvailabilitySensor`) if SSIDs are defined.
    - Security appliances (MX models) get a `MerakiUplinkStatusSensor`.
    - Each network gets a `MerakiNetworkClientCountSensor`.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        entry (ConfigEntry): The configuration entry for this Meraki integration instance.
        async_add_entities (AddEntitiesCallback): Callback function to add entities
            to Home Assistant.
    """
    # Retrieve the central data coordinator from hass.data.
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]

    # List to hold all sensor entities to be added.
    sensors_to_add: List[SensorEntity] = []

    # Ensure coordinator.data is available and contains device information.
    # The coordinator.data should have been populated by its first refresh.
    if coordinator.data and "devices" in coordinator.data:
        devices = coordinator.data.get("devices", [])
        _LOGGER.info(
            "Setting up Meraki sensors. Found %d devices in coordinator data.",
            len(devices),
        )

        for device_info in devices:
            if not isinstance(device_info, dict):
                _LOGGER.warning("Skipping non-dictionary device item: %s", device_info)
                continue

            device_serial = device_info.get("serial")
            if not device_serial:
                _LOGGER.warning("Device found without serial: %s. Skipping.", device_info)
                continue

            _LOGGER.debug(
                "Processing device for sensor setup: Name: %s, Serial: %s, Model: %s",
                device_info.get("name", "N/A"),
                device_serial,
                device_info.get("model", "N/A"),
            )

            # Add a status sensor for every device.
            sensors_to_add.append(MerakiDeviceStatusSensor(coordinator, device_info))

            device_model = device_info.get("model", "")
            # Add sensors specific to wireless access points (MR/GR models).
            if device_model.startswith("MR") or device_model.startswith("GR"):
                _LOGGER.debug(
                    "Adding Wireless (MR/GR) specific sensors for device: %s",
                    device_serial,
                )
                sensors_to_add.append(
                    MerakiConnectedClientsSensor(coordinator, device_info)
                )
                sensors_to_add.append(
                    MerakiRadioSettingsSensor(coordinator, device_info)
                )
                # Add sensors for each SSID configured on this wireless AP.
                # Assumes ATTR_SSIDS is populated in device_info by the coordinator.
                device_ssids = device_info.get(ATTR_SSIDS, [])
                if isinstance(device_ssids, list):
                    for ssid_info in device_ssids:
                        if isinstance(ssid_info, dict):
                            _LOGGER.debug(
                                "Creating SSID-specific sensors for SSID '%s' on device %s",
                                ssid_info.get("name", "N/A"),
                                device_serial,
                            )
                            # `create_ssid_sensors` returns a list of sensors (e.g., channel, client count per SSID)
                            sensors_to_add.extend(
                                create_ssid_sensors(coordinator, device_info, ssid_info)
                            )
                            sensors_to_add.append(
                                MerakiSSIDAvailabilitySensor(
                                    coordinator, device_info, ssid_info
                                )
                            )
                        else:
                            _LOGGER.warning("Skipping non-dictionary SSID item: %s for device %s", ssid_info, device_serial)
                else:
                     _LOGGER.warning("ATTR_SSIDS for device %s is not a list: %s", device_serial, device_ssids)


            # Add sensors specific to security appliances (MX models).
            elif device_model.startswith("MX"):
                _LOGGER.debug(
                    "Adding Security Appliance (MX) specific sensors for device: %s",
                    device_serial,
                )
                sensors_to_add.append(
                    MerakiUplinkStatusSensor(coordinator, device_info)
                )
            # TODO: Add elif blocks for other device types (MS, MV, MT) if they have specific sensors.
    else:
        _LOGGER.warning(
            "Coordinator data is not yet available or does not contain 'devices'. "
            "Cannot set up device-specific sensors."
        )

    # Fetch network information to create network-level sensors.
    # This makes a direct API call, consider if this should also be part of the coordinator's data.
    try:
        networks = await get_network_ids_and_names(
            coordinator.api_key, coordinator.org_id
        )
        _LOGGER.debug("Networks retrieved for sensor setup: %s", networks)
    except Exception as e: # Catch potential errors from get_network_ids_and_names
        _LOGGER.error("Failed to retrieve network IDs and names for sensor setup: %s", e)
        networks = None


    if networks: # Check if networks is not None and not empty
        for network_info in networks:
            if isinstance(network_info, dict) and "id" in network_info and "name" in network_info:
                sensors_to_add.append(
                    MerakiNetworkClientCountSensor(
                        coordinator, network_info["id"], network_info["name"]
                    )
                )
            else:
                _LOGGER.warning("Skipping malformed network item for sensor setup: %s", network_info)
    else:
        _LOGGER.info("No networks found or error in retrieval, skipping network-level sensors.")


    # Add all collected sensor entities to Home Assistant.
    if sensors_to_add:
        async_add_entities(sensors_to_add)
        _LOGGER.info("Successfully added %d Meraki sensor entities.", len(sensors_to_add))
    else:
        _LOGGER.info("No Meraki sensor entities were added.")
