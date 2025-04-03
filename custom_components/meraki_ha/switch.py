"""Switch platform for Meraki SSIDs."""

from __future__ import annotations

import logging
import aiohttp

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from typing import List  # Import List from the typing module
from .const import DOMAIN, DATA_COORDINATOR
from .meraki_api.devices import update_device_tags  #  Import update_device_tags

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


class MerakiSSIDSwitch(SwitchEntity):
    """Representation of a Meraki SSID switch."""

    def __init__(
        self, coordinator: DataUpdateCoordinator, device: dict, ssid: dict
    ) -> None:
        """Initialize the Meraki SSID switch."""
        _LOGGER.debug(
            f"Initializing MerakiSSIDSwitch for {ssid['name']}"
        )  #  add debug line
        self.coordinator = coordinator
        self.device = device
        self.ssid = ssid
        self._attr_unique_id = f"{device['serial']}-{ssid['name']}"
        self._attr_name = f"{device['name']} - {ssid['name']}"
        self._attr_is_on = ssid.get(
            "enabled", False
        )  # Get initial state from ssid data

    @property
    def is_on(self) -> bool:
        """Return the state of the SSID."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs) -> None:
        """Enable the SSID."""
        await self._set_ssid_enabled(True)
        self._attr_is_on = True  # Update the local state immediately
        self.async_write_ha_state()  # Notify HA of the change

    async def async_turn_off(self, **kwargs) -> None:
        """Disable the SSID."""
        await self._set_ssid_enabled(False)
        self._attr_is_on = False  # Update the local state immediately
        self.async_write_ha_state()  # Notify HA of the change

    async def _set_ssid_enabled(self, enabled: bool) -> None:
        """Set the SSID enabled state via Meraki API by updating device tags."""

        _LOGGER.debug(f"Setting SSID {self.ssid['name']} to enabled: {enabled}")
        ssid_tag = f"ssid_{self.ssid['name']}_enabled"
        current_tags: List[str] = self.device.get("tags", [])  #  Get current tags
        new_tags: List[str] = current_tags.copy()

        if enabled:
            if ssid_tag not in current_tags:
                new_tags.append(ssid_tag)
                _LOGGER.debug(
                    f"Adding tag {ssid_tag} to device {self.device['serial']}"
                )
        else:
            if ssid_tag in current_tags:
                new_tags.remove(ssid_tag)
                _LOGGER.debug(
                    f"Removing tag {ssid_tag} from device {self.device['serial']}"
                )

        try:
            await update_device_tags(
                self.coordinator.session,
                self.coordinator.api_key,
                self.device["serial"],
                new_tags,
            )
            _LOGGER.info(
                f"Successfully set SSID {self.ssid['name']} to enabled: {enabled} "
                f"on device {self.device['name']}"
            )
            #  Refresh data to reflect the change
            await self.coordinator.async_request_refresh()
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Error setting SSID enabled state: {e}")

    async def async_update(self) -> None:
        """Update the SSID state."""
        #  The coordinator should handle updating the SSID state,
        #  so we don't need to do anything here.
        #  We might want to add error handling or logging in the future.
        pass
