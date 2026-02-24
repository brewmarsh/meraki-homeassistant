"""Update processor for the Meraki Coordinator."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ...const_conf import CONF_IGNORED_NETWORKS, DEFAULT_IGNORED_NETWORKS
from ..helpers import filter_ignored_networks, process_coordinator_data
from ..helpers.device_registry import (
    async_ensure_network_devices_exist,
    async_ensure_ssid_devices_exist,
)

if TYPE_CHECKING:
    from ..managers import PollingManager
    from ..models.device import MerakiDevice
    from ..models.network import MerakiNetwork

_LOGGER = logging.getLogger(__name__)


class UpdateProcessor:
    """Process successful API updates."""

    def __init__(
        self, hass: HomeAssistant, config_entry: ConfigEntry, polling_manager: PollingManager
    ) -> None:
        """Initialize the update processor."""
        self.hass = hass
        self.config_entry = config_entry
        self.polling_manager = polling_manager

    def process_data(
        self,
        data: dict[str, Any],
        current_data: dict[str, Any] | None,
        update_interval: Any,
    ) -> tuple[
        dict[str, MerakiDevice],
        dict[str, MerakiNetwork],
        dict[tuple[str, int], dict[str, Any]],
        Any,  # Updated update_interval
    ]:
        """Process successful data update."""
        # Ensure network devices exist in the registry before processing
        async_ensure_network_devices_exist(
            self.hass, self.config_entry, data.get("networks", [])
        )

        # Ensure SSID devices exist
        if "ssids" in data:
            async_ensure_ssid_devices_exist(
                self.hass, self.config_entry, data["ssids"]
            )

        # Update success history and consecutive successes via PollingManager
        new_interval = update_interval
        if self.polling_manager.record_success():
            # If True, the interval was reset after recovery
            if update_interval != self.polling_manager.update_interval:
                _LOGGER.info(
                    "Meraki API recovered. Resetting update interval to %s",
                    self.polling_manager.update_interval,
                )
                new_interval = self.polling_manager.update_interval

        # Log success rate for monitoring
        _LOGGER.debug(
            "Coordinator update success rate (last 5): %.1f%%",
            self.polling_manager.get_success_rate(),
        )

        if self.config_entry:
            ignored_network_ids = self.config_entry.options.get(
                CONF_IGNORED_NETWORKS,
                DEFAULT_IGNORED_NETWORKS,
            )
            filter_ignored_networks(data, ignored_network_ids)

        if current_data:
            for key, value in current_data.items():
                if isinstance(value, str):
                    current_data[key] = value.strip()

        (
            devices_by_serial,
            networks_by_id,
            ssids_by_network_and_number,
        ) = process_coordinator_data(self.hass, self.config_entry, data)

        return (
            devices_by_serial,
            networks_by_id,
            ssids_by_network_and_number,
            new_interval,
        )
