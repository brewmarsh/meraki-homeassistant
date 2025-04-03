"""Device Tag Fetcher for the meraki_ha integration."""

import logging
from typing import List

from .api_data_fetcher import (
    MerakiApiDataFetcher,
    MerakiApiConnectionError,
    MerakiApiInvalidApiKeyError,
)

_LOGGER = logging.getLogger(__name__)


class DeviceTagFetcher:
    """Class to fetch tags for Meraki devices."""

    def __init__(self, api_fetcher: MerakiApiDataFetcher):
        """Initialize the DeviceTagFetcher."""
        self.api_fetcher = api_fetcher

    async def get_device_tags(self, serial: str) -> List[str]:
        """Fetch tags for a single device."""
        try:
            tags = await self.api_fetcher.async_get_device_tags(serial)
            return tags if tags else []
        except MerakiApiConnectionError as e:
            _LOGGER.error(f"Connection error fetching tags for device {serial}: {e}")
            return []
        except MerakiApiInvalidApiKeyError as e:
            _LOGGER.error(f"Invalid API key fetching tags for device {serial}: {e}")
            return []
        except Exception as e:
            _LOGGER.error(f"Error fetching tags for device {serial}: {e}")
            return []
