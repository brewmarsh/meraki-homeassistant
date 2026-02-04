"""Data update coordinator for the Meraki HA integration."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_TRAFFIC_SHAPING,
    CONF_ENABLE_VPN_MANAGEMENT,
    CONF_IGNORED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_ENABLE_FIREWALL_RULES,
    DEFAULT_ENABLE_TRAFFIC_SHAPING,
    DEFAULT_ENABLE_VPN_MANAGEMENT,
    DEFAULT_IGNORED_NETWORKS,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .core.api.client import MerakiAPIClient as ApiClient
from .core.coordinator_helpers.data_fetcher import DataFetchManager
from .core.helpers import filter_ignored_networks, process_coordinator_data
from .core.managers import AvailabilityTracker, PendingUpdateManager
from .types import MerakiDevice, MerakiNetwork

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
        self.data_fetch_manager = DataFetchManager(
            client=self.api,
            enable_vpn_management=entry.options.get(
                CONF_ENABLE_VPN_MANAGEMENT, DEFAULT_ENABLE_VPN_MANAGEMENT
            ),
            enable_firewall_rules=entry.options.get(
                CONF_ENABLE_FIREWALL_RULES, DEFAULT_ENABLE_FIREWALL_RULES
            ),
            enable_traffic_shaping=entry.options.get(
                CONF_ENABLE_TRAFFIC_SHAPING, DEFAULT_ENABLE_TRAFFIC_SHAPING
            ),
        )
        self.devices_by_serial: dict[str, MerakiDevice] = {}
        self.networks_by_id: dict[str, MerakiNetwork] = {}
        self.ssids_by_network_and_number: dict[tuple[str, int], dict[str, Any]] = {}
        self.last_successful_update: datetime | None = None
        self.last_successful_data: dict[str, Any] = {}

        self.pending_update_manager = PendingUpdateManager()
        self.availability_tracker = AvailabilityTracker()

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
        self.config_entry = entry

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
            # Pass the last known successful data to the API client
            timespan = (
                int(self.update_interval.total_seconds())
                if self.update_interval
                else 300
            )
            data = await self.data_fetch_manager.get_all_data(
                self.last_successful_data, timespan=timespan
            )

            if not data:
                _LOGGER.warning("API call to get_all_data returned no data.")
                # Return cached data to prevent entities from becoming unavailable
                return self.last_successful_data

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
            return data

        except Exception as err:
            _LOGGER.warning(
                "Failed to fetch new data, using stale data. Error: %s",
                err,
            )
            # Return the last successful data to maintain entity state
            if self.last_successful_data:
                return self.last_successful_data

            # If there's no last successful data, re-raise the exception
            # This will happen on the first run if it fails
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

    def is_vlan_check_due(self, network_id: str) -> bool:
        """
        Determine if a VLAN availability check is due.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            True if the check is due, False otherwise.

        """
        return self.availability_tracker.is_check_due(network_id, "vlan")

    def is_traffic_check_due(self, network_id: str) -> bool:
        """
        Determine if a Traffic Analysis availability check is due.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            True if the check is due, False otherwise.

        """
        return self.availability_tracker.is_check_due(network_id, "traffic")

    def mark_vlan_check_done(self, network_id: str) -> None:
        """
        Mark a VLAN availability check as done for the day.

        Args:
        ----
            network_id: The ID of the network.

        """
        self.availability_tracker.mark_check_done(network_id, "vlan")

    def mark_traffic_check_done(self, network_id: str) -> None:
        """
        Mark a Traffic Analysis availability check as done for the day.

        Args:
        ----
            network_id: The ID of the network.

        """
        self.availability_tracker.mark_check_done(network_id, "traffic")

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
