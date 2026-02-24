"""Data update coordinator for the Meraki HA integration."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .const_conf import (
    CONF_ENABLE_CAMERA_SENSE,
    CONF_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_TRAFFIC_SHAPING,
    CONF_ENABLE_VPN_MANAGEMENT,
    CONF_IGNORED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_ENABLE_CAMERA_SENSE,
    DEFAULT_ENABLE_FIREWALL_RULES,
    DEFAULT_ENABLE_TRAFFIC_SHAPING,
    DEFAULT_ENABLE_VPN_MANAGEMENT,
    DEFAULT_IGNORED_NETWORKS,
    DEFAULT_SCAN_INTERVAL,
)
from .core.api.client import MerakiAPIClient as ApiClient
from .core.coordinator_helpers.data_fetcher import DataFetchManager
from .core.helpers import filter_ignored_networks, process_coordinator_data
from .core.helpers.device_registry import (
    async_ensure_network_devices_exist,
    async_ensure_ssid_devices_exist,
)
from .core.managers import PendingUpdateManager, PollingManager
from .core.models.device import MerakiDevice
from .core.models.network import MerakiNetwork

if TYPE_CHECKING:
    from custom_components.meraki_ha.services.camera_service import CameraService
    from custom_components.meraki_ha.services.device_control_service import (
        DeviceControlService,
    )
    from custom_components.meraki_ha.services.switch_port_service import (
        SwitchPortService,
    )

_LOGGER = logging.getLogger(__name__)


class MerakiDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """A centralized coordinator for Meraki API data."""

    config_entry: ConfigEntry
    update_interval: timedelta | None

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
        )
        # Feature flags can be in either options (user-controlled)
        # or data (initial setup)
        enable_vpn = entry.options.get(
            CONF_ENABLE_VPN_MANAGEMENT,
            entry.data.get(CONF_ENABLE_VPN_MANAGEMENT, DEFAULT_ENABLE_VPN_MANAGEMENT),
        )
        enable_firewall = entry.options.get(
            CONF_ENABLE_FIREWALL_RULES,
            entry.data.get(CONF_ENABLE_FIREWALL_RULES, DEFAULT_ENABLE_FIREWALL_RULES),
        )
        enable_traffic = entry.options.get(
            CONF_ENABLE_TRAFFIC_SHAPING,
            entry.data.get(CONF_ENABLE_TRAFFIC_SHAPING, DEFAULT_ENABLE_TRAFFIC_SHAPING),
        )
        enable_camera_sense = entry.options.get(
            CONF_ENABLE_CAMERA_SENSE,
            entry.data.get(CONF_ENABLE_CAMERA_SENSE, DEFAULT_ENABLE_CAMERA_SENSE),
        )

        self.data_fetch_manager = DataFetchManager(
            client=self.api,
            enable_vpn_management=enable_vpn,
            enable_firewall_rules=enable_firewall,
            enable_traffic_shaping=enable_traffic,
            enable_camera_sense=enable_camera_sense,
        )
        self.devices_by_serial: dict[str, MerakiDevice] = {}
        self.networks_by_id: dict[str, MerakiNetwork] = {}
        self.ssids_by_network_and_number: dict[tuple[str, int], dict[str, Any]] = {}
        self.last_successful_update: datetime | None = None
        self.last_successful_data: dict[str, Any] = {}

        self.pending_update_manager = PendingUpdateManager()

        try:
            scan_interval = int(
                entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            )
            if scan_interval <= 0:
                scan_interval = DEFAULT_SCAN_INTERVAL
        except (ValueError, TypeError):
            scan_interval = DEFAULT_SCAN_INTERVAL

        default_interval = timedelta(seconds=scan_interval)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=default_interval,
        )
        self.config_entry = entry

        self.polling_manager = PollingManager(default_interval)

    def register_pending_update(
        self,
        unique_id: str | None,
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
        self.pending_update_manager.register(unique_id, expiry_seconds)

    def is_pending(self, unique_id: str | None) -> bool:
        """
        Check if an entity is in a pending (cooldown) state.

        Args:
        ----
            unique_id: The unique ID of the entity.

        Returns
        -------
            True if the entity is in a pending state, False otherwise.

        """
        return self.pending_update_manager.is_pending(unique_id)

    def cancel_pending_update(self, unique_id: str | None) -> None:
        """
        Cancel a pending update for a device.

        Args:
        ----
            unique_id: The unique ID of the entity.

        """
        self.pending_update_manager.cancel(unique_id)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint, apply filters, and handle exceptions."""
        try:
            timespan = (
                int(self.update_interval.total_seconds())
                if self.update_interval
                else 300
            )

            data = await self._fetch_data_from_api(timespan)

            if not data:
                _LOGGER.warning("API call to get_all_data returned no data.")
                return self.last_successful_data

            self._process_successful_update(data)
            return data

        except Exception as err:
            return self._handle_update_failure(err)

    async def _fetch_data_from_api(self, timespan: int) -> dict[str, Any]:
        """Fetch data from the API with a timeout."""
        try:
            async with asyncio.timeout(30):  # HA default setup limit
                return await self.data_fetch_manager.get_all_data(
                    self.last_successful_data, timespan=timespan
                )
        except TimeoutError:
            _LOGGER.error("Meraki API took too long; check for semaphore deadlock")
            raise UpdateFailed("API Timeout") from None

    def _process_successful_update(self, data: dict[str, Any]) -> None:
        """Process successful data update."""
        # --- CRITICAL FIX FROM BETA BRANCH ---
        # Ensure network devices exist in the registry before processing
        async_ensure_network_devices_exist(
            self.hass, self.config_entry, data.get("networks", [])
        )

        # Ensure SSID devices exist
        if "ssids" in data:
            async_ensure_ssid_devices_exist(
                self.hass, self.config_entry, data["ssids"]
            )

        # --- LOGIC FROM REFACTOR BRANCH ---
        # Update success history and consecutive successes via PollingManager
        if self.polling_manager.record_success():
            # If True, the interval was reset after recovery
            if self.update_interval != self.polling_manager.update_interval:
                _LOGGER.info(
                    "Meraki API recovered. Resetting update interval to %s",
                    self.polling_manager.update_interval,
                )
                self.update_interval = self.polling_manager.update_interval

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

        if self.data:
            for key, value in self.data.items():
                if isinstance(value, str):
                    self.data[key] = value.strip()

        (
            self.devices_by_serial,
            self.networks_by_id,
            self.ssids_by_network_and_number,
        ) = process_coordinator_data(self.hass, self.config_entry, data)

        self.last_successful_update = datetime.now()
        self.last_successful_data = data

    def _handle_update_failure(self, err: Exception) -> dict[str, Any]:
        """Handle update failure."""
        # Update success history and reset consecutive successes
        if self.polling_manager.record_failure(err):
            # If True, the interval was increased
            if self.update_interval != self.polling_manager.update_interval:
                _LOGGER.warning(
                    "Increasing poll interval to %s due to failures.",
                    self.polling_manager.update_interval,
                )
                self.update_interval = self.polling_manager.update_interval

        # Log success rate for monitoring
        _LOGGER.debug(
            "Coordinator update success rate (last 5): %.1f%%",
            self.polling_manager.get_success_rate(),
        )

        _LOGGER.warning(
            "Failed to fetch new data, using stale data. Error: %s",
            err,
        )
        # Return the last successful data to maintain entity state
        if self.last_successful_data:
            return self.last_successful_data

        # If there's no last successful data, re-raise the exception
        _LOGGER.error(
            "Unexpected error fetching Meraki data for the first time: %s",
            err,
            exc_info=True,
        )
        raise UpdateFailed(f"Error communicating with API: {err}") from err

    def get_device(self, serial: str | None) -> MerakiDevice | None:
        """
        Get device data by serial number.

        Args:
        ----
            serial: The serial number of the device.

        Returns
        -------
            The device data or None if not found.

        """
        if not serial:
            return None
        return self.devices_by_serial.get(serial)

    def get_network(self, network_id: str) -> MerakiNetwork | None:
        """
        Get network data by ID.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            The network data or None if not found.

        """
        return self.networks_by_id.get(network_id)

    def get_ssid(self, network_id: str, ssid_number: int) -> dict[str, Any] | None:
        """
        Get SSID data by network ID and SSID number.

        Args:
        ----
            network_id: The ID of the network.
            ssid_number: The number of the SSID.

        Returns
        -------
            The SSID data or None if not found.

        """
        return self.ssids_by_network_and_number.get((network_id, ssid_number))

    def add_status_message(self, serial: str, message: str) -> None:
        """
        Add a status message for a device.

        Args:
        ----
            serial: The serial number of the device.
            message: The message to add.

        """
        device = self.get_device(serial)
        if device:
            # Avoid duplicate messages
            if message not in device.status_messages:
                device.status_messages.append(message)

    def add_network_status_message(self, network_id: str, message: str) -> None:
        """
        Add a status message for a network.

        Args:
        ----
            network_id: The ID of the network.
            message: The message to add.

        """
        network = self.get_network(network_id)
        if network:
            # Avoid duplicate messages
            if message not in network.status_messages:
                network.status_messages.append(message)

    async def async_setup_services(
        self,
        device_control_service: DeviceControlService,
        switch_port_service: SwitchPortService,
        camera_service: CameraService,
    ) -> None:
        """
        Set up the services for the Meraki integration.

        Args:
        ----
            device_control_service: The device control service.
            switch_port_service: The switch port service.
            camera_service: The camera service.

        """
        from .core.coordinator_helpers.service_setup import async_setup_services

        await async_setup_services(
            self.hass,
            device_control_service,
            switch_port_service,
            camera_service,
        )
