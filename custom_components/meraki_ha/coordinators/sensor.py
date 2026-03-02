"""Sensor coordinator for the Meraki HA integration."""

from __future__ import annotations

import logging
from typing import Any

from .base import MerakiBaseCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiSensorCoordinator(MerakiBaseCoordinator[dict[str, Any]]):
    """A coordinator for Meraki sensor data."""

    def __init__(self, hass, entry) -> None:
        """Initialize the sensor coordinator."""
        super().__init__(hass, entry, name="sensor")
        self.last_successful_data: dict[str, Any] = {}

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch sensor data."""
        try:
            return await self.data_fetch_manager.get_all_data(self.last_successful_data)
        except Exception as err:
            data, _ = self.update_processor.process_failure(err, self.last_successful_data)
            return data
