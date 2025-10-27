"""Data update coordinator for the Meraki HA integration."""
import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_IGNORED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_IGNORED_NETWORKS,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .core.api.client import MerakiAPIClient as ApiClient
from .types import MerakiDevice, MerakiNetwork

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
        )
        self.config_entry = entry
        self.devices_by_serial: dict[str, MerakiDevice] = {}
        self.networks_by_id: dict[str, MerakiNetwork] = {}
        self.ssids_by_network_and_number: dict[tuple[str, int], dict[str, Any]] = {}
        self.last_successful_update: datetime | None = None
        self.last_successful_data: dict[str, Any] = {}
        self._pending_updates: dict[str, datetime] = {}
        self._vlan_check_timestamps: dict[str, datetime] = {}
        self._traffic_check_timestamps: dict[str, datetime] = {}

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
        expiry_time = datetime.now() + timedelta(seconds=expiry_seconds)
        self._pending_updates[unique_id] = expiry_time
        _LOGGER.debug(
            "Registered pending update for %s, ignoring coordinator updates until %s",
            unique_id,
            expiry_time,
        )

    def is_pending(self, unique_id: str) -> bool:
        """
        Check if an entity is in a pending (cooldown) state.

        Args:
        ----
            unique_id: The unique ID of the entity.

        Returns:
        -------
            True if the entity is in a pending state, False otherwise.

        """
        if unique_id not in self._pending_updates:
            return False

        now = datetime.now()
        expiry_time = self._pending_updates[unique_id]

        if now > expiry_time:
            # Cooldown has expired, remove it from the dictionary
            del self._pending_updates[unique_id]
            _LOGGER.debug("Pending update expired for %s", unique_id)
            return False

        # Cooldown is still active
        _LOGGER.debug("Update for %s is still pending (on cooldown)", unique_id)
        return True

    def _filter_ignored_networks(self, data: dict[str, Any]) -> None:
        """
        Filter out networks that the user has chosen to ignore.

        Args:
        ----
            data: The data dictionary to filter.

        """
        if not self.config_entry or not hasattr(self.config_entry, "options"):
            _LOGGER.debug(
                "Config entry or options not available, "
                "cannot filter ignored networks.",
            )
            return
        ignored_networks_str = self.config_entry.options.get(
            CONF_IGNORED_NETWORKS,
            DEFAULT_IGNORED_NETWORKS,
        )
        if ignored_networks_str and "networks" in data:
            ignored_names = {name.strip() for name in ignored_networks_str.split(",")}
            data["networks"] = [
                n for n in data["networks"] if n.get("name") not in ignored_names
            ]

    def _populate_device_entities(self, data: dict[str, Any]) -> None:
        """
        Populate device data with associated Home Assistant entities.

        Args:
        ----
            data: The data dictionary to populate.

        """
        if not (data and "devices" in data):
            return

        ent_reg = er.async_get(self.hass)
        dev_reg = dr.async_get(self.hass)

        for device in data["devices"]:
            device.setdefault("status_messages", [])
            device["entities"] = []

            ha_device = dev_reg.async_get_device(
                identifiers={(DOMAIN, device["serial"])},
            )
            if ha_device:
                entities_for_device = er.async_entries_for_device(
                    ent_reg,
                    ha_device.id,
                )
                for entity_entry in entities_for_device:
                    state = self.hass.states.get(entity_entry.entity_id)
                    if state:
                        device["entities"].append(
                            {
                                "entity_id": entity_entry.entity_id,
                                "name": state.name,
                                "state": state.state,
                                "attributes": dict(state.attributes),
                            },
                        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint and apply filters."""
        try:
            data = await self.api.get_all_data(self.last_successful_data)
            if not data:
                _LOGGER.warning("API call to get_all_data returned no data.")
                raise UpdateFailed("API call returned no data.")

            self._filter_ignored_networks(data)

            # Create lookup tables for efficient access in entities
            self.devices_by_serial = {
                d["serial"]: d for d in data.get("devices", []) if "serial" in d
            }
            self.networks_by_id = {
                n["id"]: n for n in data.get("networks", []) if "id" in n
            }
            self.ssids_by_network_and_number = {
                (s["networkId"], s["number"]): s
                for s in data.get("ssids", [])
                if "networkId" in s and "number" in s
            }

            self._populate_device_entities(data)

            self.last_successful_update = datetime.now()
            self.last_successful_data = data
            return data
        except Exception as err:
            if self.last_successful_update and (
                datetime.now() - self.last_successful_update
            ) < timedelta(minutes=30):
                _LOGGER.warning(
                    "Failed to fetch new data, using stale data. Error: %s",
                    err,
                )
                return self.data

            _LOGGER.error(
                "Unexpected error fetching Meraki data: %s",
                err,
                exc_info=True,
            )
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    def get_device(self, serial: str) -> MerakiDevice | None:
        """
        Get device data by serial number.

        Args:
        ----
            serial: The serial number of the device.

        Returns:
        -------
            The device data or None if not found.

        """
        return self.devices_by_serial.get(serial)

    def get_network(self, network_id: str) -> MerakiNetwork | None:
        """
        Get network data by ID.

        Args:
        ----
            network_id: The ID of the network.

        Returns:
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

        Returns:
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
        if self.data and self.data.get("devices"):
            for device in self.data["devices"]:
                if device.get("serial") == serial:
                    device.setdefault("status_messages", [])
                    # Avoid duplicate messages
                    if message not in device["status_messages"]:
                        device["status_messages"].append(message)
                    break

    def add_network_status_message(self, network_id: str, message: str) -> None:
        """
        Add a status message for a network.

        Args:
        ----
            network_id: The ID of the network.
            message: The message to add.

        """
        if self.data and self.data.get("networks"):
            for network in self.data["networks"]:
                if network.get("id") == network_id:
                    network.setdefault("status_messages", [])
                    # Avoid duplicate messages
                    if message not in network["status_messages"]:
                        network["status_messages"].append(message)
                    break

    def _is_check_due(
        self,
        check_timestamps: dict[str, datetime],
        network_id: str,
        interval_hours: int = 24,
    ) -> bool:
        """
        Determine if an availability check is due for a network feature.

        Args:
        ----
            check_timestamps: The dictionary of timestamps.
            network_id: The ID of the network.
            interval_hours: The interval in hours.

        Returns:
        -------
            True if the check is due, False otherwise.

        """
        last_check = check_timestamps.get(network_id)
        if not last_check:
            return True
        return (datetime.now() - last_check) > timedelta(hours=interval_hours)

    def is_vlan_check_due(self, network_id: str) -> bool:
        """
        Determine if a VLAN availability check is due.

        Args:
        ----
            network_id: The ID of the network.

        Returns:
        -------
            True if the check is due, False otherwise.

        """
        return self._is_check_due(self._vlan_check_timestamps, network_id)

    def is_traffic_check_due(self, network_id: str) -> bool:
        """
        Determine if a Traffic Analysis availability check is due.

        Args:
        ----
            network_id: The ID of the network.

        Returns:
        -------
            True if the check is due, False otherwise.

        """
        return self._is_check_due(self._traffic_check_timestamps, network_id)

    def mark_vlan_check_done(self, network_id: str) -> None:
        """
        Mark a VLAN availability check as done for the day.

        Args:
        ----
            network_id: The ID of the network.

        """
        self._vlan_check_timestamps[network_id] = datetime.now()

    def mark_traffic_check_done(self, network_id: str) -> None:
        """
        Mark a Traffic Analysis availability check as done for the day.

        Args:
        ----
            network_id: The ID of the network.

        """
        self._traffic_check_timestamps[network_id] = datetime.now()
