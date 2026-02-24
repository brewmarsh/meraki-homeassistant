"""Update processor for the Meraki HA integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ..data_processor import MerakiDataProcessor
from ..helpers.device_registry import (
    async_ensure_network_devices_exist,
    async_ensure_ssid_devices_exist,
)
from ..managers import PollingManager
from .config_helper import CoordinatorConfig

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
        """Process successful data update."""
        # RESOLVED: Local import breaks the circular dependency with core.helpers
        from ..helpers import filter_ignored_networks

        # Ensure network devices exist in the registry before processing
        async_ensure_network_devices_exist(
            self.hass, self.config_entry, data.get("networks", [])
        )

        # Ensure SSID devices exist
        if "ssids" in data:
            async_ensure_ssid_devices_exist(
                self.hass, self.config_entry, data["ssids"]
            )

        interval_changed = False
        # Update success history and consecutive successes via PollingManager
        if self.polling_manager.record_success():
            # If True, the interval was reset after recovery
            interval_changed = True
            _LOGGER.info(
                "Meraki API recovered. Resetting update interval to %s",
                self.polling_manager.update_interval,
            )

        # Log success rate for monitoring
        _LOGGER.debug(
            "Coordinator update success rate (last 5): %.1f%%",
            self.polling_manager.get_success_rate(),
        )

        # Apply network filters using the config helper
        filter_ignored_networks(data, self.config.ignored_networks)

        # Delegate heavy transformation logic to the specialized data processor
        processed_result = await self.data_processor.async_process(data, current_data)

        return (
            processed_result["devices_by_serial"],
            processed_result["networks_by_id"],
            processed_result["ssids_by_network_and_number"],
            interval_changed,
        )