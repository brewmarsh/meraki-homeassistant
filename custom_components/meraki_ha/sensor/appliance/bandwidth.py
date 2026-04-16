"""Bandwidth sensors for Meraki appliances."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Literal

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfDataRate
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ...entity import MerakiSensor

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from ...coordinators import MerakiMainCoordinator
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)

# --- Constants for metrics and units ---
METRIC_MAPPING: dict[str, dict[str, Any]] = {
    "sent": {
        "api_key": "sent",
        "unit": UnitOfDataRate.KILOBITS_PER_SECOND,
        "device_class": SensorDeviceClass.DATA_RATE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
    "received": {
        "api_key": "received",
        "unit": UnitOfDataRate.KILOBITS_PER_SECOND,
        "device_class": SensorDeviceClass.DATA_RATE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
}


class MerakiUplinkBandwidthSensor(MerakiSensor):
    """Representation of a Meraki uplink bandwidth sensor."""

    _device_serial: str
    _interface: str
    _metric_api_key: str
    _attr_native_unit_of_measurement: str | None

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        interface: str,
        metric: Literal["sent", "received"],
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

        if not device.serial:
            _LOGGER.error(
                "Device serial is required for uplink bandwidth sensor (Device: %s)",
                device.name,
            )
            raise ValueError(
                "Device serial is required for uplink bandwidth sensor "
                f"(Device: {device.name})"
            )
        self._device_serial = device.serial
        self._interface = interface

        metric_details = METRIC_MAPPING.get(metric)
        if not metric_details:
            _LOGGER.error(
                "Unsupported uplink bandwidth metric: %s for device %s.",
                metric,
                device.name,
            )
            raise ValueError(f"Unsupported uplink bandwidth metric: {metric}")

        self._metric_api_key = metric_details["api_key"]
        self._attr_native_unit_of_measurement = metric_details["unit"]
        self._attr_device_class = metric_details["device_class"]
        self._attr_state_class = metric_details["state_class"]

        self.entity_description = description

        self._attr_unique_id = (
            f"{self._device_serial}_{interface}_{self._metric_api_key}_bandwidth"
        )

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
        """Find and parse the metric value for a specific uplink interface."""
        for uplink in uplinks:
            if not isinstance(uplink, dict):
                continue
            if uplink.get("interface") == interface:
                # getNetworkApplianceUplinksUsageHistory returns bytes per interval
                # If timespan is 60s, it's bytes per 60s (if it's one interval)
                # Actually, Meraki returns total bytes in that interval.
                # To get bps: (bytes * 8) / seconds
                value = uplink.get(metric_api_key)
                if value is not None:
                    try:
                        # Assuming 60s interval for now as per fetcher config
                        # Conversion: bytes * 8 (bits) / 60 (seconds) / 1000 (kilobits)
                        # = value * 8 / 60000
                        return (float(value) * 8.0) / 60.0 / 1000.0
                    except (ValueError, TypeError):
                        _LOGGER.debug(
                            "Could not convert bandwidth value '%s' to float "
                            "for interface '%s'",
                            value,
                            interface,
                        )
                        return None
        return None

    @callback
    def _update_state(self) -> None:
        """Update the sensor state from the coordinator data."""
        device = self.coordinator.get_device(self._device_serial)
        if not device or not device.uplinks:
            self._attr_native_value = None
            return

        self._attr_native_value = self._get_uplink_metric_value(
            uplinks=device.uplinks,
            interface=self._interface,
            metric_api_key=self._metric_api_key,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()
