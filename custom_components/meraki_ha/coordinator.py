"""Data update coordinator for the Meraki HA integration."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_ENABLE_VPN_MANAGEMENT,
    CONF_IGNORED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_ENABLE_VPN_MANAGEMENT,
    DEFAULT_IGNORED_NETWORKS,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .core.api.client import MerakiAPIClient as ApiClient
from .core.helpers import filter_ignored_networks, update_device_registry_info
from .core.managers import AvailabilityTracker
from .types import MerakiDevice, MerakiNetwork

if TYPE_CHECKING:
    from .services.camera_service import CameraService
    from .services.device_control_service import DeviceControlService
    from .services.switch_port_service import SwitchPortService


_LOGGER = logging.getLogger(__name__)


class MerakiDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """A centralized coordinator for Meraki API data."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """
        Initialize the coordinator.

        Args:
        ----
            hass: The Home Assistant instance.
            entry: The config entry.

        """
        self.api = ApiClient(
            hass=hass,
            api_key=entry.data[CONF_MERAKI_API_KEY],
            org_id=entry.data[CONF_MERAKI_ORG_ID],
            coordinator=self,
            enable_vpn_management=entry.options.get(
                CONF_ENABLE_VPN_MANAGEMENT, DEFAULT_ENABLE_VPN_MANAGEMENT
            ),
        )
        self.config_entry = entry
        self.devices_by_serial: dict[str, MerakiDevice] = {}
        self.networks_by_id: dict[str, MerakiNetwork] = {}
        self.ssids_by_network_and_number: dict[tuple[str, int], dict[str, Any]] = {}
        self.last_successful_update: datetime | None = None
        self.last_successful_data: dict[str, Any] = {}
        self._pending_updates: dict[str, datetime] = {}
        self.availability_tracker = AvailabilityTracker()
        self.device_control_service: DeviceControlService | None = None
        self.switch_port_service: SwitchPortService | None = None
        self.camera_service: CameraService | None = None

        try:
            scan_interval = int(
                entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            )
            if scan_interval <= 0:
                scan_interval = DEFAULT_SCAN_INTERVAL
        except (ValueError, TypeError):
            scan_interval = DEFAULT_SCAN_INTERVAL

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    def register_pending_update(
        self,
        unique_id: str,
        expiry_seconds: int = 150,
    ) -> None:
        """
        Register a pending update to ignore coordinator data.

        This prevents overwriting an optimistic state with stale data from the
        Meraki API, which can have a significant provisioning delay.

        Args:
        ----
            unique_id: The unique ID of the entity.
            expiry_seconds: The duration of the cooldown period.

        """
        expiry_time =