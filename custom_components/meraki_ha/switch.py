"""Switch platform for Meraki SSIDs."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN, DATA_COORDINATOR
from .meraki_ssid_switch import MerakiSSIDSwitch

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Meraki SSID switch platform."""
    _LOGGER.debug("SSID Switch async_setup_entry called")
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        DATA_COORDINATOR
    ]
    _LOGGER.debug(f"Coordinator Data in SSID Switch: {coordinator.data}")
    switches = []  #  Initialize an empty list for switches

    #  Check if SSIDs are in the coordinator.data
    ssids = coordinator.data.get("ssids", [])
    _LOGGER.debug(f"Retrieved SSIDs: {ssids}")  #  add debug line
    if ssids:
        _LOGGER.debug(f"SSIDs found in coordinator data: {ssids}")
        for ssid in ssids:
            _LOGGER.debug(f"Processing SSID: {ssid['name']}")  #  add debug line
            #  Find the corresponding device based on SSID availabilityTags
            devices = [
                d
                for d in coordinator.data["devices"]
                if ssid.get("availabilityTags")
                and any(tag in d.get("tags", []) for tag in ssid["availabilityTags"])
                and d.get("model")[0:2] == "MR"  # only MR devices have SSIDs
            ]
            if devices:
                for device in devices:  #  Create a switch for each device
                    _LOGGER.debug(
                        f"Creating switch for SSID: {ssid['name']} on device"
                        f" {device['name']}"
                    )
                    switches.append(MerakiSSIDSwitch(coordinator, device, ssid))
                    _LOGGER.debug(f"Added switch entity for SSID: {ssid['name']}")
            else:
                _LOGGER.warning(f"No matching device found for SSID: {ssid['name']}")
    else:
        _LOGGER.debug("No SSIDs found in coordinator data.")

    _LOGGER.debug(f"Total Switches created: {len(switches)}")
    async_add_entities(switches)
