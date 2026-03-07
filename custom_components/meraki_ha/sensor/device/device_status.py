"""
Sensor entity for representing the status of a Meraki device.

This module defines the `MerakiDeviceStatusSensor` class, which
is a Home Assistant sensor entity that displays the status (product type)
of a specific Meraki device.
"""

import logging
from typing import Any, cast

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback

from ...coordinators import MerakiMainCoordinator
from ...core.models.device import MerakiDevice
from ...entity import MerakiSensor
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceStatusSensor(MerakiSensor):
    """
    Representation of a Meraki Device Status sensor.

    This sensor displays the actual reported status of a Meraki device
    (e.g., "online", "offline", "alerting").
    """

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device_data: "MerakiDevice",
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Device Status sensor."""
        super().__init__(coordinator)
        self._device_serial: str = cast(str, device_data.serial)

        # Set device info for linking to HA device registry
        self._attr_device_info = resolve_device_info(device_data, config_entry)

        self.entity_description = SensorEntityDescription(
            key="device_status",
            name="Status",
            native_unit_of_measurement=None,
            state_class=None,
            device_class=SensorDeviceClass.ENUM,
            icon="mdi:help-network-outline",
        )
        self._attr_options = ["online", "offline", "alerting", "dormant", "unknown"]

        # Initial update of state and attributes
        self._update_sensor_data()

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        status_icon_map = {
            "online": "mdi:access-point-network",
            "offline": "mdi:access-point-network-off",
            "alerting": "mdi:access-point-network-off",
            "dormant": "mdi:access-point-network-off",
        }
        if isinstance(self.native_value, str):
            return status_icon_map.get(
                self.native_value.lower(), "mdi:help-network-outline"
            )
        return "mdi:help-network-outline"

    def _update_sensor_data(self) -> None:
        """Update sensor state and attributes from coordinator data."""
        # Data extraction is handled by MerakiEntity; we access it via self.coordinator.data
        if not self.coordinator.data or self._device_serial not in self.coordinator.data:
            self._attr_native_value = None
            self._attr_icon = "mdi:help-rhombus"
            return

        current_device_data = self.coordinator.data[self._device_serial]
        self._attr_native_value = self._determine_device_status(current_device_data)

        # Populate attributes from the latest device data
        self._attr_extra_state_attributes = self._get_base_device_attributes(
            current_device_data
        )

        # If the device is an appliance, add uplink information as attributes
        if getattr(current_device_data, "product_type", None) == "appliance":
            self._attr_extra_state_attributes.update(
                self._get_appliance_uplink_attributes(current_device_data)
            )

    def _determine_device_status(self, device_data: MerakiDevice) -> str:
        """Determine the device status with fallback logic."""
        device_status: str | None = getattr(device_data, "status", None)

        native_value = "unknown"
        if isinstance(device_status, str) and device_status.lower() not in ["", "unknown"]:
            native_value = device_status.lower()

        # Fallback to composite state from uplinks
        if native_value == "unknown" and hasattr(device_data, "uplinks") and device_data.uplinks:
            if any(u.get("status") == "active" for u in device_data.uplinks):
                native_value = "online"
            elif all(u.get("status") == "failed" for u in device_data.uplinks):
                native_value = "offline"

        return native_value

    def _get_base_device_attributes(self, device_data: MerakiDevice) -> dict[str, Any]:
        """Collect base attributes for the device."""
        attrs = {
            "model": getattr(device_data, "model", None),
            "serial_number": getattr(device_data, "serial", None),
            "firmware_version": getattr(device_data, "firmware", None),
            "product_type": getattr(device_data, "product_type", None),
            "mac_address": getattr(device_data, "mac", None),
            "lan_ip": getattr(device_data, "lan_ip", None),
            "public_ip": getattr(device_data, "public_ip", None),
            "wan1_ip": getattr(device_data, "wan1_ip", None),
            "wan2_ip": getattr(device_data, "wan2_ip", None),
            "tags": getattr(device_data, "tags", None),
            "network_id": getattr(device_data, "network_id", None),
        }
        return {k: v for k, v in attrs.items() if v is not None}

    def _get_appliance_uplink_attributes(self, device_data: MerakiDevice) -> dict[str, Any]:
        """Collect appliance-specific uplink attributes."""
        attrs: dict[str, Any] = {}
        statuses = getattr(device_data, "appliance_uplink_statuses", [])
        for uplink in statuses:
            interface = uplink.get("interface")
            if interface is not None:
                attrs.update({
                    f"{interface}_status": uplink.get("status"),
                    f"{interface}_ip": uplink.get("ip"),
                    f"{interface}_gateway": uplink.get("gateway"),
                    f"{interface}_public_ip": uplink.get("publicIp"),
                    f"{interface}_dns_servers": uplink.get("dns"),
                })
        return attrs

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Use the base class logic to verify availability and call update methods
        super()._handle_coordinator_update()