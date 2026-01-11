"""Data update coordinator for the Meraki HA integration."""

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .async_logging import async_log_time
from .const import (
    CONF_CLIENT_SCAN_INTERVAL,
    CONF_DASHBOARD_DEVICE_TYPE_FILTER,
    CONF_DEVICE_SCAN_INTERVAL,
    CONF_ENABLE_MQTT,
    CONF_ENABLED_NETWORKS,
    CONF_NETWORK_SCAN_INTERVAL,
    CONF_SSID_SCAN_INTERVAL,
    DEFAULT_CLIENT_SCAN_INTERVAL,
    DEFAULT_DEVICE_SCAN_INTERVAL,
    DEFAULT_ENABLE_MQTT,
    DEFAULT_NETWORK_SCAN_INTERVAL,
    DEFAULT_SSID_SCAN_INTERVAL,
    DOMAIN,
)
from .core.api.client import MerakiAPIClient as ApiClient
from .core.errors import ApiClientCommunicationError
from .helpers.logging_helper import MerakiLoggers
from .types import MerakiDevice, MerakiNetwork

# Use feature-specific logger - can be configured independently via:
# logger:
#   logs:
#     custom_components.meraki_ha.coordinator: warning
_LOGGER = MerakiLoggers.COORDINATOR


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

        # Tiered polling timestamps
        self.last_network_update: datetime | None = None
        self.last_device_update: datetime | None = None
        self.last_client_update: datetime | None = None
        self.last_ssid_update: datetime | None = None

        # MQTT-related state
        self._mqtt_enabled: bool = bool(
            entry.options.get(CONF_ENABLE_MQTT, DEFAULT_ENABLE_MQTT)
        )
        self._mqtt_last_updates: dict[str, datetime] = {}  # serial -> last MQTT update

        # Set a short update interval for the coordinator to run frequently
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )

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
        if unique_id is None:
            return
        expiry_time = datetime.now() + timedelta(seconds=expiry_seconds)
        self._pending_updates[unique_id] = expiry_time
        _LOGGER.debug(
            "Registered pending update for %s, ignoring coordinator updates until %s",
            unique_id,
            expiry_time,
        )

    def is_update_pending(self, unique_id: str | None) -> bool:
        """
        Check if an entity update is in a pending (cooldown) state.

        Args:
        ----
            unique_id: The unique ID of the entity.

        Returns
        -------
            True if the entity is in a pending state, False otherwise.

        """
        if unique_id is None or unique_id not in self._pending_updates:
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

    def is_pending(self, unique_id: str | None) -> bool:
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
        self.register_pending_update(unique_id, expiry_seconds)

    def cancel_pending_update(self, unique_id: str | None) -> None:
        """
        Cancel a pending update for an entity.

        Args:
        ----
            unique_id: The unique ID of the entity.

        """
        if unique_id is None:
            return
        if unique_id in self._pending_updates:
            del self._pending_updates[unique_id]
            _LOGGER.debug("Cancelled pending update for %s", unique_id)

    @property
    def mqtt_enabled(self) -> bool:
        """Return True if MQTT mode is enabled."""
        return self._mqtt_enabled

    def set_mqtt_enabled(self, enabled: bool) -> None:
        """
        Set the MQTT enabled state.

        Args:
        ----
            enabled: Whether MQTT mode should be enabled.

        """
        self._mqtt_enabled = enabled

    def get_mqtt_last_update(self, serial: str) -> datetime | None:
        """
        Get the timestamp of the last MQTT update for a device.

        Args:
        ----
            serial: The device serial number.

        Returns
        -------
            The timestamp of the last MQTT update, or None if never updated.

        """
        return self._mqtt_last_updates.get(serial)

    async def async_update_from_mqtt(
        self,
        serial: str,
        metric: str,
        data: dict[str, Any],
    ) -> None:
        """
        Update sensor data from an MQTT message.

        This method is called by the MQTT service when a message is received.
        It updates the device's readings in the coordinator data and notifies
        all listeners.

        Args:
        ----
            serial: The device serial number.
            metric: The metric name (e.g., "temperature", "humidity").
            data: The parsed MQTT payload data.

        """
        if not self.data or "devices" not in self.data:
            _LOGGER.debug(
                "Cannot update from MQTT - coordinator data not yet available"
            )
            return

        # Find the device using O(1) lookup table instead of linear search
        device = self.devices_by_serial.get(serial)
        if device is None:
            _LOGGER.debug("Device %s not found in coordinator data", serial)
            return

        # Update the readings_raw list with the new MQTT data
        readings_raw = device.get("readings_raw", [])
        if not isinstance(readings_raw, list):
            readings_raw = []

        # Build the new reading in the Meraki API format
        new_reading = self._mqtt_data_to_reading(metric, data)
        if new_reading is None:
            return

        # Find and update existing reading for this metric, or append new one
        found = False
        for i, reading in enumerate(readings_raw):
            if reading.get("metric") == metric:
                readings_raw[i] = new_reading
                found = True
                break

        if not found:
            readings_raw.append(new_reading)

        # Update device data directly (device is a reference to the same object
        # in self.data["devices"], so changes are reflected in both places)
        device["readings_raw"] = readings_raw
        device["readings"] = self._process_sensor_readings_for_frontend(readings_raw)

        # Track MQTT update timestamp
        mqtt_update_time = datetime.now()
        self._mqtt_last_updates[serial] = mqtt_update_time

        # Update readings_meta with timestamp and data source
        # Use the timestamp from the reading if available, otherwise use current time
        reading_ts = data.get("ts") or mqtt_update_time.isoformat()
        device["readings_meta"] = {
            "last_updated": reading_ts,
            "data_source": "mqtt",
        }

        _LOGGER.debug(
            "Updated device %s metric %s from MQTT",
            serial,
            metric,
        )

        # Notify all listeners that data has changed
        self.async_update_listeners()

    def _mqtt_data_to_reading(
        self,
        metric: str,
        data: dict[str, Any],
    ) -> dict[str, Any] | None:
        """
        Convert MQTT payload data to Meraki API reading format.

        Args:
        ----
            metric: The metric name.
            data: The MQTT payload data.

        Returns
        -------
            A reading dict in Meraki API format, or None if conversion fails.

        """
        # MQTT format examples from Meraki documentation:
        # temperature: {"ts": "...", "fahrenheit": 72.6, "celsius": 22.6}
        # humidity: {"ts": "...", "humidity": 62}
        # waterDetection: {"ts": "...", "wet": false}
        # etc.

        # Include the timestamp from MQTT data if available
        reading: dict[str, Any] = {"metric": metric}
        if "ts" in data:
            reading["ts"] = data["ts"]

        if metric == "temperature":
            reading["temperature"] = {
                "celsius": data.get("celsius"),
                "fahrenheit": data.get("fahrenheit"),
            }
        elif metric == "humidity":
            reading["humidity"] = {"relativePercentage": data.get("humidity")}
        elif metric == "waterDetection":
            reading["water"] = {"present": data.get("wet")}
        elif metric in ("pm25", "tvoc", "co2"):
            # These share the same structure
            reading[metric] = {"concentration": data.get(metric)}
        elif metric == "noise":
            reading["noise"] = {"ambient": {"level": data.get("noise")}}
        elif metric == "indoorAirQuality":
            reading["indoorAirQuality"] = {"score": data.get("indoorAirQuality")}
        elif metric == "batteryPercentage":
            reading["metric"] = "battery"
            reading["battery"] = {"percentage": data.get("battery percentage")}
        elif metric == "buttonPressed":
            reading["metric"] = "button"
            reading["button"] = {
                "pressType": "short" if data.get("button pressed") else None
            }
        elif metric == "usbPowered":
            reading["metric"] = "usb_powered"
            reading["usb_powered"] = {"powered": data.get("usb powered", False)}
        elif metric == "cableConnected":
            reading["metric"] = "cable_connected"
            reading["cable_connected"] = {
                "connected": data.get("cable connected", False)
            }
        elif metric == "probeType":
            reading["metric"] = "probe_type"
            reading["probe_type"] = {"type": data.get("probe type")}
        elif metric == "door":
            reading["door"] = {"open": data.get("open")}
        elif metric == "mainsVolts":
            reading["metric"] = "voltage"
            reading["voltage"] = {"level": data.get("mainsVolts")}
        elif metric == "mainsCurrent":
            reading["metric"] = "current"
            reading["current"] = {"draw": data.get("mainsCurrent")}
        elif metric == "mainsRealPower":
            reading["metric"] = "realPower"
            reading["realPower"] = {"draw": data.get("mainsRealPower")}
        elif metric == "mainsApparentPower":
            reading["metric"] = "apparentPower"
            reading["apparentPower"] = {"draw": data.get("mainsApparentPower")}
        elif metric == "mainsPowerFactor":
            reading["metric"] = "powerFactor"
            reading["powerFactor"] = {"percentage": data.get("mainsPowerFactor")}
        elif metric == "mainsFrequency":
            reading["metric"] = "frequency"
            reading["frequency"] = {"level": data.get("mainsFrequency")}
        elif metric == "mainsDeltaEnergy":
            reading["metric"] = "energy"
            reading["energy"] = {"usage": data.get("mainsDeltaEnergy")}
        elif metric == "downstreamPowerStatus":
            reading["metric"] = "downstream_power"
            reading["value"] = data.get("downstreamPower") == "on"
        elif metric.startswith("gateway/") and metric.endswith("/rssi"):
            # Gateway RSSI metric: gateway/{ap_mac}/rssi
            # Extract AP MAC from metric path
            parts = metric.split("/")
            if len(parts) == 3:
                ap_mac = parts[1]
                reading["metric"] = "gateway_rssi"
                reading["gateway_rssi"] = {
                    "ap_mac": ap_mac,
                    "rssi": data.get("rssi"),
                    "units": data.get("units", "dBm"),
                }
            else:
                _LOGGER.debug("Malformed gateway RSSI metric: %s", metric)
                return None
        else:
            _LOGGER.debug("Unknown MQTT metric: %s", metric)
            return None

        return reading

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
            if not device:
                continue

            entities = er.async_entries_for_device(ent_reg, device.id)
            if not entities:
                # No entities - safe to remove orphaned device
                _LOGGER.debug("Removing orphaned device %s (no entities)", device_id)
                dev_reg.async_remove_device(device.id)
                continue

            # Device has entities - check if they should migrate to a valid device
            # An entity should migrate if a device with valid identifier exists
            # that matches what the entity's unique_id suggests
            should_remove = True
            for entity in entities:
                # Check if this entity's unique_id references data we still have
                # If the unique_id contains a serial that exists, keep entity
                unique_id = entity.unique_id or ""
                entity_refs_valid_data = any(
                    valid_id in unique_id for valid_id in latest_valid_identifiers
                )
                if not entity_refs_valid_data:
                    # Entity references data we don't have anymore - remove it
                    _LOGGER.debug(
                        "Removing stale entity %s (references removed data)",
                        entity.entity_id,
                    )
                    ent_reg.async_remove(entity.entity_id)
                else:
                    # Entity references valid data but is on wrong device
                    # This shouldn't happen after reload - warn and keep device
                    _LOGGER.warning(
                        "Entity %s on stale device %s references valid data - "
                        "reload integration to fix device association",
                        entity.entity_id,
                        device_id,
                    )
                    should_remove = False

            if should_remove:
                _LOGGER.debug("Removing device %s after cleaning entities", device_id)
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
            "realPower": "draw",  # API uses realPower
            "apparentPower": "draw",
            "voltage": "level",
            "current": "draw",
            "battery": "percentage",
            "button": "pressType",
            "door": "open",
            "indoorAirQuality": "score",
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

                # Add readings_meta with timestamp and data source
                # Check if this device has MQTT updates (preserve MQTT source if active)
                serial = device.get("serial", "")
                mqtt_update = self._mqtt_last_updates.get(serial)
                if mqtt_update and self._mqtt_enabled:
                    # MQTT is providing data - keep existing meta
                    pass
                else:
                    # Extract timestamp from readings if available
                    last_ts = None
                    for reading in raw_readings:
                        ts = reading.get("ts")
                        if ts:
                            last_ts = ts
                            break
                    device["readings_meta"] = {
                        "last_updated": last_ts or datetime.now().isoformat(),
                        "data_source": "api",
                    }

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

    def _filter_device_types(self, data: dict[str, Any]) -> None:
        """Filter out devices by type based on user's selection."""
        if not self.config_entry or not hasattr(self.config_entry, "options"):
            _LOGGER.debug(
                "Config entry or options not available, cannot filter device types.",
            )
            return

        selected_types = self.config_entry.options.get(
            CONF_DASHBOARD_DEVICE_TYPE_FILTER
        )

        if not selected_types or "all" in selected_types:
            return

        if "devices" in data:
            type_map = {
                "switch": "MS",
                "camera": "MV",
                "wireless": "MR",
                "sensor": "MT",
                "appliance": "MX",
            }
            prefixes_to_keep = tuple(
                type_map[type_] for type_ in selected_types if type_ in type_map
            )

            if prefixes_to_keep:
                data["devices"] = [
                    d
                    for d in data["devices"]
                    if d.get("model", "").startswith(prefixes_to_keep)
                ]

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

    @async_log_time(MerakiLoggers.COORDINATOR, slow_threshold=10.0)
    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint based on tiered polling intervals."""
        now = datetime.now()

        # Get intervals from config entry options
        if not self.config_entry:
            raise UpdateFailed("Configuration entry not available.")

        network_interval_seconds = self.config_entry.options.get(
            CONF_NETWORK_SCAN_INTERVAL, DEFAULT_NETWORK_SCAN_INTERVAL
        )
        device_interval_seconds = self.config_entry.options.get(
            CONF_DEVICE_SCAN_INTERVAL, DEFAULT_DEVICE_SCAN_INTERVAL
        )
        client_interval_seconds = self.config_entry.options.get(
            CONF_CLIENT_SCAN_INTERVAL, DEFAULT_CLIENT_SCAN_INTERVAL
        )
        ssid_interval_seconds = self.config_entry.options.get(
            CONF_SSID_SCAN_INTERVAL, DEFAULT_SSID_SCAN_INTERVAL
        )

        network_interval = timedelta(seconds=network_interval_seconds)
        device_interval = timedelta(seconds=device_interval_seconds)
        client_interval = timedelta(seconds=client_interval_seconds)
        ssid_interval = timedelta(seconds=ssid_interval_seconds)

        # Determine which data to fetch
        fetch_networks = (
            self.last_network_update is None
            or (now - self.last_network_update) > network_interval
        )
        fetch_devices = (
            self.last_device_update is None
            or (now - self.last_device_update) > device_interval
        )
        fetch_clients = (
            self.last_client_update is None
            or (now - self.last_client_update) > client_interval
        )
        fetch_ssids = (
            self.last_ssid_update is None
            or (now - self.last_ssid_update) > ssid_interval
        )

        if not any([fetch_networks, fetch_devices, fetch_clients, fetch_ssids]):
            _LOGGER.debug("No polling interval reached, skipping API call.")
            return self.last_successful_data

        try:
            enabled_network_ids = self._get_enabled_network_ids()

            data = await self.api.get_all_data(
                self.last_successful_data,
                enabled_network_ids=enabled_network_ids,
                fetch_networks=fetch_networks,
                fetch_devices=fetch_devices,
                fetch_clients=fetch_clients,
                fetch_ssids=fetch_ssids,
            )
            if not data:
                _LOGGER.warning("API call to get_all_data returned no data.")
                raise UpdateFailed("API call returned no data.")

            if fetch_networks:
                self.last_network_update = now
            if fetch_devices:
                self.last_device_update = now
            if fetch_clients:
                self.last_client_update = now
            if fetch_ssids:
                self.last_ssid_update = now

            self._filter_enabled_networks(data)
            self._filter_device_types(data)
            await self._async_remove_disabled_devices(data)

            # Process errors and update timers
            for nid, traffic in data.get("appliance_traffic", {}).items():
                is_disabled = (
                    isinstance(traffic, dict) and traffic.get("error") == "disabled"
                )
                if is_disabled:
                    self.add_network_status_message(
                        nid, "Traffic Analysis is not enabled for this network."
                    )
                    self.mark_traffic_check_done(nid)

            for nid, vlans in data.get("vlans", {}).items():
                is_empty = isinstance(vlans, list) and not vlans
                if is_empty:
                    self.add_network_status_message(
                        nid, "VLANs are not enabled for this network."
                    )
                    self.mark_vlan_check_done(nid)

            # Create lookup tables
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

            # Add SSIDs to each network
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

            self.last_successful_update = now
            self.last_successful_data = data
            return data
        except ApiClientCommunicationError as err:
            if self.last_successful_data:
                _LOGGER.warning(
                    "Could not connect to Meraki API, using stale data. Error: %s",
                    err,
                )
                return self.last_successful_data
            raise UpdateFailed(f"Could not connect to Meraki API: {err}") from err
        except Exception as err:
            _LOGGER.error(
                "Unexpected error fetching Meraki data: %s", err, exc_info=True
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

    async def async_handle_scanning_api_data(self, data: dict[str, Any]) -> None:
        """
        Update client data from a Scanning API webhook payload.

        This method is called by the webhook handler when a POST request is received.
        It updates the client's data in the coordinator and notifies all listeners,
        but only for clients that already exist.

        Args:
        ----
            data: The parsed "data" object from the Scanning API payload.

        """
        if not self.data or "clients" not in self.data:
            _LOGGER.debug(
                "Cannot update from Scanning API - coordinator data not yet available"
            )
            return

        clients_by_mac = {
            client.get("mac"): client for client in self.data.get("clients", [])
        }
        ap_mac = data.get("apMac")
        updated_clients = 0

        for observation in data.get("observations", []):
            client_mac = observation.get("clientMac")
            if not client_mac:
                continue

            client = clients_by_mac.get(client_mac)
            if client:
                # This is an existing client, update its data
                updated_clients += 1
                client["lastSeen"] = observation.get("seenTime")
                client["rssi"] = observation.get("rssi")
                if ap_mac:
                    client["recentDeviceMac"] = ap_mac

                location = observation.get("location")
                if isinstance(location, dict):
                    client["latitude"] = location.get("lat")
                    client["longitude"] = location.get("lng")
            else:
                _LOGGER.debug(
                    "Ignoring Scanning API observation for unknown client MAC: %s",
                    client_mac,
                )

        if updated_clients > 0:
            _LOGGER.info("Updated %d client(s) from Scanning API data", updated_clients)
            self.async_update_listeners()
