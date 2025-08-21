"""Data update coordinator for Meraki network content filtering."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ...const import DOMAIN
from ...core.api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class NetworkContentFilteringCoordinator(DataUpdateCoordinator):
    """A coordinator for Meraki content filtering settings for a single network."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: MerakiAPIClient,
        scan_interval: int,
        network_id: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_network_content_filtering_{network_id}",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api_client
        self.network_id = network_id

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch content filtering settings from the API."""
        try:
            cf_data = await self.api.appliance.get_network_appliance_content_filtering(
                network_id=self.network_id
            )
            if cf_data:
                blocked_categories = cf_data.get("blockedUrlCategories", [])
                cf_data["blocked_categories_names"] = [
                    category["name"] for category in blocked_categories if "name" in category
                ]
            return cf_data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def async_update_content_filtering(self, **kwargs: Any) -> None:
        """Update content filtering settings."""
        current_settings = self.data or {}
        updated_settings = {**current_settings, **kwargs}

        await self.api.appliance.update_network_appliance_content_filtering(
            network_id=self.network_id, **updated_settings
        )
        await self.async_refresh()
