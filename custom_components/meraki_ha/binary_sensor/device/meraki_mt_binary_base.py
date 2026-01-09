"""Base class for Meraki MT binary sensor entities."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiMtBinarySensor(
    CoordinatorEntity[MerakiDataCoordinator], BinarySensorEntity
):
    """Representation of a Meraki MT binary sensor."""

    coordinator: MerakiDataCoordinator

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Mapping[str, Any],
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._device = device
        self.entity_description = entity_description
        self._attr_unique_id = f"{self._device['serial']}_{entity_description.key}"
        self._attr_name = f"{self._device['name']} {entity_description.name}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device.get("model", "MT Sensor"),
            manufacturer="Cisco Meraki",
        )

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device.get("serial"):
                    return dev_data
        return None

    def _get_readings(self) -> list[dict[str, Any]] | None:
        """Get the readings list from the current device data."""
        device = self._get_current_device_data()
        if not device:
            return None
        # Use readings_raw (list format) for sensor entities
        readings = device.get("readings_raw") or device.get("readings")
        if isinstance(readings, list):
            return readings
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        current_data = self._get_current_device_data()
        if current_data:
            self._device = current_data
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not self.coordinator.last_update_success:
            return False

        readings = self._get_readings()
        if not readings:
            return False

        # Check if there's a reading for this specific metric
        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                return True
        return False

    def _get_reading_timestamp(self) -> str | None:
        """Get the timestamp from the current reading."""
        readings = self._get_readings()
        if not readings:
            return None

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                # Meraki readings include 'ts' field with ISO timestamp
                return reading.get("ts")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return entity state attributes with update source and timestamps."""
        attrs: dict[str, Any] = {}

        # Get the actual reading timestamp from the data
        reading_ts = self._get_reading_timestamp()
        if reading_ts:
            attrs["last_updated"] = reading_ts

        # Determine data source and add relevant timestamps
        serial = self._device.get("serial")
        if serial:
            mqtt_update = self.coordinator.get_mqtt_last_update(serial)
            if mqtt_update:
                attrs["data_source"] = "mqtt"
                attrs["last_mqtt_update"] = mqtt_update.isoformat()
            elif self.coordinator.mqtt_enabled:
                attrs["data_source"] = "mqtt_pending"
            else:
                attrs["data_source"] = "api"

        # Add coordinator update timestamp for reference
        if self.coordinator.last_successful_update:
            attrs["last_coordinator_update"] = (
                self.coordinator.last_successful_update.isoformat()
            )

        return attrs if attrs else None

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        # Always get fresh data from coordinator
        readings = self._get_readings()
        if not readings:
            return None

        for reading in readings:
            metric = reading.get("metric")
            if metric == self.entity_description.key:
                # API returns nested data like:
                #   {"metric": "door", "door": {"open": true}}
                #   {"metric": "water", "water": {"present": true}}
                metric_data = reading.get(self.entity_description.key)
                if isinstance(metric_data, dict):
                    # Map metric to the key holding the boolean value
                    key_map = {
                        "door": "open",
                        "water": "present",
                    }
                    value_key = key_map.get(self.entity_description.key)
                    if value_key:
                        value = metric_data.get(value_key)
                        if isinstance(value, bool):
                            return value
                elif isinstance(metric_data, bool):
                    # Direct boolean value
                    return metric_data

                # Fallback: check for "value" key (legacy format)
                value = reading.get("value")
                if isinstance(value, bool):
                    return value
                if isinstance(value, str):
                    return value.lower() in ("true", "1", "on", "open")
        return None
