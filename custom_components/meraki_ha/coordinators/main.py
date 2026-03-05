"""Main coordinator for the Meraki HA integration."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from .base import MerakiBaseCoordinator

if TYPE_CHECKING:
    pass

_LOGGER = logging.getLogger(__name__)


class MerakiMainCoordinator(MerakiBaseCoordinator[dict[str, Any]]):
    """A centralized coordinator for main Meraki organization and network data."""

    def __init__(self, hass, entry) -> None:
        """Initialize the main coordinator."""
        super().__init__(hass, entry, name="main")
        self.last_successful_update: datetime | None = None
        self.last_successful_data: dict[str, Any] = {}

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint, apply filters, and handle exceptions."""
        try:
            return await self._execute_update_cycle()
        except Exception as err:
            data, interval_changed = self.update_processor.process_failure(
                err, self.last_successful_data
            )
            if interval_changed:
                self.update_interval = self.polling_manager.update_interval
            return data

    async def _execute_update_cycle(self) -> dict[str, Any]:
        """Execute the update cycle and process data."""
        timespan = int(self.update_interval.total_seconds()) if self.update_interval else 300
        data = await self.data_fetch_manager.get_all_data(
            self.last_successful_data, timespan=timespan
        )

        if not data:
            _LOGGER.warning("API call to get_all_data returned no data.")
            return self.last_successful_data

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
