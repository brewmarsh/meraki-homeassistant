"""
Sensor entity for representing the status of a Meraki device.

This module defines the `MerakiDeviceStatusSensor` class, which
is a Home Assistant sensor entity that displays the status (product type)
of a specific Meraki device.
"""

import logging
from collections.abc import Mapping
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceStatusSensor(
    CoordinatorEntity,
    SensorEntity,
    RestoreEntity,  # type: ignore[type-arg]
):
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

    Uses RestoreEntity to preserve state across Home Assistant restarts.
    """

    coordinator: MerakiDataCoordinator
    _attr_has_entity_name = True
    _attr_native_value: str | None = None

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: Mapping[str, Any],  # Initial device_data snapshot
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
        self._device_serial: str = device_data["serial"]  # Serial is mandatory

        # Set up unique ID
        self._attr_unique_id = f"{self._device_serial}_device_status"

        # Set device info for linking to HA device registry
        # This uses the initial device_data for static info.
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, config_entry.options),
            model=device_data.get("model"),
            manufacturer="Cisco Meraki",
            serial_number=self._device_serial,
            sw_version=device_data.get("firmware"),
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

    async def async_added_to_hass(self) -> None:
        """Restore state when entity is added to HA."""
        await super().async_added_to_hass()

        # Restore previous state on restart if no fresh data
        if self._attr_native_value is None:
            if (last_state := await self.async_get_last_state()) is not None:
                self._attr_native_value = last_state.state
                if last_state.attributes:
                    self._attr_extra_state_attributes = dict(last_state.attributes)

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
            return status_icon_map.get(self.native_value, "mdi:help-network-outline")
        return "mdi:help-network-outline"

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        return None

    def _update_sensor_data(self) -> None:
        """Update sensor state and attributes from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = None
            self._attr_icon = "mdi:help-rhombus"
            return

        # Status is the primary value of this sensor
        device_status: str | None = current_device_data.get("status")
        if isinstance(device_status, str):
            self._attr_native_value = device_status.lower()
        else:
            self._attr_native_value = "unknown"  # Default if status is not a string

        # Populate attributes from the latest device data
        attributes = {
            "model": current_device_data.get("model"),
            "serial_number": current_device_data.get("serial"),
            "firmware_version": current_device_data.get("firmware"),
            "product_type": current_device_data.get("productType"),
            "mac_address": current_device_data.get("mac"),
            "lan_ip": current_device_data.get("lanIp"),
            "public_ip": current_device_data.get("publicIp"),
            "wan1_ip": current_device_data.get("wan1Ip"),
            "wan2_ip": current_device_data.get("wan2Ip"),
            "tags": current_device_data.get("tags", []),
            "network_id": current_device_data.get("networkId"),
        }
        # Filter out None values from attributes
        self._attr_extra_state_attributes = {
            k: v for k, v in attributes.items() if v is not None
        }

        # Add coordinator update timestamp
        if self.coordinator.last_successful_update:
            self._attr_extra_state_attributes["last_meraki_update"] = (
                self.coordinator.last_successful_update.isoformat()
            )

        # If the device is an appliance, add uplink information as attributes
        if current_device_data.get("productType") == "appliance":
            for uplink in current_device_data.get("uplinks", []):
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
                dev.get("serial") == self._device_serial
                for dev in self.coordinator.data["devices"]
            )
        return False
