"""Sets up the switch platform for the Meraki Home Assistant integration.

This module is responsible for initializing and adding switch entities that
allow users to control aspects of their Meraki network, primarily the
enabled state of SSIDs on specific devices.
"""

import logging
from typing import List

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.switch import SwitchEntity

from .ssid_switch import MerakiSSIDSwitch, match_device_to_ssid
from ..const import DOMAIN, DATA_COORDINATOR, ATTR_SSIDS
from ..coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki SSID switch entities based on a config entry.

    This function is called by Home Assistant when a Meraki config entry is
    set up for the switch platform. It retrieves the central data coordinator
    and iterates through the devices and their associated SSIDs.

    A `MerakiSSIDSwitch` entity is created for each SSID that is determined
    to be controllable on a specific device. The `match_device_to_ssid`
    function is used to determine if an SSID should be manageable on a given
    device, potentially based on device tags and the `relaxed_tag_match`
    setting from the coordinator.

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

    # List to hold all switch entities to be added.
    switches_to_add: List[SwitchEntity] = []

    # Get the relaxed_tag_match setting from the coordinator, which influences
    # how SSIDs are associated with devices for control.
    relaxed_matching = coordinator.relaxed_tag_match
    _LOGGER.debug("Relaxed tag matching for SSID switches is set to: %s", relaxed_matching)

    # Ensure coordinator.data and device list are available.
    if coordinator.data and "devices" in coordinator.data:
        all_devices_data = coordinator.data.get("devices", [])
        _LOGGER.info(
            "Setting up Meraki SSID switches. Found %d devices in coordinator data.",
            len(all_devices_data),
        )

        for device_info in all_devices_data:
            if not isinstance(device_info, dict):
                _LOGGER.warning("Skipping non-dictionary device item: %s", device_info)
                continue

            device_serial = device_info.get("serial")
            if not device_serial:
                _LOGGER.warning("Device found without serial: %s. Skipping.", device_info)
                continue

            # Check if the device has SSIDs defined for it in the coordinator's data.
            # The ATTR_SSIDS key should hold a list of SSID information relevant to this device.
            device_ssids = device_info.get(ATTR_SSIDS, [])
            if isinstance(device_ssids, list) and device_ssids:
                _LOGGER.debug(
                    "Device %s has %d SSIDs listed. Checking for switch creation.",
                    device_serial,
                    len(device_ssids),
                )
                for ssid_info in device_ssids:
                    if not isinstance(ssid_info, dict):
                        _LOGGER.warning("Skipping non-dictionary SSID item for device %s: %s", device_serial, ssid_info)
                        continue

                    # The `match_device_to_ssid` function determines if this specific SSID
                    # should be controllable as a switch on this particular device.
                    # This logic might involve checking device tags against SSID configurations
                    # or other criteria defined in `match_device_to_ssid`.
                    # It uses all_devices_data for context if matching involves cross-device checks (e.g. network-wide tags).
                    if match_device_to_ssid(
                        ssid_info, all_devices_data, relaxed_matching
                    ):
                        _LOGGER.info(
                            "Creating SSID switch for SSID '%s' (Number: %s) on device %s (Serial: %s)",
                            ssid_info.get("name", "N/A"),
                            ssid_info.get("number", "N/A"),
                            device_info.get("name", "N/A"),
                            device_serial,
                        )
                        switches_to_add.append(
                            MerakiSSIDSwitch(coordinator, device_info, ssid_info)
                        )
                    else:
                        _LOGGER.debug(
                            "SSID '%s' on device %s did not match criteria for switch creation.",
                            ssid_info.get("name", "N/A"),
                            device_serial,
                        )
            else:
                _LOGGER.debug(
                    "No SSIDs found or ATTR_SSIDS not a list for device %s. No SSID switches will be created for it.",
                    device_serial,
                )
    else:
        _LOGGER.warning(
            "Coordinator data is not yet available or does not contain 'devices'. "
            "Cannot set up SSID switches."
        )

    # Add all collected switch entities to Home Assistant.
    if switches_to_add:
        async_add_entities(switches_to_add)
        _LOGGER.info(
            "Successfully added %d Meraki SSID switch entities.", len(switches_to_add)
        )
    else:
        _LOGGER.info("No Meraki SSID switch entities were added.")
