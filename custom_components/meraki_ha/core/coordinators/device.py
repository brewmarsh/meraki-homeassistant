"""Device coordinator for the Meraki integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from ..api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for Meraki device data."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        update_interval: int = 300,
    ) -> None:
        """Initialize the device coordinator."""
        self.api_client = api_client
        self.config_entry = config_entry

        super().__init__(
            hass,
            _LOGGER,
            name="meraki_device_coordinator",
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch device data from the API."""
        try:
            devices = await self.api_client.devices.get_organization_devices()
            return {"devices": devices}
        except Exception as err:
            raise UpdateFailed(f"Error fetching device data: {err}") from err

