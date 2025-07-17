"""Sensor for Meraki WAN1 Connectivity."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.meraki_haconst import DOMAIN
from custom_components.meraki_hacoordinators import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

STATE_CONNECTED = "Connected"
STATE_DISCONNECTED = "Disconnected"
STATE_UNKNOWN = "Unknown"


class MerakiWAN1ConnectivitySensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki WAN1 Connectivity Sensor."""

    _attr_icon = "mdi:wan"
    _attr_has_entity_name = True  # Home Assistant will prepend the device name
    _attr_device_class = "connectivity"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._attr_unique_id = f"{self._device_serial}_wan1_connectivity"
        # self.entity_id = f"sensor.{DOMAIN}_{self._device_serial}_wan1_connectivity" # Let HA generate

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)}
            # No other fields like name, model, manufacturer, sw_version.
            # These should be inherited from the device entry already created by MerakiDataUpdateCoordinator.
        )
        self._attr_name = "WAN 1 Connectivity"  # Suffix to device name

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
            self._attr_native_value = STATE_UNKNOWN
            self._attr_extra_state_attributes = {}
            _LOGGER.debug(
                "Device %s not found in coordinator data for WAN1 connectivity sensor.",
                self._device_serial,
            )
            return

        wan1_ip = current_device_data.get("wan1Ip")
        # Device status is usually 'online', 'offline', 'dormant', etc.
        device_status = str(current_device_data.get("status", "")).lower()

        if wan1_ip and device_status == "online":
            self._attr_native_value = STATE_CONNECTED
        else:
            self._attr_native_value = STATE_DISCONNECTED

        self._attr_extra_state_attributes = {
            "wan1_ip_address": wan1_ip if wan1_ip else "N/A"
        }
        # _LOGGER.debug(
        #     "WAN1 Sensor update for %s: wan1_ip=%s, device_status=%s, state=%s",
        #     self._device_serial,
        #     wan1_ip,
        #     device_status,
        #     self._attr_native_value,
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
