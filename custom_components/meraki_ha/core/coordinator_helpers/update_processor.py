"""Update processor for the Meraki HA integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ..data_processor import MerakiDataProcessor
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
        interval_changed = False
        
        # 1. Update success history and check for recovery via PollingManager
        if self.polling_manager.record_success():
            # If True, the interval was reset after recovery
            interval_changed = True
            _LOGGER.info(
                "Meraki API recovered. Resetting update interval to %s",
                self.polling_manager.update_interval,
            )

        # 2. Log success rate for monitoring
        _LOGGER.debug(
            "Coordinator update success rate (last 5): %.1f%%",
            self.polling_manager.get_success_rate(),
        )

        # 3. Delegate processing to MerakiDataProcessor 
        # (This now handles device_registry checks and network filtering internally)
        processed_result = await self.data_processor.async_process(data, current_data)

        # 4. Unpack result dict to the tuple format expected by the Coordinator
        return (
            processed_result["devices_by_serial"],
            processed_result["networks_by_id"],
            processed_result["ssids_by_network_and_number"],
            interval_changed,
        )