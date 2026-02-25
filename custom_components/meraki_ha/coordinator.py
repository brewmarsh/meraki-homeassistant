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
from .core.api.client import MerakiAPIClient as ApiClient
from .core.coordinator_helpers.config_helper import (
    CoordinatorConfig,
    get_coordinator_config,
)
from .core.coordinator_helpers.data_fetcher import DataFetchManager
from .core.coordinator_helpers.update_processor import UpdateProcessor
from .core.managers import PendingUpdateManager, PollingManager

if TYPE_CHECKING:
    from .core.models.device import MerakiDevice
    from .core.models.network import MerakiNetwork
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
    config: CoordinatorConfig

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
        # Accept Beta/Refactor: Standardized Encapsulated config logic
        self.config = get_coordinator_config(entry)
        
        self.api = ApiClient(
            hass=hass,
            api_key=self.config.api_key,
            org_id=self.config.org_id,
        )

        self.data_fetch_manager = DataFetchManager(
            client=self.api,
            enable_vpn_management=self.config.enable_vpn,
            enable_firewall_rules=self.config.enable_firewall,
            enable_traffic_shaping=self.config.enable_traffic,
            enable_camera_sense=self.config.enable_camera_sense,
        )
        
        self.devices_by_serial: dict[str, MerakiDevice] = {}
        self.networks_by_id: dict[str, MerakiNetwork] = {}
        self.ssids_by_network_and_number: dict[tuple[str, int], dict[str, Any]] = {}
        self.last_successful_update: datetime | None = None
        self.last_successful_data: dict[str, Any] = {}

        self.pending_update_manager = PendingUpdateManager()
        self.polling_manager = PollingManager(self.config.update_interval)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=self.config.update_interval,
        )
        self.config_entry = entry

        # Accept Beta/Refactor: UpdateProcessor replaces MerakiDataProcessor
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

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint, apply filters, and handle exceptions."""
        try:
            return await self._execute_update_cycle()
        except Exception as err:
            return self._handle_update_failure(err)

    async def _execute_update_cycle(self) -> dict[str, Any]:
        """Execute the update cycle and process data."""
        timespan = self._get_update_timespan()
        data = await self._fetch_data_from_api(timespan)

        if not data:
            _LOGGER.warning("API call to get_all_data returned no data.")
            return self.last_successful_data

        await self._process_successful_update(data)
        return data

    def _get_update_timespan(self) -> int:
        """Get the update timespan in seconds."""
        if not self.update_interval:
            return 300
        return int(self.update_interval.total_seconds())

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

    async def _process_successful_update(self, data: dict[str, Any]) -> None:
        """Process successful data update via the specialized UpdateProcessor."""
        # Accept Beta/Refactor: Delegated async logic reduces coordinator complexity
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

    def _handle_update_failure(self, err: Exception) -> dict[str, Any]:
        """Handle update failure via PollingManager."""
        self._record_and_adjust_polling(err)
        self._log_update_status(err)

        if not self.last_successful_data:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

        return self.last_successful_data

    def _record_and_adjust_polling(self, err: Exception) -> None:
        """Record the failure and adjust poll interval if necessary."""
        if not self.polling_manager.record_failure(err):
            return

        if self.update_interval == self.polling_manager.update_interval:
            return

        _LOGGER.warning(
            "Increasing poll interval to %s due to failures.",
            self.polling_manager.update_interval,
        )
        self.update_interval = self.polling_manager.update_interval

    def _log_update_status(self, err: Exception) -> None:
        """Log update status and failure details."""
        _LOGGER.debug(
            "Coordinator update success rate (last 5): %.1f%%",
            self.polling_manager.get_success_rate(),
        )
        _LOGGER.warning(
            "Failed to fetch new data, using stale data. Error: %s",
            err,
        )

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

    def add_status_message(self, serial: str, message: str) -> None:
        """Add a status message for a device."""
        device = self.get_device(serial)
        if device:
            if message not in device.status_messages:
                device.status_messages.append(message)

    def add_network_status_message(self, network_id: str, message: str) -> None:
        """Add a status message for a network."""
        network = self.get_network(network_id)
        if network:
            if message not in network.status_messages:
                network.status_messages.append(message)

    async def async_setup_services(
        self,
        device_control_service: DeviceControlService,
        switch_port_service: SwitchPortService,
        camera_service: CameraService,
    ) -> None:
        """Set up the services for the Meraki integration."""
        from .core.coordinator_helpers.service_setup import async_setup_services

        await async_setup_services(
            self.hass,
            device_control_service,
            switch_port_service,
            camera_service,
        )