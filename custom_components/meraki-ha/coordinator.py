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
    hass: HomeAssistant,
    api_key: str,
    config_entry_id: str,
    org_id: str,
    session: aiohttp.ClientSession,  # Added session
):
    """Create Home Assistant device records for Meraki networks."""
    networks = await get_meraki_networks(api_key, org_id, session)  # Passed session

    if not networks or len(networks) == 0:
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
        self.scan_interval_timedelta = scan_interval_timedelta
        self.session = aiohttp.ClientSession()  # Initialize session here
        self.config_entry = config_entry  # Store config_entry
        self.domain = DOMAIN  # Added this line
        _LOGGER.debug("MerakiCoordinator initialized")

    async def _async_update_data(self) -> List[Dict[str, Any]]:
        """Fetch data from Meraki API endpoint."""
        _LOGGER.debug("Starting Meraki data update")
        device_registry = dr.async_get(self.hass)
        try:
            _LOGGER.debug(f"Config Entry options: {self.config_entry.options}")
            api_key = self.config_entry.options.get("meraki_api_key")
            org_id = self.config_entry.options.get("meraki_org_id")
            _LOGGER.debug(f"Org ID from options: {org_id}")
            _LOGGER.debug(f"API Key from options: {api_key}")
            _LOGGER.debug("Calling get_meraki_devices")
            devices: List[Dict[str, Any]] = await get_meraki_devices(
                self.session, api_key, org_id
            )
            _LOGGER.debug(f"get_meraki_devices returned: {devices}")
            if devices is None:
                raise UpdateFailed("Error communicating with Meraki API")
            processed_devices = []
            for device in devices:
                device_data = {}
                for key, value in device.items():
                    if key is not None:
                        device_data[key] = value
                    else:
                        _LOGGER.warning(f"Found None key in device data: {device}")
                processed_devices.append(device_data)

            for device in processed_devices:
                model: str = device["model"].strip()
                _LOGGER.debug(f"Raw Model: {repr(model)}")
                if model.startswith("MR") or model.startswith("GR"):
                    _LOGGER.debug(f"Fetching clients for {device['serial']}")
                    try:
                        _LOGGER.debug(f"Calling get_clients for {device['serial']}")
                        clients: List[Dict[str, Any]] = await get_meraki_device_clients(
                            self.session,
                            api_key,
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

            _LOGGER.debug(f"Meraki data update completed: {processed_devices}")
            return processed_devices
        except aiohttp.ClientError as client_error:
            _LOGGER.error(f"Client error communicating with API: {client_error}")
            raise UpdateFailed(f"Client error communicating with API: {client_error}")
        except UpdateFailed as update_error:
            _LOGGER.error(f"Update failed: {update_error}")
            raise update_error
        except Exception as error:  # Capture the exception in the 'error' variable
            if self.session and not self.session.closed:
                _LOGGER.error(f"Unexpected error: {error}")
                raise UpdateFailed(f"Unexpected error: {error}")

    async def _async_shutdown(self):
        """Close the aiohttp session on shutdown."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first refresh of a config entry."""
        try:
            await super().async_config_entry_first_refresh()
        finally:
            self.hass.bus.async_listen_once("homeassistant_stop", self._async_shutdown)

    async def async_create_network_devices(self):  # Function call from init.py
        """Create Meraki Network Devices"""
        api_key = self.config_entry.options.get("meraki_api_key")
        org_id = self.config_entry.options.get("meraki_org_id")
        await async_create_meraki_network_devices(
            self.hass,
            api_key,
            self.config_entry.entry_id,
            org_id,
            self.session,  # added self.session
        )  # org_id added here.
