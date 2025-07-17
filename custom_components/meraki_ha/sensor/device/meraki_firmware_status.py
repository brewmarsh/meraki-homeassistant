"""Sensor for Meraki Device Firmware Status."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.meraki_haconst import DOMAIN
from custom_components.meraki_hacoordinators import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiFirmwareStatusSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Device Firmware Status Sensor."""

    _attr_icon = "mdi:package-up"  # Icon suggesting updates or package version
    _attr_has_entity_name = True  # Home Assistant will prepend the device name
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["up-to-date", "out-of-date", "unknown"]

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._attr_unique_id = f"{self._device_serial}_firmware_status"
        # self.entity_id = f"sensor.{DOMAIN}_{self._device_serial}_firmware_status" # Let HA generate

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)}
            # No other fields like name, model, manufacturer, sw_version.
            # These should be inherited from the device entry already created by MerakiDataUpdateCoordinator.
        )
        self._attr_name = "Firmware Status"  # Suffix to device name

        self._attr_extra_state_attributes: Dict[str, Any] = {}
        # Initialize state
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        current_device_data: Optional[Dict[str, Any]] = None
        if (
            self.coordinator.data
            and self.coordinator.data.get("devices")
            and isinstance(self.coordinator.data["devices"], list)
        ):
            for device in self.coordinator.data["devices"]:
                if device.get("serial") == self._device_serial:
                    current_device_data = device
                    break

        if not current_device_data:
            self._attr_native_value = "unknown"
            self._attr_extra_state_attributes = {}
            # _LOGGER.debug( # Covered by available property
            #     "Device %s not found in coordinator data for firmware status sensor.",
            #     self._device_serial,
            # ) # Removed
            return

        firmware_up_to_date = current_device_data.get("firmware_up_to_date")
        if firmware_up_to_date is True:
            self._attr_native_value = "up-to-date"
        elif firmware_up_to_date is False:
            self._attr_native_value = "out-of-date"
        else:
            self._attr_native_value = "unknown"


        attributes = {
            "current_firmware_version": current_device_data.get("firmware"),
            "firmware_up_to_date": current_device_data.get("firmware_up_to_date", False),
            "latest_available_firmware_version": current_device_data.get("latest_firmware_version", "N/A"),
            "model": current_device_data.get("model"),
        }

        self._attr_extra_state_attributes = {
            k: v for k, v in attributes.items() if v is not None
        }

        # _LOGGER.debug(
        #     "Firmware Status Sensor update for %s: state=%s, attributes=%s",
        #     self._device_serial,
        #     self._attr_native_value,
        #     self._attr_extra_state_attributes,
        # ) # Removed

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not super().available:
            return False
        if not self.coordinator.data or not self.coordinator.data.get("devices"):
            return False
        # Check if the specific device data is available
        for device in self.coordinator.data["devices"]:
            if device.get("serial") == self._device_serial:
                return True
        return False
