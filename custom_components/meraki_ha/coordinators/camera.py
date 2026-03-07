"""Specialized coordinator for Meraki camera data."""

from __future__ import annotations

import logging
from typing import Any

from .base import MerakiBaseCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiCameraCoordinator(MerakiBaseCoordinator[dict[str, Any]]):
    """A coordinator for Meraki camera data."""

    def __init__(self, hass, entry, api_client) -> None:
        """Initialize the camera coordinator."""
        super().__init__(hass, entry, api_client, name="camera")
        self.last_successful_data: dict[str, Any] = {}
        # Slow poll interval
        from datetime import timedelta
        self.update_interval = timedelta(seconds=600)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch camera data."""
        try:
            timespan = int(self.update_interval.total_seconds()) if self.update_interval else 600
            data = await self.data_fetch_manager.get_sensor_data(
                self.last_successful_data, timespan=timespan
            )
            if data:
                (
                    self.devices_by_serial,
                    self.networks_by_id,
                    self.ssids_by_network_and_number,
                    _,
                ) = await self.update_processor.process_success(data, self.data)
                self.last_successful_data = data

            # Return a merged dictionary keyed by serial/ID for efficient extraction
            return {**self.devices_by_serial, **self.networks_by_id}
        except Exception as err:
            # Fallback to last successful data if update fails
            self.update_processor.process_failure(
                err, self.last_successful_data
            )
            return {**self.devices_by_serial, **self.networks_by_id}
