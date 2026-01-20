"""
Sensor entity for representing the status of a Meraki device.

This module defines the `MerakiDeviceStatusSensor` class, which
is a Home Assistant sensor entity that displays the status (product type)
of a specific Meraki device.
"""

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name
from ...types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceStatusSensor(CoordinatorEntity, SensorEntity):
    """
    Representation of a Meraki Device Status sensor.

    This sensor displays the actual reported status of a Meraki device
    (e.g., "online", "offline", "alerting"). It uses SensorEntityDescription
    to define its core properties. The device status is fetched from the
    coordinator's data. Additional device details are provided as state attributes,
    and the icon dynamically changes based on the device model.

    The `name` property is derived from the `EntityDescription` ("Status"), and
    Home Assistant combines this with the device name because `_attr_has_entity_name`
    is True. Properties like `options`, `suggested_unit_of_measurement`,
    `suggested_display_precision`, and `last_reset` default to None behavior
    as they are not applicable or overridden by the base `SensorEntity` or
    `SensorEntityDescription` defaults for categorical sensors.
    """

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: "MerakiDevice",  # Initial device_data snapshot
        config_entry: ConfigEntry,
    ) -> None:
        """
        Initialize the Meraki Device Status sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            device_data: A dictionary containing initial information about the
                Meraki device.
            config_entry: The config entry.

        """
        super().__init__(coordinator)
        self._device_serial: str = device_data.serial  # Serial is mandatory

        # Set up unique ID
        self._attr_unique_id = f"{self._device_serial}_device_status"

        # Set device info for linking to HA device registry
        # This uses the initial device_data for static info.
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, config_entry.options),
            model=device_data.model,
            manufacturer="Cisco Meraki",
            serial_number=self._device_serial,
            sw_version=device_data.firmware,
        )

        # _attr_name is not explicitly set
        self.entity_description = SensorEntityDescription(
            key="device_status",
            name="Status",
            native_unit_of_measurement=None,  # Categorical status, no unit
            state_class=None,  # Categorical status
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

    def _get_current_device_data(self) -> MerakiDevice | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        return self.coordinator.get_device(self._device_serial)

    def _update_sensor_data(self) -> None:
        """Update sensor state and attributes from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = None
            self._attr_icon = "mdi:help-rhombus"
            return

        # Status is the primary value of this sensor
        device_status: str | None = current_device_data.status
        if isinstance(device_status, str):
            self._attr_native_value = device_status.lower()
        else:
            self._attr_native_value = "unknown"  # Default if status is not a string

        # Populate attributes from the latest device data
        self._attr_extra_state_attributes = {
            "model": current_device_data.model,
            "serial_number": current_device_data.serial,
            "firmware_version": getattr(current_device_data, "firmware", None),
            "product_type": current_device_data.product_type,
            "mac_address": current_device_data.mac,
            "lan_ip": current_device_data.lan_ip,
            "public_ip": current_device_data.public_ip,
            "wan1_ip": current_device_data.wan1_ip,
            "wan2_ip": current_device_data.wan2_ip,
            "tags": getattr(current_device_data, "tags", []),
            "network_id": current_device_data.network_id,
        }
        # Filter out None values from attributes
        self._attr_extra_state_attributes = {
            k: v for k, v in self._attr_extra_state_attributes.items() if v is not None
        }

        # If the device is an appliance, add uplink information as attributes
        if current_device_data.product_type == "appliance":
            for uplink in getattr(current_device_data, "uplinks", []):
                interface = uplink.get("interface")
                if interface is not None:
                    self._attr_extra_state_attributes[f"{interface}_status"] = (
                        uplink.get("status")
                    )
                    self._attr_extra_state_attributes[f"{interface}_ip"] = uplink.get(
                        "ip"
                    )
                    self._attr_extra_state_attributes[f"{interface}_gateway"] = (
                        uplink.get("gateway")
                    )
                    self._attr_extra_state_attributes[f"{interface}_public_ip"] = (
                        uplink.get("publicIp")
                    )
                    self._attr_extra_state_attributes[f"{interface}_dns_servers"] = (
                        uplink.get("dns")
                    )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_data()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # Check basic coordinator availability
        if not super().available:  # Checks coordinator.last_update_success
            return False
        # Check if the specific device data is available
        if self.coordinator.data and self.coordinator.data.get("devices"):
            return any(
                dev.serial == self._device_serial
                for dev in self.coordinator.data["devices"]
            )
        return False
