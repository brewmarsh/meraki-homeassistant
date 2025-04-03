"""Base coordinator for the meraki_ha integration."""

import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)


class MerakiBaseCoordinator(DataUpdateCoordinator):
    """Base coordinator to handle Meraki API communication."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        device_name_format: str,  # added device_name_format
    ) -> None:
        """Initialize the Meraki base coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Base Data",
            update_interval=scan_interval,
        )
        self.session = session
        self.api_key = api_key
        self.org_id = org_id
        self.device_name_format = device_name_format  # added device_name_format

    async def _async_update_data(self) -> dict:
        """Base data update logic."""
        try:
            # Basic API checks and error handling can be added here
            # Example API call (replace with your actual base logic):
            headers = {
                "X-Cisco-Meraki-API-Key": self.api_key,
                "Content-Type": "application/json",
            }
            url = f"https://api.meraki.com/api/v1/organizations/{self.org_id}"  # Or some base level API call.
            _LOGGER.debug(f"Making API call to: {url}")  # added log
            async with self.session.get(url, headers=headers) as resp:
                _LOGGER.debug(f"API response status: {resp.status}")  # added log
                if resp.status != 200:
                    raise UpdateFailed(f"API error: {resp.status}")
                response_json = await resp.json()
                _LOGGER.debug(f"API response JSON: {response_json}")  # added log
                return response_json

        except aiohttp.ClientError as e:
            _LOGGER.error(f"API communication error: {e}")
            raise UpdateFailed(f"API communication error: {e}")
        except Exception as e:
            _LOGGER.error(f"Unexpected error during data update: {e}")
            raise UpdateFailed(f"Unexpected error: {e}")
