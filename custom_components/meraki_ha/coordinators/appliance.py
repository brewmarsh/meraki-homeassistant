"""Appliance coordinator for the Meraki HA integration."""

from __future__ import annotations

import logging
from typing import Any
from datetime import timedelta

from .base import MerakiBaseCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiApplianceCoordinator(MerakiBaseCoordinator[dict[str, Any]]):
    """A coordinator for Meraki appliance data."""

    def __init__(self, hass, entry, api_client, data_fetch_manager=None) -> None:
        """Initialize the appliance coordinator."""
        super().__init__(
            hass, entry, api_client, name="appliance", data_fetch_manager=data_fetch_manager
        )
        self.last_successful_data: dict[str, Any] = {}
        # Slow poll interval for appliance metrics to respect rate limits
        self.update_interval = timedelta(seconds=600)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch and process appliance data with serial-keyed mapping."""
        try:
            timespan = int(self.update_interval.total_seconds()) if self.update_interval else 600
            data = await self.data_fetch_manager.get_sensor_data(
                self.last_successful_data, timespan=timespan
            )
            
            if data:
                # Update processor populates internal maps (devices_by_serial, etc.)
                (
                    self.devices_by_serial,
                    self.networks_by_id,
                    self.ssids_by_network_and_number,
                    _,
                ) = await self.update_processor.process_success(data, self.data)
                self.last_successful_data = data

            # Return a merged dictionary keyed by serial/ID for efficient extraction by entities.
            # This fulfills the data contract required by MerakiEntity.available.
            return {
                **self.devices_by_serial,
                **self.networks_by_id,
                "devices": list(self.devices_by_serial.values()),
                "networks": list(self.networks_by_id.values()),
                "ssids": list(self.ssids_by_network_and_number.values()),
            }
            
        except Exception as err:
            _LOGGER.debug("Appliance coordinator fetch failed, processing fallback: %s", err)
            data, _ = self.update_processor.process_failure(
                err, self.last_successful_data
            )
            return data