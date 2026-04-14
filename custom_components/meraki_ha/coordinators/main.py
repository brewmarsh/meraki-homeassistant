"""Main coordinator for the Meraki HA integration."""

from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import UpdateFailed

from .base import MerakiBaseCoordinator

if TYPE_CHECKING:
    pass

_LOGGER = logging.getLogger(__name__)


class MerakiMainCoordinator(MerakiBaseCoordinator[dict[str, Any]]):
    """A centralized coordinator for main Meraki organization and network data."""

    def __init__(
        self,
        hass,
        entry,
        api_client,
        static_data: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the main coordinator."""
        super().__init__(
            hass,
            entry,
            api_client,
            name="main",
            static_data=static_data,
        )
        self.last_successful_update: datetime | None = None
        self.last_successful_data: dict[str, Any] = {}
        
        # Tiered polling state
        self._last_slow_poll: float = 0
        self._slow_poll_interval: int = 600  # 10 minutes
        
        # Fast poll interval (30s)
        self.update_interval = timedelta(seconds=30)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint, apply filters, and handle exceptions."""
        try:
            data = await self._execute_update_cycle()

            # Record success and potentially reset interval
            updated = self.polling_manager.record_success()
            # In tiered mode, we maintain our own fast poll interval
            # unless the polling manager forces a specific backoff
            if updated and self.polling_manager.update_interval:
                 if self.polling_manager.update_interval > self.update_interval:
                      self.apply_polling_update(updated)

            return data
        except Exception as err:
            _LOGGER.error("Error fetching Meraki main data: %s", err)

            # Record failure and potentially back off
            updated = self.polling_manager.record_failure(err)
            self.apply_polling_update(updated)

            if "429" in str(err):
                raise UpdateFailed(f"Meraki API rate limit: {err}") from err

            data, _ = self.update_processor.process_failure(
                err, self.last_successful_data
            )
            return data

    async def _execute_update_cycle(self) -> dict[str, Any]:
        """Execute the tiered update cycle."""
        now = time.time()
        
        # Determine if we should do a full slow poll
        is_slow_poll = (now - self._last_slow_poll) >= self._slow_poll_interval
        
        if is_slow_poll:
            _LOGGER.debug("Executing Meraki slow poll (full refresh)")
            data = await self.data_fetch_manager.get_sensor_data(
                self.last_successful_data, 
                timespan=self._slow_poll_interval
            )
            self._last_slow_poll = now
        else:
            _LOGGER.debug("Executing Meraki fast poll (status only)")
            data = await self.data_fetch_manager.get_device_data(
                self.last_successful_data
            )

        if not data:
            _LOGGER.warning("API call returned no data.")
            return self.last_successful_data

        # Explicitly propagate organization_id to all networks and devices
        from ..core.models.device import MerakiDevice
        from ..core.models.network import MerakiNetwork

        org_id = self.api.organization_id

        if "networks" in data:
            for network in data["networks"]:
                if isinstance(network, MerakiNetwork):
                    network.organization_id = org_id
                elif isinstance(network, dict):
                    network["organizationId"] = org_id

        if "devices" in data:
            for device in data["devices"]:
                if isinstance(device, MerakiDevice):
                    device.organization_id = org_id
                elif isinstance(device, dict):
                    device["organizationId"] = org_id

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
