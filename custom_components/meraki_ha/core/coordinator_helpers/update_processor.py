"""Update processor for the Meraki HA integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ..data_processor import MerakiDataProcessor
from ..managers import PollingManager
from .config_helper import CoordinatorConfig
from ..helpers.device_registry import (
    async_ensure_network_devices_exist,
    async_ensure_ssid_devices_exist,
)

if TYPE_CHECKING:
    from ..models.device import MerakiDevice
    from ..models.network import MerakiNetwork

_LOGGER = logging.getLogger(__name__)


class UpdateProcessor:
    """Process update data for the coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        polling_manager: PollingManager,
        config: CoordinatorConfig,
    ) -> None:
        """Initialize the update processor."""
        self.hass = hass
        self.config_entry = config_entry
        self.polling_manager = polling_manager
        self.config = config
        self.data_processor = MerakiDataProcessor(hass, config_entry)

    async def process_success(
        self,
        data: dict[str, Any],
        current_data: dict[str, Any] | None = None,
    ) -> tuple[
        dict[str, MerakiDevice],
        dict[str, MerakiNetwork],
        dict[tuple[str, int], dict[str, Any]],
        bool,  # interval_changed
    ]:
        """
        Process successful data update.
        
        This method acts as an orchestrator, delegating specific tasks to
        sub-methods to maintain a low Agent Cognitive Load (ACL).
        """
        # 1. Ensure network and SSID devices are in the HA registry
        self._ensure_registries(data)

        # 2. Update polling metrics and check for recovery
        interval_changed = self._handle_interval_recovery()

        # 3. Clean up the current data state
        self._sanitize_current_data(current_data)

        # 4. Transform raw API data into Meraki models
        (
            devices_by_serial,
            networks_by_id,
            ssids_by_network_and_number,
        ) = await self._process_data_result(data)

        return (
            devices_by_serial,
            networks_by_id,
            ssids_by_network_and_number,
            interval_changed,
        )

    def _ensure_registries(self, data: dict[str, Any]) -> None:
        """Ensure network and SSID devices exist in the registry."""
        async_ensure_network_devices_exist(
            self.hass, self.config_entry, data.get("networks", [])
        )
        if "ssids" in data:
            async_ensure_ssid_devices_exist(
                self.hass, self.config_entry, data["ssids"]
            )

    def _handle_interval_recovery(self) -> bool:
        """Handle polling interval recovery logic and return if interval changed."""
        interval_changed = False
        if self.polling_manager.record_success():
            interval_changed = True
            _LOGGER.info(
                "Meraki API recovered. Resetting update interval to %s",
                self.polling_manager.update_interval,
            )

        _LOGGER.debug(
            "Coordinator update success rate (last 5): %.1f%%",
            self.polling_manager.get_success_rate(),
        )
        return interval_changed

    def _sanitize_current_data(self, current_data: dict[str, Any] | None) -> None:
        """Sanitize current data by stripping strings."""
        if current_data:
            for key, value in current_data.items():
                if isinstance(value, str):
                    current_data[key] = value.strip()

    async def _process_data_result(
        self, data: dict[str, Any]
    ) -> tuple[
        dict[str, MerakiDevice],
        dict[str, MerakiNetwork],
        dict[tuple[str, int], dict[str, Any]],
    ]:
        """Filter ignored networks and process data into models."""
        processed_data = await self.data_processor.async_process(data)

        return (
            cast(dict[str, "MerakiDevice"], processed_data["devices_by_serial"]),
            cast(dict[str, "MerakiNetwork"], processed_data["networks_by_id"]),
            cast(dict[tuple[str, int], dict[str, Any]], processed_data["ssids_by_network_and_number"]),
        )
