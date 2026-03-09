"""Main coordinator for the Meraki HA integration."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import UpdateFailed

from .base import MerakiBaseCoordinator

if TYPE_CHECKING:
    pass

_LOGGER = logging.getLogger(__name__)


class MerakiMainCoordinator(MerakiBaseCoordinator[dict[str, Any]]):
    """A centralized coordinator for main Meraki organization and network data."""

    def __init__(self, hass, entry, api_client) -> None:
        """Initialize the main coordinator."""
        super().__init__(hass, entry, api_client, name="main")
        self.last_successful_update: datetime | None = None
        self.last_successful_data: dict[str, Any] = {}
        # Slow poll interval
        from datetime import timedelta
        self.update_interval = timedelta(seconds=600)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint, apply filters, and handle exceptions."""
        try:
            data = await self._execute_update_cycle()

            # Record success and potentially reset interval
            updated = self.polling_manager.record_success()
            self.apply_polling_update(updated)

            return data
        except Exception as err:
            _LOGGER.error("Error fetching Meraki main data: %s", err)

            # Record failure and potentially back off
            updated = self.polling_manager.record_failure(err)
            self.apply_polling_update(updated)

            if "429" in str(err):
                raise UpdateFailed(f"Meraki API rate limit: {err}") from err

            data, _ = self.update_processor.process_failure(err, self.last_successful_data)
            return data

    async def _execute_update_cycle(self) -> dict[str, Any]:
        """Execute the update cycle and process data."""
        timespan = (
            int(self.update_interval.total_seconds()) if self.update_interval else 300
        )
        data = await self.data_fetch_manager.get_all_data(
            self.last_successful_data, timespan=timespan
        )

        if not data:
            _LOGGER.warning("API call to get_all_data returned no data.")
            return self.last_successful_data

        # Explicitly propagate organization_id to all networks
        from ..core.models.network import MerakiNetwork
        org_id = self.api.organization_id
        if "networks" in data:
            for network in data["networks"]:
                if isinstance(network, MerakiNetwork):
                    network.organization_id = org_id
                elif isinstance(network, dict):
                    network["organizationId"] = org_id

        # Process successful update
        (
            self.devices_by_serial,
            self.networks_by_id,
            self.ssids_by_network_and_number,
            interval_changed,
        ) = await self.update_processor.process_success(data, self.data)

        if interval_changed:
            self.update_interval = self.polling_manager.update_interval

        self.last_successful_update = datetime.now()
        self.last_successful_data = data
        return data
