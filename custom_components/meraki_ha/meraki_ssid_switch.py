"""Meraki SSID Switch platform."""

import logging
import aiohttp

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from typing import List
from .meraki_api.devices import update_device_tags

_LOGGER = logging.getLogger(__name__)


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
                self.coordinator.api_key,  # Get API key from coordinator
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
