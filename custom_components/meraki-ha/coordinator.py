"""DataUpdateCoordinator for the meraki_ha integration."""

import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .meraki_api.devices import get_meraki_devices, get_meraki_device_clients
import aiohttp
from .meraki_api.networks import get_meraki_networks

_LOGGER = logging.getLogger(__name__)


async def async_create_meraki_network_devices(
    hass: HomeAssistant, api_key: str, config_entry_id: str, org_id: str
):
    """Create Home Assistant device records for Meraki networks."""
    networks = await get_meraki_networks(api_key, org_id)  # org_id added

    if networks is None:
        _LOGGER.warning("Failed to retrieve Meraki networks.")
        return  # Handle the error, log it, etc.

    device_registry = dr.async_get(hass)

    for network in networks:
        network_id = network["id"]
        network_name = network["name"]

        device_registry.async_get_or_create(
            config_entry_id=config_entry_id,  # Use the config entry ID.
            identifiers={(DOMAIN, network_id)},
            manufacturer="Cisco Meraki",
            name=network_name,
            model="Network",
        )
        _LOGGER.debug(f"Created Meraki Network Device: {network_name} ({network_id})")


class MerakiCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from Meraki API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        scan_interval_timedelta: timedelta,
        config_entry,  # Add config_entry to the constructor.
    ) -> None:
        """Initialize the Meraki data coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data",
            update_interval=scan_interval_timedelta,
        )
        self.api_key = api_key
        self.org_id = org_id
        self.scan_interval_timedelta = scan_interval_timedelta
        self.session = None
        self.config_entry = config_entry  # Store config_entry
        self.domain = DOMAIN  # Added this line
        _LOGGER.debug("MerakiCoordinator initialized")

    async def _async_update_data(self) -> List[Dict[str, Any]]:
        """Fetch data from Meraki API endpoint."""
        _LOGGER.debug("Starting Meraki data update")
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        try:
            _LOGGER.debug("Calling get_meraki_devices")
            devices: List[Dict[str, Any]] = await get_meraki_devices(
                self.session, self.api_key, self.org_id
            )
            _LOGGER.debug(f"get_meraki_devices returned: {devices}")
            if devices is None:
                raise UpdateFailed("Error communicating with Meraki API")

            device_registry = dr.async_get(self.hass)

            for device in devices:
                model: str = device["model"].strip()
                _LOGGER.debug(f"Raw Model: {repr(model)}")
                if model.startswith("MR") or model.startswith("GR"):
                    _LOGGER.debug(f"Fetching clients for {device['serial']}")
                    try:
                        _LOGGER.debug(f"Calling get_clients for {device['serial']}")
                        clients: List[Dict[str, Any]] = await get_meraki_device_clients(
                            self.session,
                            self.api_key,
                            device["networkId"],
                            device["serial"],
                        )
                        _LOGGER.debug(f"get_clients returned: {clients}")
                        device["connected_clients"] = clients
                    except Exception as client_error:
                        _LOGGER.warning(
                            f"Failed to fetch clients for {device['serial']}: {client_error}"
                        )
                        device["connected_clients"] = []
                else:
                    device["connected_clients"] = []

                # Device creation logic
                _LOGGER.debug(f"Creating/Updating device: {device['serial']}")

                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, device["serial"])},
                    manufacturer="Cisco Meraki",
                    model=device["model"],
                    name=device["name"],
                    sw_version=device.get("firmware"),
                )
                _LOGGER.debug(f"Device {device['serial']} created/updated")

            _LOGGER.debug(f"Meraki data update completed: {devices}")
            return devices
        except Exception as error:
            _LOGGER.error(f"Error communicating with API: {error}")
            raise UpdateFailed(f"Error communicating with API: {error}")

    async def async_close_session(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def _async_shutdown(self, event):
        """Close the aiohttp session on shutdown."""
        await self.async_close_session()

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first refresh of a config entry."""
        await super().async_config_entry_first_refresh()
        self.hass.bus.async_listen_once("homeassistant_stop", self._async_shutdown)

    async def async_create_network_devices(self):  # Function call from init.py
        """Create Meraki Network Devices"""
        await async_create_meraki_network_devices(
            self.hass, self.api_key, self.config_entry.entry_id, self.org_id
        )  # org_id added here.
