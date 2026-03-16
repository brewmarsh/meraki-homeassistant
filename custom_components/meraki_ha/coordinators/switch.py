"""Specialized coordinator for Meraki switch data."""

from __future__ import annotations

import logging
from typing import Any

from .base import MerakiBaseCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiSwitchCoordinator(MerakiBaseCoordinator[dict[str, Any]]):
    """A coordinator for Meraki switch data."""

    def __init__(self, hass, entry, api_client) -> None:
        """Initialize the switch coordinator."""
        super().__init__(hass, entry, api_client, name="switch")
        self.last_successful_data: dict[str, Any] = {}
        # Slow poll interval
        from datetime import timedelta

        self.update_interval = timedelta(seconds=600)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch switch data."""
        try:
            timespan = (
                int(self.update_interval.total_seconds())
                if self.update_interval
                else 600
            )
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
            return data
        except Exception as err:
            data, _ = self.update_processor.process_failure(
                err, self.last_successful_data
            )
            return data
