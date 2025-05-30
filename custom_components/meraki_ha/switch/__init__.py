"""Switch platform for the Meraki Home Assistant integration.

This module is responsible for setting up and initializing switch entities
that represent Meraki SSIDs, allowing them to be enabled or disabled via
Home Assistant.
"""
import logging
from typing import Any, Dict, List  # Added Any, Dict

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Import constants and the central data coordinator
from ..const import ATTR_SSIDS, DATA_COORDINATOR, DOMAIN
from ..coordinators import MerakiDataUpdateCoordinator
# Import the specific switch entity and any utility functions
from .ssid_switch import MerakiSSIDSwitch, match_device_to_ssid

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki SSID switch entities based on a config entry.

    This function is called by Home Assistant to initialize switch entities.
    It retrieves device and SSID information from the central Meraki data
    coordinator and creates `MerakiSSIDSwitch` entities for each relevant SSID
    that can be controlled.

    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry for this Meraki integration instance.
        async_add_entities: Callback function to add entities to Home Assistant.
    """
    coordinator: MerakiDataUpdateCoordinator = hass.data[
        DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    # Ensure coordinator data is available before proceeding
    if coordinator.data is None:
        _LOGGER.error(
            "Meraki coordinator data is not available. Cannot set up switch platform."
        )
        return

    created_switches: List[SwitchEntity] = []
    # The coordinator.data["devices"] is expected to be a list of devices,
    # where each device might have an ATTR_SSIDS key.
    all_devices: List[Dict[str, Any]] = coordinator.data.get("devices", [])

    if not all_devices:
        _LOGGER.info(
            "No Meraki devices found in coordinator data for switch setup.")
        return

    relaxed_matching: bool = coordinator.relaxed_tag_match
    _LOGGER.debug("Switch setup using relaxed_tag_match: %s", relaxed_matching)

    for device_info in all_devices:  # Iterate through all devices
        # SSIDs are typically associated with wireless devices (APs)
        # The match_device_to_ssid function likely handles if a device is
        # appropriate for an SSID.
        ssids_on_device: List[Dict[str, Any]] = device_info.get(ATTR_SSIDS, [])

        if not ssids_on_device:
            _LOGGER.debug(
                "Device '%s' (Serial: %s) has no SSIDs listed under ATTR_SSIDS.",
                device_info.get(
                    "name",
                    "Unknown"),
                device_info.get(
                    "serial",
                    "N/A"))
            continue

        for ssid_info in ssids_on_device:
            ssid_name = ssid_info.get("name", "Unknown SSID")
            # The `match_device_to_ssid` function determines if this SSID, based on its tags
            # and the device's tags (and potentially other APs' tags), should have a switch created.
            # This logic is crucial for deciding which SSIDs are controllable or relevant.
            # It appears to check if *any* device in `all_devices` matches the SSID's tags.
            # This might mean an SSID switch is created for each AP that *could* broadcast it,
            # or one switch per SSID that is matched by at least one AP.
            # The original logic passed `coordinator.data.get("devices", [])`
            # which is `all_devices`.
            if match_device_to_ssid(ssid_info, all_devices, relaxed_matching):
                _LOGGER.debug(
                    "Creating SSID switch for SSID '%s' associated with device '%s' (Serial: %s)",
                    ssid_name,
                    device_info.get(
                        "name",
                        "Unknown"),
                    device_info.get(
                        "serial",
                        "N/A"),
                )
                created_switches.append(
                    MerakiSSIDSwitch(coordinator, device_info, ssid_info)
                )
            else:
                _LOGGER.debug(
                    "SSID '%s' on device '%s' did not meet criteria for switch creation via match_device_to_ssid.",
                    ssid_name,
                    device_info.get(
                        "name",
                        "Unknown"))

    if created_switches:
        async_add_entities(created_switches)
        _LOGGER.debug(
            "Added %d Meraki SSID switch entities.",
            len(created_switches))
    else:
        _LOGGER.debug("No Meraki SSID switch entities were created.")
