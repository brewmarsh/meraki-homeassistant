"""Base coordinator for the Meraki HA integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, Generic, TypeVar

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..core.api import MerakiApiClientProtocol as ApiClient
from ..core.coordinator_helpers.config_helper import (
    CoordinatorConfig,
    get_coordinator_config,
)
from ..core.coordinator_helpers.data_fetcher import DataFetchManager
from ..core.coordinator_helpers.update_processor import UpdateProcessor
from ..core.managers import PendingUpdateManager, PollingManager
from ..core.models import MerakiDevice, MerakiNetwork

T = TypeVar("T")

_LOGGER = logging.getLogger(__name__)


class MerakiBaseCoordinator(DataUpdateCoordinator[T], Generic[T]):
    """Base coordinator for Meraki API data."""

    config_entry: ConfigEntry
    update_interval: timedelta | None
    config: CoordinatorConfig
    devices_by_serial: dict[str, MerakiDevice]
    networks_by_id: dict[str, MerakiNetwork]
    ssids_by_network_and_number: dict[tuple[str, int], dict[str, Any]]

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        api_client: ApiClient,
        name: str = DOMAIN,
    ) -> None:
        """Initialize the base coordinator."""
        self.config = get_coordinator_config(entry)

        self.api = api_client

        self.data_fetch_manager = DataFetchManager(
            client=self.api,
            enable_vpn_management=self.config.enable_vpn,
            enable_firewall_rules=self.config.enable_firewall,
            enable_traffic_shaping=self.config.enable_traffic,
            enable_camera_sense=self.config.enable_camera_sense,
        )

        self.pending_update_manager = PendingUpdateManager()
        self.polling_manager = PollingManager(self.config.update_interval)

        self.devices_by_serial = {}
        self.networks_by_id = {}
        self.ssids_by_network_and_number = {}

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{name}",
            update_interval=self.config.update_interval,
        )
        self.config_entry = entry

        self.update_processor = UpdateProcessor(
            hass=hass,
            config_entry=entry,
            polling_manager=self.polling_manager,
            config=self.config,
        )

    def register_pending_update(
        self,
        unique_id: str | None,
        expiry_seconds: int = 150,
    ) -> None:
        """Register a pending update to ignore coordinator data."""
        self.pending_update_manager.register(unique_id, expiry_seconds)

    def is_pending(self, unique_id: str | None) -> bool:
        """Check if an entity is in a pending (cooldown) state."""
        return self.pending_update_manager.is_pending(unique_id)

    def cancel_pending_update(self, unique_id: str | None) -> None:
        """Cancel a pending update for a device."""
        self.pending_update_manager.cancel(unique_id)

    def get_device(self, serial: str | None) -> MerakiDevice | None:
        """Get device data by serial number."""
        if not serial:
            return None
        return self.devices_by_serial.get(serial)

    def get_network(self, network_id: str) -> MerakiNetwork | None:
        """Get network data by ID."""
        return self.networks_by_id.get(network_id)

    def get_ssid(self, network_id: str, ssid_number: int) -> dict[str, Any] | None:
        """Get SSID data by network ID and SSID number."""
        return self.ssids_by_network_and_number.get((network_id, ssid_number))

    def apply_polling_update(self, updated: bool) -> None:
        """Update the coordinator's update interval if the manager changed it."""
        if updated:
            self.update_interval = self.polling_manager.update_interval
            _LOGGER.debug(
                "Coordinator %s update interval changed to %s",
                self.name,
                self.update_interval,
            )
