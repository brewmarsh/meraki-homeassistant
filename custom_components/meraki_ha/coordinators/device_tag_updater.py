"""Device Tag Updater for the meraki_ha integration."""

import logging
from typing import List

from .api_data_fetcher import (
    MerakiApiDataFetcher,
    MerakiApiConnectionError,
    MerakiApiInvalidApiKeyError,
)
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import UpdateFailed

_LOGGER = logging.getLogger(__name__)


class DeviceTagUpdater:
    """Class to update tags for Meraki devices."""

    def __init__(self, api_fetcher: MerakiApiDataFetcher):
        """Initialize the DeviceTagUpdater."""
        self.api_fetcher = api_fetcher

    async def update_device_tags(self, serial: str, tags: List[str]) -> None:
        """Update tags for a single device."""
        try:
            await self.api_fetcher.async_update_device_tags(serial, tags)
            _LOGGER.info(f"Tags updated for device: {serial} with tags: {tags}")
        except MerakiApiConnectionError as e:
            _LOGGER.error(f"Connection error updating tags: {e}")
            raise UpdateFailed(f"Failed to connect to Meraki API: {e}")
        except MerakiApiInvalidApiKeyError as e:
            _LOGGER.error(f"Invalid API key updating tags: {e}")
            raise ConfigEntryAuthFailed(f"Invalid Meraki API key: {e}")
        except Exception as e:
            _LOGGER.error(f"Error updating tags for device {serial}: {e}")
            raise UpdateFailed(f"Error updating tags for device {serial}: {e}")
