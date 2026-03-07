"""Specialized coordinator for Meraki switch data."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from .base import MerakiBaseCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiSwitchCoordinator(MerakiBaseCoordinator[dict[str, Any]]):
    """A coordinator for Meraki switch data."""

    def __init__(self, hass, entry, api_client, data_fetch_manager=None) -> None:
        """Initialize the switch coordinator."""
        super().__init__(
            hass, entry, api_client, name="switch", data_fetch_manager=data_fetch_manager
        )
        self.last_successful_data: dict[str, Any] = {}
        # 10-minute poll interval to balance data freshness with API rate limits
        self.update_interval = timedelta(seconds=600)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch switch data and process into serial-keyed maps."""
        try:
            timespan = int(self.update_interval.total_seconds()) if self.update_interval else 600
            data = await self.data_fetch_manager.get_sensor_data(
                self.last_successful_data, timespan=timespan
            )
            
            if data:
                # process_success populates the internal O(1) identifier maps
                (
                    self.devices_by_serial,
                    self.networks_by_id,
                    self.ssids_by_network_and_number,
                    _,
                ) = await self.update_processor.process_success(data, self.data)
                self.last_successful_data = data

            # Return a merged dictionary keyed by serial/ID for efficient extraction.
            # This directly resolves 'Unavailable' issues by ensuring 
            # entities can find their specific data block via identifier lookups.
            return {
                **self.devices_by_serial,
                **self.networks_by_id,
                "devices": list(self.devices_by_serial.values()),
                "networks": list(self.networks_by_id.values()),
                "ssids": list(self.ssids_by_network_and_number.values()),
            }

        except Exception as err:
            _LOGGER.error("Error fetching Meraki switch coordinator data: %s", err)
            data, _ = self.update_processor.process_failure(
                err, self.last_successful_data
            )
            return data