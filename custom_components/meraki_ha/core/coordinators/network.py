"""Network coordinator for the Meraki integration."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ...async_logging import async_log_time
from ...helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from ..api.client import MerakiAPIClient

_LOGGER = MerakiLoggers.COORDINATOR


class MerakiNetworkCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for Meraki network data."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        update_interval: int = 300,
    ) -> None:
        """Initialize the network coordinator."""
        self.api_client = api_client
        self.config_entry = config_entry

        super().__init__(
            hass,
            _LOGGER,
            name="meraki_network_coordinator",
            update_interval=timedelta(seconds=update_interval),
        )

    @async_log_time(MerakiLoggers.COORDINATOR, slow_threshold=5.0)
    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch network data from the API."""
        try:
            networks = await self.api_client.organization.get_organization_networks()
            return {"networks": networks}
        except Exception as err:
            raise UpdateFailed(f"Error fetching network data: {err}") from err
