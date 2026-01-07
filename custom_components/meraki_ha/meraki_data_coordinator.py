"""Data update coordinator for the Meraki HA integration."""

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_ENABLED_NETWORKS,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .core.api.client import MerakiAPIClient as ApiClient
from .core.errors import ApiClientCommunicationError
from .types import MerakiDevice, MerakiNetwork

_LOGGER = logging.getLogger(__name__)


class MerakiDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """A centralized coordinator for Meraki API data."""

    def __init__(
        self,
        hass: "HomeAssistant",
        api_client: ApiClient,
        entry: ConfigEntry,
    ) -> None:
        """
        Initialize the coordinator.

        Args:
        ----
            hass: The Home Assistant instance.
            entry: The config entry.

        """
        self.api = api_client
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

    def is_update_pending(self, unique_id: str) -> bool:
        """
        Check if an entity update is in a pending (cooldown) state.

        Args:
        ----
            unique_id: The unique ID of the entity.

        Returns
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

    def is_pending(self, unique_id: str) -> bool:
        """
        Check if an entity update is in a pending (cooldown) state.

        Args:
        ----
            unique_id: The unique ID of the entity.

        Returns
        -------
            True if the entity is in a pending state, False otherwise.

        """
        return self.is_update_pending(unique_id)

    def register_pending(
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
        self.register_pending_update(unique_id, expiry_seconds)

    def _filter_enabled_networks(self, data: dict[str, Any]) -> None:
        """
        Filter out networks that the user has chosen to disable.

        Args:
        ----
            data: The data dictionary to filter.

        """
        if not self.config_entry or not hasattr(self.config_entry, "options"):
            _LOGGER.debug(
                "Config entry or options not available, "
                "cannot filter enabled networks.",
            )
            return
        enabled_network_ids = self.config_entry.options.get(
            CONF_ENABLED_NETWORKS,
        )

        # If the option is not set, all networks are enabled by default.
        if enabled_network_ids is None:
            enabled_network_ids = [
                n["id"] for n in data.get("networks", []) if "id" in n
            ]

        if "networks" in data:
            for network in data["networks"]:
                network["is_enabled"] = network.get("id") in enabled_network_ids

            # Filter devices and SSIDs to only include those from enabled networks
            if "devices" in data:
                data["devices"] = [
                    d
                    for d in data["devices"]
                    if d.get("networkId") in enabled_network_ids
                ]
            if "ssids" in data:
                data["ssids"] = [
                    s
                    for s in data["ssids"]
                    if s.get("networkId") in enabled_network_ids
                ]

    async def _async_remove_disabled_devices(self, data: dict[str, Any]) -> None:
        """
        Remove devices and entities from disabled networks.

        Args:
        ----
            data: The data dictionary containing the latest device information.

        """
        if not self.config_entry:
            return

        dev_reg = dr.async_get(self.hass)
        ent_reg = er.async_get(self.hass)

        # Get identifiers for all devices associated with this config entry
        device_ids_in_registry = {
            list(device.identifiers)[0][1]
            for device in dev_reg.devices.values()
            if self.config_entry.entry_id in device.config_entries
        }

        # Build a set of all valid identifiers from the latest coordinator data
        # Physical devices use serial number as identifier
        latest_valid_identifiers: set[str] = {
            device["serial"] for device in data.get("devices", [])
        }

        # SSIDs use ssid_{network_id}_{ssid_number} format
        for ssid in data.get("ssids", []):
            network_id = ssid.get("networkId")
            ssid_number = ssid.get("number")
            if network_id and ssid_number is not None:
                latest_valid_identifiers.add(f"ssid_{network_id}_{ssid_number}")

        # Networks use network_{network_id} format
        for network in data.get("networks", []):
            if network.get("is_enabled"):
                latest_valid_identifiers.add(f"network_{network['id']}")

        # VLANs use vlan_{network_id}_{vlan_id} format
        for network_id, vlans in data.get("vlans", {}).items():
            if isinstance(vlans, list):
                for vlan in vlans:
                    if "id" in vlan:
                        latest_valid_identifiers.add(f"vlan_{network_id}_{vlan['id']}")

        # Organization uses org_{org_id} format
        org_data = data.get("organization", {})
        if org_data.get("id"):
            latest_valid_identifiers.add(f"org_{org_data['id']}")

        # Determine which device identifiers to remove
        device_ids_to_remove = device_ids_in_registry - latest_valid_identifiers

        for device_id in device_ids_to_remove:
            device = dev_reg.async_get_device(identifiers={(DOMAIN, device_id)})
            if device:
                _LOGGER.debug("Removing device %s and its entities.", device_id)
                entities = er.async_entries_for_device(ent_reg, device.id)
                for entity in entities:
                    ent_reg.async_remove(entity.entity_id)
                dev_reg.async_remove_device(device.id)

    def _populate_ssid_entities(self, data: dict[str, Any]) -> None:
        """
        Populate SSID data with associated Home Assistant entities.

        Args:
        ----
            data: The data dictionary to populate.

        """
        if not (data and "ssids" in data):
            return

        ent_reg = er.async_get(self.hass)
        dev_reg = dr.async_get(self.hass)

        for ssid in data["ssids"]:
            network_id = ssid.get("networkId")
            ssid_number = ssid.get("number")
            if network_id and ssid_number is not None:
                # Construct the device identifier for the SSID
                # Note: This must match the identifier logic in device_info_helpers.py
                identifier = f"ssid_{network_id}_{ssid_number}"

                ha_device = dev_reg.async_get_device(
                    identifiers={(DOMAIN, identifier)},
                )

                if ha_device:
                    entities_for_device = er.async_entries_for_device(
                        ent_reg,
                        ha_device.id,
                    )

                    # Find the enabled switch
                    for entity in entities_for_device:
                        if entity.domain == "switch" and (
                            "enabled" in (entity.unique_id or "")
                            or "Enabled Control" in (entity.original_name or "")
                        ):
                            ssid["entity_id"] = entity.entity_id
                            break

    def _process_sensor_readings_for_frontend(
        self, readings: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Process raw sensor readings into a flat format for the frontend.

        The Meraki API returns readings as a list like:
        [{"metric": "temperature", "temperature": {"celsius": 23.5}}, ...]

        This converts it to:
        {"temperature": 23.5, "humidity": 45, ...}

        Args:
        ----
            readings: The raw readings list from the Meraki API.

        Returns
        -------
            A flat dictionary with metric names as keys and values.

        """
        if not readings or not isinstance(readings, list):
            return {}

        result: dict[str, Any] = {}
        key_map = {
            "temperature": "celsius",
            "humidity": "relativePercentage",
            "pm25": "concentration",
            "tvoc": "concentration",
            "co2": "concentration",
            "noise": "ambient",
            "water": "present",
            "power": "draw",
            "voltage": "level",
            "current": "draw",
            "battery": "percentage",
            "button": "pressType",
        }

        for reading in readings:
            metric = reading.get("metric")
            if not metric:
                continue

            metric_data = reading.get(metric)
            if isinstance(metric_data, dict):
                value_key = key_map.get(metric)
                if value_key:
                    if value_key == "ambient":
                        value = metric_data.get("ambient", {}).get("level")
                    else:
                        value = metric_data.get(value_key)
                    if value is not None:
                        result[metric] = value

        return result

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

            # Process raw sensor readings into frontend-friendly format.
            # Keep original list for sensor entities, add flat dict for frontend.
            raw_readings = device.get("readings")
            if raw_readings and isinstance(raw_readings, list):
                # Store flat readings for frontend consumption
                device["readings"] = self._process_sensor_readings_for_frontend(
                    raw_readings
                )
                # Keep original list for sensor entities under a different key
                device["readings_raw"] = raw_readings

            ha_device = dev_reg.async_get_device(
                identifiers={(DOMAIN, device["serial"])},
            )
            if ha_device:
                entities_for_device = er.async_entries_for_device(
                    ent_reg,
                    ha_device.id,
                )
                if entities_for_device:
                    # Prioritize more representative entities
                    primary_entity = None
                    device_entities = []
                    for entity in entities_for_device:
                        # Collect entity details for the frontend
                        state = self.hass.states.get(entity.entity_id)
                        device_entities.append(
                            {
                                "name": entity.name or entity.original_name,
                                "entity_id": entity.entity_id,
                                "state": state.state if state else "unknown",
                            }
                        )

                        if not primary_entity and entity.domain in [
                            "switch",
                            "camera",
                            "binary_sensor",
                        ]:
                            primary_entity = entity

                        # If we haven't found a preferred platform entity yet,
                        # check if this is the dedicated device status sensor.
                        # This ensures we prefer a "clean" status sensor over
                        # random other sensors if available.
                        elif (
                            not primary_entity
                            and entity.unique_id
                            and entity.unique_id.endswith("_device_status")
                        ):
                            primary_entity = entity

                    device["entities"] = device_entities

                    if primary_entity:
                        device["entity_id"] = primary_entity.entity_id
                    else:
                        # Fallback: Pick the first non-button entity if possible.
                        # Button entities often have a timestamp state (last pressed),
                        # which is confusing for a "status" display.
                        fallback_entity = entities_for_device[0]
                        for entity in entities_for_device:
                            if entity.domain != "button":
                                fallback_entity = entity
                                break
                        device["entity_id"] = fallback_entity.entity_id

                    # Add list of entities to device data for frontend
                    device["entities"] = []
                    for entity in entities_for_device:
                        state_obj = self.hass.states.get(entity.entity_id)
                        device["entities"].append(
                            {
                                "name": entity.name or entity.original_name,
                                "entity_id": entity.entity_id,
                                "state": state_obj.state if state_obj else "unknown",
                            }
                        )

    def _get_enabled_network_ids(self) -> set[str] | None:
        """
        Get the set of enabled network IDs from config options.

        Returns
        -------
            A set of enabled network IDs, or None if all networks should be
            enabled (e.g., when the option is not set or config is unavailable).

        """
        if not self.config_entry or not hasattr(self.config_entry, "options"):
            return None

        enabled_network_ids = self.config_entry.options.get(CONF_ENABLED_NETWORKS)

        # If the option is not set or is empty, return None to poll all networks
        if not enabled_network_ids:
            return None

        return set(enabled_network_ids)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint and apply filters."""
        try:
            # Get enabled network IDs to filter API calls upfront
            enabled_network_ids = self._get_enabled_network_ids()

            data = await self.api.get_all_data(
                self.last_successful_data,
                enabled_network_ids=enabled_network_ids,
            )
            if not data:
                _LOGGER.warning("API call to get_all_data returned no data.")
                raise UpdateFailed("API call returned no data.")

            self._filter_enabled_networks(data)
            _LOGGER.debug("SSIDs after filtering: %s", data.get("ssids"))
            await self._async_remove_disabled_devices(data)

            # Process errors and update timers
            for network_id, traffic_data in data.get("appliance_traffic", {}).items():
                if (
                    isinstance(traffic_data, dict)
                    and traffic_data.get("error") == "disabled"
                ):
                    self.add_network_status_message(
                        network_id, "Traffic Analysis is not enabled for this network."
                    )
                    self.mark_traffic_check_done(network_id)
            for network_id, vlan_data in data.get("vlans", {}).items():
                if isinstance(vlan_data, list) and not vlan_data:
                    self.add_network_status_message(
                        network_id, "VLANs are not enabled for this network."
                    )
                    self.mark_vlan_check_done(network_id)

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

            # Add SSIDs to each network for easier access in the UI
            all_ssids = data.get("ssids", [])
            for network in data.get("networks", []):
                network_id = network.get("id")
                if network_id:
                    network["ssids"] = [
                        ssid
                        for ssid in all_ssids
                        if ssid.get("networkId") == network_id
                    ]

            self._populate_device_entities(data)
            self._populate_ssid_entities(data)

            _LOGGER.info("Meraki networks: %s", data.get("networks"))

            self.last_successful_update = datetime.now()
            self.last_successful_data = data
            return data
        except ApiClientCommunicationError as err:
            # If we have successfully fetched data before, log a warning and return
            # the stale data. Otherwise, raise UpdateFailed to indicate that the
            # integration cannot start.
            if self.last_successful_data:
                _LOGGER.warning(
                    "Could not connect to Meraki API, using stale data. "
                    "This is expected if the internet connection is down. "
                    "Error: %s",
                    err,
                )
                return self.last_successful_data
            raise UpdateFailed(f"Could not connect to Meraki API: {err}") from err
        except Exception as err:
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

        Returns
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

        Returns
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

        Returns
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

        Returns
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
