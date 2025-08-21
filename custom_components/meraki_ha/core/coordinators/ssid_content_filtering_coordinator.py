"""Data update coordinator for Meraki SSID content filtering."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ...const import DOMAIN
from ...core.api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class SsidContentFilteringCoordinator(DataUpdateCoordinator):
    """A coordinator for Meraki content filtering settings for a single SSID."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: MerakiAPIClient,
        scan_interval: int,
        network_id: str,
        ssid_number: int,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_ssid_content_filtering_{network_id}_{ssid_number}",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api_client
        self.network_id = network_id
        self.ssid_number = ssid_number

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch SSID data from the API."""
        try:
            return await self.api.wireless.get_network_wireless_ssid(
                network_id=self.network_id, number=self.ssid_number
            )
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def async_update_content_filtering(self, **kwargs: Any) -> None:
        """Update content filtering settings for the SSID."""
        # The Meraki API for updating an SSID takes the full SSID object.
        # We need to get the current settings, update the content filtering part,
        # and then send the whole object back.
        current_ssid_data = self.data or {}

        # The content filtering settings are nested under the 'contentFiltering' key.
        current_content_filtering = current_ssid_data.get("contentFiltering", {})
        updated_content_filtering = {**current_content_filtering, **kwargs}

        updated_ssid_data = {
            "contentFiltering": updated_content_filtering,
        }

        await self.api.wireless.update_network_wireless_ssid(
            network_id=self.network_id,
            number=self.ssid_number,
            **updated_ssid_data,
        )
        await self.async_refresh()
