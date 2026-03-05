"""Device coordinator for the Meraki HA integration."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.helpers.update_coordinator import UpdateFailed

from .base import MerakiBaseCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceCoordinator(MerakiBaseCoordinator[dict[str, Any]]):
    """A coordinator for fast-poll Meraki device status data."""

    def __init__(self, hass, entry) -> None:
        """Initialize the device coordinator."""
        super().__init__(hass, entry, name="device")
        self.last_successful_data: dict[str, Any] = {}
        # Fast poll interval
        self.update_interval = timedelta(seconds=60)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch fast-poll device data."""
        try:
            data = await self.data_fetch_manager.get_device_data(self.last_successful_data)

            if data:
                # Process success to update internal state (ssids, devices, networks)
                (
                    self.devices_by_serial,
                    self.networks_by_id,
                    self.ssids_by_network_and_number,
                    _,
                ) = await self.update_processor.process_success(data, self.data)
                self.last_successful_data = data

            # Record success and potentially reset interval
            updated = self.polling_manager.record_success()
            self.apply_polling_update(updated)

            return data
        except Exception as err:
            _LOGGER.error("Error fetching Meraki device data: %s", err)

            # Record failure and potentially back off
            updated = self.polling_manager.record_failure(err)
            self.apply_polling_update(updated)

            if "429" in str(err):
                raise UpdateFailed(f"Meraki API rate limit: {err}") from err

            data, _ = self.update_processor.process_failure(err, self.last_successful_data)
            return data
