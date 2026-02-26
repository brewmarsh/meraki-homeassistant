"""Uplink performance sensors for Meraki appliances."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Literal

from homeassistant.components.sensor import (
    SensorDeviceClass,  # Added for potential future use in METRIC_MAPPING
    SensorEntityDescription,
)
from homeassistant.const import PERCENTAGE, UnitOfTime
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN
from ..entity import MerakiSensor

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from ..coordinator import MerakiDataUpdateCoordinator
    from ..core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)

# --- Constants for metrics and units ---
# Using a dict to map user-friendly metric names to Meraki API keys and Home Assistant units/device classes.
# This centralizes configuration and makes the __init__ method cleaner.
METRIC_MAPPING: dict[str, dict[str, Any]] = {
    "latency": {
        "api_key": "latencyMs",
        "unit": UnitOfTime.MILLISECONDS,
        "device_class": SensorDeviceClass.DURATION,
    },
    "jitter": {
        "api_key": "jitter",
        "unit": UnitOfTime.MILLISECONDS,
        "device_class": SensorDeviceClass.DURATION,
    },
    "lossPercent": {
        "api_key": "lossPercent",
        "unit": PERCENTAGE,
        # Home Assistant does not have a specific device class for "percentage of loss".
        # SensorDeviceClass.DURATION is not appropriate here. Leaving as None for now.
        "device_class": None,
    },
}


class MerakiUplinkPerformanceSensor(MerakiSensor):
    """Representation of a Meraki uplink performance sensor."""

    # Explicitly type key attributes for clarity and static analysis
    _device_serial: str
    _interface: str
    _metric_api_key: str
    _attr_native_unit_of_measurement: str | None

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,  # Kept for consistency, though not directly used here
        interface: str,
        metric: Literal[
            "latency", "jitter", "lossPercent"
        ],  # Enforce allowed metric strings
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

        if not device.serial:
            _LOGGER.error(
                "Device serial is required for uplink performance sensor (Device: %s)",
                device.name,
            )
            raise ValueError(
                f"Device serial is required for uplink performance sensor (Device: {device.name})"
            )
        self._device_serial = device.serial
        self._interface = interface

        # Resolve metric details using the predefined mapping
        metric_details = METRIC_MAPPING.get(metric)
        if not metric_details:
            _LOGGER.error(
                "Unsupported uplink performance metric: %s for device %s. Supported: %s",
                metric,
                device.name,
                ", ".join(METRIC_MAPPING.keys()),
            )
            raise ValueError(f"Unsupported uplink performance metric: {metric}")

        self._metric_api_key = metric_details["api_key"]
        self._attr_native_unit_of_measurement = metric_details["unit"]
        # Uncomment and assign if you wish to use a device class for the sensor
        # self._attr_device_class = metric_details["device_class"]

        self.entity_description = description

        # Use Home Assistant Sentence Case for names
        # Entity name will be e.g. "WAN1 Latency"
        # Since _attr_has_entity_name is True in MerakiEntity,
        # the final name will be "Device Name WAN1 Latency"
        self._attr_unique_id = (
            f"{self._device_serial}_{interface}_{self._metric_api_key}"
        )

        # DeviceInfo needs to be set. _device_serial is guaranteed at this point.
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
        )
        self._update_state()

    def _get_uplink_metric_value(
        self,
        uplinks: list[dict[str, Any]],
        interface: str,
        metric_api_key: str,
    ) -> float | None:
        """
        Helper to find and parse the metric value for a specific uplink interface.
        Encapsulates the iteration and type conversion logic.
        """
        for uplink in uplinks:
            if uplink.get("interface") == interface:
                value = uplink.get(metric_api_key)
                if value is not None:
                    try:
                        return float(value)
                    except (ValueError, TypeError):
                        _LOGGER.debug(
                            "Could not convert uplink value '%s' to float for interface '%s', metric '%s' on entity '%s'. "
                            "This may indicate unexpected data format from Meraki API.",
                            value,
                            interface,
                            metric_api_key,
                            self.name,
                        )
                        return None  # Value found but invalid type
                else:
                    _LOGGER.debug(
                        "Uplink metric '%s' value is None for interface '%s' on entity '%s'.",
                        metric_api_key,
                        interface,
                        self.name,
                    )
                    return None  # Interface found, but metric value is None
        _LOGGER.debug(
            "Uplink interface '%s' not found in device uplinks for entity '%s'.",
            interface,
            self.name,
        )
        return None  # Interface not found in any uplink

    @callback
    def _update_state(self) -> None:
        """Update the sensor state from the coordinator data."""
        device = self.coordinator.get_device(self._device_serial)
        if not device or not device.uplinks:
            _LOGGER.debug(
                "No device or no uplink data found for serial %s. Setting state to None for %s.",
                self._device_serial,
                self.name,
            )
            self._attr_native_value = None
            return

        self._attr_native_value = self._get_uplink_metric_value(
            uplinks=device.uplinks,
            interface=self._interface,
            metric_api_key=self._metric_api_key,
        )

        # If after attempting to get the value, it's still None, log informative message.
        if self._attr_native_value is None:
            _LOGGER.debug(
                "Final native value for '%s' on interface '%s' for device %s is None. "
                "The metric might be missing or invalid in the latest update.",
                self._metric_api_key,
                self._interface,
                self._device_serial,
            )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()
