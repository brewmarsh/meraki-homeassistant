"""DataUpdateCoordinator for the meraki_ha integration."""
import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers import device_registry as dr

from .meraki_api.devices import get_meraki_devices
from .meraki_api.clients import get_clients
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class MerakiCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from Meraki API."""

    def __init__(self, hass: HomeAssistant, api_key: str, org_id: str, scan_interval_timedelta: timedelta) -> None:
        """Initialize the Meraki data coordinator.

        Args:
            hass: Home Assistant instance.
            api_key: Meraki API key.
            org_id: Meraki organization ID.
            scan_interval_timedelta: Time delta for scan interval.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Data",
            update_interval=scan_interval_timedelta,  # use the scan interval.
        )
        self.api_key = api_key
        self.org_id = org_id
        self.scan_interval_timedelta = scan_interval_timedelta  # store the scan interval.
        _LOGGER.debug("MerakiCoordinator initialized")

    async def _async_update_data(self) -> List[Dict[str, Any]]:
        """Fetch data from Meraki API endpoint.

        Returns:
            A list of dictionaries representing Meraki devices with client data.

        Raises:
            UpdateFailed: If there's an error communicating with the Meraki API.
        """
        _LOGGER.debug("Starting Meraki data update")
        try:
            _LOGGER.debug("Calling get_meraki_devices")
            devices: List[Dict[str, Any]] = await get_meraki_devices(self.api_key, self.org_id)
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
                        clients: List[Dict[str, Any]] = await get_clients(self.api_key, device["networkId"], device["serial"])
                        _LOGGER.debug(f"get_clients returned: {clients}")
                        device["connected_clients"] = clients
                    except Exception as client_err:
                        _LOGGER.warning(f"Failed to fetch clients for {device['serial']}: {client_err}")
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
        except Exception as err:
            _LOGGER.error(f"Error communicating with API: {err}")
            raise UpdateFailed(f"Error communicating with API: {err}")