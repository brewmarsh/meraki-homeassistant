"""Data update coordinator for Meraki switch port statuses."""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ...core.repository import MerakiRepository
from ...coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class SwitchPortStatusCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """A dedicated coordinator for Meraki switch port statuses."""

    def __init__(
        self,
        hass: HomeAssistant,
        repository: MerakiRepository,
        main_coordinator: MerakiDataUpdateCoordinator,
        config_entry,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Switch Port Status",
            update_interval=timedelta(seconds=60),
        )
        self._repository = repository
        self._main_coordinator = main_coordinator
        self.config_entry = config_entry

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint."""
        if not self._main_coordinator.last_update_success:
            raise UpdateFailed("Main coordinator has not successfully updated yet.")

        devices = self._main_coordinator.data.get("devices", [])
        switches = [
            device for device in devices if device.get("productType") == "switch"
        ]

        if not switches:
            _LOGGER.debug("No switches found in the main coordinator data.")
            return {}

        tasks = {
            switch["serial"]: self._repository.async_get_switch_port_statuses(
                switch["serial"]
            )
            for switch in switches
        }

        results = await asyncio.gather(*tasks.values(), return_exceptions=True)

        port_statuses: dict[str, Any] = {}
        for serial, result in zip(tasks.keys(), results):
            if isinstance(result, Exception):
                _LOGGER.warning(
                    "Failed to fetch port statuses for switch %s: %s", serial, result
                )
            elif result is not None:
                port_statuses[serial] = result

        return port_statuses
