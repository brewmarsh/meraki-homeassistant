"""Sensor entity for representing the status of a Meraki device.

This module defines the `MerakiDeviceStatusSensor` class, which
is a Home Assistant sensor entity that displays the status (product type)
of a specific Meraki device.
"""

import logging
from typing import Any, Dict, Optional  # Added Optional
from datetime import datetime # Added import

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription # Updated import

# Added callback for coordinator updates
from homeassistant.core import callback
# from homeassistant.helpers.entity import EntityDescription # No longer needed
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
from ..coordinators import MerakiDataUpdateCoordinator
from ..const import DOMAIN  # For device_info identifiers

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceStatusSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Device Status sensor.

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

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: Dict[str, Any],  # Initial device_data snapshot
    ) -> None:
        """Initialize the Meraki Device Status sensor.

        Args:
            coordinator: The data update coordinator.
            device_data: A dictionary containing initial information about the Meraki device
                         (e.g., name, serial, model, firmware, productType).
        """
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]  # Serial is mandatory

        # Set up unique ID
        self._attr_unique_id = f"{self._device_serial}_device_status"

        # Set device info for linking to HA device registry
        # This uses the initial device_data for static info.
        device_name_for_registry = device_data.get("name") or self._device_serial
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)}
            # No other fields like name, model, manufacturer, sw_version.
            # These should be inherited from the device entry already created by MerakiDataUpdateCoordinator.
        )

        # Name of the sensor itself (e.g., "Device Name Status")
        # self.entity_id will be sensor.device_name_status
        # _attr_name is not explicitly set, letting has_entity_name and device name work.
        # If has_entity_name is False or more control is needed:
        # self._attr_name = f"{device_name_for_registry} Status" # This line should be removed if present

        self.entity_description = SensorEntityDescription(
            key="device_status",
            name="Status",
            native_unit_of_measurement=None, # Categorical status, no unit
            state_class=None, # Categorical status
        )
        # Properties like state_class and native_unit_of_measurement are now set by SensorEntityDescription.
        # Other properties (options, suggested_unit_of_measurement, suggested_display_precision, last_reset)
        # are intentionally not overridden here and will default to None or appropriate base class behavior.

        # Initial update of state and attributes
        self._update_sensor_data()
        _LOGGER.debug(
            "MerakiDeviceStatusSensor Initialized for %s (Serial: %s)",
            device_name_for_registry,
            self._device_serial,
        )

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        _LOGGER.debug(
            "Device data for serial '%s' not found in coordinator for sensor '%s'.",
            self._device_serial,
            self.unique_id,
        )
        return None

    def _update_sensor_data(self) -> None:
        """Update sensor state (native_value, icon) and attributes from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data: # Should be primarily handled by the `available` property
            self._attr_native_value = None
            self._attr_icon = "mdi:help-rhombus"
            # Consider clearing extra_state_attributes if device becomes unavailable for a long time
            # self._attr_extra_state_attributes = {}
            return

        # Status is the primary value of this sensor
        device_status: Optional[str] = current_device_data.get("status")
        if isinstance(device_status, str):
            self._attr_native_value = device_status.lower()
        else:
            self._attr_native_value = "unknown"  # Default if status is not a string

        # Icon logic based on model
        model: Optional[str] = current_device_data.get("model")
        if isinstance(model, str):
            model_upper = model.upper()
            if model_upper.startswith("MR"):  # Wireless AP
                self._attr_icon = "mdi:access-point-network"
            elif model_upper.startswith("MX"):  # Security Appliance
                self._attr_icon = "mdi:router-network"
            elif model_upper.startswith("MS"):  # Switch
                self._attr_icon = "mdi:switch"
            elif model_upper.startswith("MV"):  # Camera
                self._attr_icon = "mdi:cctv"
            elif model_upper.startswith("MT"):  # Sensor
                self._attr_icon = "mdi:thermometer-lines"
            else:  # Default for other models
                self._attr_icon = "mdi:help-network-outline"
        else:
            self._attr_icon = (
                "mdi:help-network-outline"  # Default if model is not a string
            )

        # Populate attributes from the latest device data
        self._attr_extra_state_attributes = {
            "model": current_device_data.get("model"),
            "serial_number": current_device_data.get(
                "serial"
            ),  # Should match self._device_serial
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
            k: v for k, v in self._attr_extra_state_attributes.items() if v is not None
        }

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
        # Check if the specific device data is available in the coordinator's current data
        if self.coordinator.data and self.coordinator.data.get("devices"):
            return any(
                dev.get("serial") == self._device_serial
                for dev in self.coordinator.data["devices"]
            )
        return False

    # @property
    # def options(self) -> list[str] | None:
    #     return None
    #
    # @property
    # def suggested_unit_of_measurement(self) -> str | None:
    #     return None
    #
    # @property
    # def suggested_display_precision(self) -> int | None:
    #     return None
    #
    # @property
    # def last_reset(self) -> datetime | None:
    #     return None
