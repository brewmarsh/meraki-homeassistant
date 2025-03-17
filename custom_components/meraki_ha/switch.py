"""Switch platform for Meraki SSIDs."""

from __future__ import annotations

import logging
import aiohttp

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DATA_COORDINATOR
from .coordinator import MerakiCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Meraki SSID switch platform."""
    _LOGGER.debug("SSID Switch async_setup_entry called")
    coordinator: MerakiCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        DATA_COORDINATOR
    ]
    _LOGGER.debug(f"Coordinator Data in SSID Switch: {coordinator.data}")
    switches = []  # Initialize an empty list for switches

    for device in coordinator.data["devices"]:
        _LOGGER.debug(f"Checking device: {device}")
        if device.get("productType") == "wireless" and device.get("ssids"):
            _LOGGER.debug(f"Wireless device found: {device['name']}")
            try:
                ssids = device["ssids"]
                _LOGGER.debug(f"SSIDs found: {ssids}")
                for ssid in ssids:
                    _LOGGER.debug(f"Creating switch for SSID: {ssid['name']}")
                    switches.append(MerakiSSIDSwitch(coordinator, device, ssid))
                    _LOGGER.debug(f"Added switch entity for SSID: {ssid['name']}")
            except KeyError:
                _LOGGER.debug(f"No SSIDs found for device: {device['name']}")

    async_add_entities(switches)


class MerakiSSIDSwitch(SwitchEntity):
    """Representation of a Meraki SSID switch."""

    def __init__(
        self, coordinator: MerakiCoordinator, device: dict, ssid: dict
    ) -> None:
        """Initialize the Meraki SSID switch."""
        self.coordinator = coordinator
        self.device = device
        self.ssid = ssid
        self._attr_unique_id = f"{device['serial']}-{ssid['name']}"
        self._attr_name = f"{device['name']} - {ssid['name']}"

    @property
    def is_on(self) -> bool:
        """Return the state of the SSID."""
        return self.ssid.get("enabled", False)

    async def async_turn_on(self, **kwargs) -> None:
        """Enable the SSID."""
        await self._set_ssid_enabled(True)

    async def async_turn_off(self, **kwargs) -> None:
        """Disable the SSID."""
        await self._set_ssid_enabled(False)

    async def _set_ssid_enabled(self, enabled: bool) -> None:
        """Set the SSID enabled state via Meraki API."""
        _LOGGER.debug(f"Setting SSID {self.ssid['name']} to enabled: {enabled}")
        api_key = self.coordinator.config_entry.options.get("meraki_api_key")
        network_id = self.device.get("networkId")
        ssid_number = self.ssid.get("number")
        if not network_id or ssid_number is None:
            _LOGGER.error("Network ID or SSID number not found.")
            return

        url = f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids/{ssid_number}"
        headers = {
            "X-Cisco-Meraki-API-Key": api_key,
            "Content-Type": "application/json",
        }
        payload = {"enabled": enabled}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        _LOGGER.debug(
                            f"Successfully set SSID {self.ssid['name']} to enabled: {enabled}"
                        )
                        # Refresh data to reflect the change
                        await self.coordinator.async_request_refresh()
                    else:
                        error_text = await response.text()
                        _LOGGER.error(
                            f"Failed to set SSID {self.ssid['name']} to enabled: {enabled}. Status: {response.status}, Response: {error_text}"
                        )
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Error setting SSID enabled state: {e}")

    async def async_update(self) -> None:
        """Update the SSID state."""
        device = next(
            (
                d
                for d in self.coordinator.data["devices"]
                if d["serial"] == self.device["serial"]
            ),
            None,
        )
        if device and "ssids" in device:
            self.ssid = next(
                (s for s in device["ssids"] if s["name"] == self.ssid["name"]),
                self.ssid,
            )
