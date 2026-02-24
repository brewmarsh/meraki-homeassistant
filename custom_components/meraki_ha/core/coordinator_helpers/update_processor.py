"""Update processor for the Meraki HA integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ..helpers import filter_ignored_networks, process_coordinator_data
from ..helpers.device_registry import (
    async_ensure_network_devices_exist,
    async_ensure_ssid_devices_exist,
)
from ..managers import PollingManager
from ..models.device import MerakiDevice
from ..models.network import MerakiNetwork
from .config_helper import CoordinatorConfig

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

    def process_success(
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
        self._ensure_registries(data)
        interval_changed = self._handle_interval_recovery()

        self._sanitize_current_data(current_data)

        (
            devices_by_serial,
            networks_by_id,
            ssids_by_network_and_number,
        ) = self._process_data_result(data)

        return (
            devices_by_serial,
            networks_by_id,
            ssids_by_network_and_number,
            interval_changed,
        )

    def _ensure_registries(self, data: dict[str, Any]) -> None:
        """Ensure network and SSID devices exist in the registry."""
        # Ensure network devices exist in the registry before processing
        async_ensure_network_devices_exist(
            self.hass, self.config_entry, data.get("networks", [])
        )

        # Ensure SSID devices exist
        if "ssids" in data:
            async_ensure_ssid_devices_exist(
                self.hass, self.config_entry, data["ssids"]
            )

    def _handle_interval_recovery(self) -> bool:
        """Handle polling interval recovery logic."""
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
        return interval_changed

    def _sanitize_current_data(self, current_data: dict[str, Any] | None) -> None:
        """Sanitize current data by stripping strings."""
        if current_data:
            for key, value in current_data.items():
                if isinstance(value, str):
                    current_data[key] = value.strip()

    def _process_data_result(
        self, data: dict[str, Any]
    ) -> tuple[
        dict[str, MerakiDevice],
        dict[str, MerakiNetwork],
        dict[tuple[str, int], dict[str, Any]],
    ]:
        """Filter ignored networks and process data into models."""
        # Use the injected config object to filter networks
        filter_ignored_networks(data, self.config.ignored_networks)

        return process_coordinator_data(self.hass, self.config_entry, data)