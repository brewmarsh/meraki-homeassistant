"""Sensor entity for representing the status of a Meraki device.

This module defines the `MerakiDeviceStatusSensor` class, which
is a Home Assistant sensor entity that displays the status (product type)
of a specific Meraki device.
"""
import logging
from typing import Any, Dict, Optional # Added Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback # Added callback for coordinator updates
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
from ..coordinators import MerakiDataUpdateCoordinator
from ..const import DOMAIN # For device_info identifiers

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceStatusSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Device Status sensor.

    This sensor displays the product type of the Meraki device as its state.
    It also provides additional device details as state attributes and an
    icon based on the device model.

    Attributes:
        _attr_name: The name of the sensor.
        _attr_unique_id: The unique ID of the sensor.
        _device_info_data: Raw dictionary data for the associated Meraki device.
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: Dict[str, Any], # Data for the Meraki device this sensor is for
    ) -> None:
        """Initialize the Meraki Device Status sensor.

        Args:
            coordinator: The data update coordinator.
            device_data: A dictionary containing information about the Meraki device
                         (e.g., name, serial, model, firmware, productType).
        """
        super().__init__(coordinator)
        self._device_info_data: Dict[str, Any] = device_data
        device_name = self._device_info_data.get("name", self._device_info_data.get("serial", "Unknown Device"))
        device_serial = self._device_info_data.get("serial", "")

        self._attr_name = f"{device_name} Status"
        self._attr_unique_id = f"{device_serial}_device_status" # Ensure consistency, e.g. all lowercase with _
        
        # Set initial state and icon
        self._update_sensor_state_and_icon()
        _LOGGER.debug("Meraki Device Status Sensor Initialized: %s", self._attr_name)


    def _update_sensor_state_and_icon(self) -> None:
        current_device_data: Optional[Dict[str, Any]] = None
        # Ensure device_serial is defined here, e.g.,
        device_serial = self._device_info_data.get("serial")

        if self.coordinator.data and "devices" in self.coordinator.data:
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == device_serial:
                    current_device_data = dev_data
                    break
        
        if not current_device_data:
            _LOGGER.warning(
                "MERAKI_DEBUG_STATUS: Device data for serial '%s' not found in coordinator for sensor '%s'. Status will be unknown.", # Added prefix
                device_serial,
                self.unique_id,
            )
            self._attr_native_value = "unknown"
            self._attr_icon = "mdi:help-rhombus"
            return

        # This is the critical log line to ensure:
        _LOGGER.debug(
            "MERAKI_DEBUG_STATUS: Device %s raw status from coordinator data: %s (type: %s)",
            device_serial,
            current_device_data.get("status"),
            type(current_device_data.get("status")).__name__,
        )

        device_status: Optional[str] = current_device_data.get("status")
        if isinstance(device_status, str):
            self._attr_native_value = device_status.lower()
        else:
            self._attr_native_value = "unknown"

        product_type: Optional[str] = current_device_data.get("productType") # Keep for attributes

        model: Optional[str] = current_device_data.get("model")
        if isinstance(model, str):
            model_upper = model.upper()
            if model_upper.startswith("MR"):
                self._attr_icon = "mdi:access-point-network"
            elif model_upper.startswith("MX"):
                self._attr_icon = "mdi:router-network"
            elif model_upper.startswith("MS"):
                self._attr_icon = "mdi:switch"
            elif model_upper.startswith("MV"):
                self._attr_icon = "mdi:cctv"
            elif model_upper.startswith("MT"):
                self._attr_icon = "mdi:thermometer-lines"
            else:
                self._attr_icon = "mdi:help-network-outline"
        else:
            self._attr_icon = "mdi:help-network-outline"

        self._attr_extra_state_attributes = {
            "model": current_device_data.get("model"),
            "serial_number": current_device_data.get("serial"),
            "firmware_version": current_device_data.get("firmware"),
            "product_type": product_type,
            "mac_address": current_device_data.get("mac"),
            "lan_ip": current_device_data.get("lanIp"),
            "tags": current_device_data.get("tags", []),
            "network_id": current_device_data.get("networkId"),
        }
        self._attr_extra_state_attributes = {
            k: v for k, v in self._attr_extra_state_attributes.items() if v is not None
        }


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        This method is called by the CoordinatorEntity base class when new data
        is available from the coordinator. It updates the sensor's state and icon.
        """
        self._update_sensor_state_and_icon()
        self.async_write_ha_state()

    # native_value and icon properties are now managed by _attr_native_value and _attr_icon,
    # set by _update_sensor_state_and_icon.

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for linking this entity to the device registry.

        This links the sensor to the physical Meraki device it represents.
        """
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_info_data["serial"])},
            name=str(self._device_info_data.get("name", self._device_info_data["serial"])),
            manufacturer="Cisco Meraki",
            model=str(self._device_info_data.get("model", "Unknown")),
            sw_version=str(self._device_info_data.get("firmware", "")),
        )

    # extra_state_attributes is now managed by _attr_extra_state_attributes,
    # set by _update_sensor_state_and_icon.
