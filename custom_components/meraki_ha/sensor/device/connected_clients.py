"""Sensor entity for monitoring connected clients on a Meraki device.

This module defines the `MerakiConnectedClientsSensor` class, which
represents a sensor in Home Assistant that displays the number of clients
currently connected to a specific Meraki device (typically an access point).
"""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
from ...core.coordinators.device import MerakiDeviceCoordinator
from ...const import DOMAIN, CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
from ...helpers.entity_helpers import format_entity_name

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceConnectedClientsSensor(
    CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity
):
    """Representation of a Meraki Connected Clients sensor.

    This sensor entity monitors the number of clients connected to a
    specific Meraki device, such as a wireless access point. The data
    is sourced from the `MerakiDataUpdateCoordinator`.

    Attributes:
        _attr_name: The name of the sensor.
        _attr_unique_id: The unique ID of the sensor.
        _attr_icon: The icon to use for the sensor in the frontend.
        _attr_native_unit_of_measurement: The unit of measurement for the sensor.
        _attr_state_class: The state class of the sensor (measurement).
        _device_info_data: Raw dictionary data for the associated Meraki device.
    """

    _attr_icon = "mdi:account-network"  # Standard icon for network clients
    _attr_native_unit_of_measurement = "clients"
    # Indicates a numeric value that's not a total
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        # Data for the Meraki device this sensor is for
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki Connected Clients sensor.

        Args:
            coordinator: The data update coordinator.
            device_data: A dictionary containing information about the Meraki device
                         (e.g., name, serial, model, firmware).
        """
        super().__init__(coordinator)
        self._device_info_data: Dict[str, Any] = device_data
        device_name = self._device_info_data.get(
            "name", self._device_info_data.get("serial", "Unknown Device")
        )
        device_serial = self._device_info_data.get(
            "serial", ""
        )  # Should always have serial

        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            f"{device_name} Connected Clients", "sensor", name_format
        )
        self._attr_unique_id = f"{device_serial}_connected_clients"

        # Set initial state
        self._update_sensor_state()

    def _get_client_count(self) -> Optional[int]:
        """Retrieve the client count for this device from coordinator data.

        Searches the coordinator's device list for this sensor's device
        and returns the 'connected_clients_count' value.

        Returns:
            The number of connected clients as an integer, or 0 if data is
            unavailable or the device is not found. Returns None if the
            coordinator data itself is unavailable.
        """
        if self.coordinator.data is None or "devices" not in self.coordinator.data:
            _LOGGER.warning(
                "Coordinator data or devices list is unavailable for %s.",
                self.unique_id,
            )
            return None  # Or 0 if preferred for unavailable data source

        device_serial = self._device_info_data.get("serial")
        found_device_data: Optional[Dict[str, Any]] = None
        for dev_data in self.coordinator.data["devices"]:
            if dev_data.get("serial") == device_serial:
                found_device_data = dev_data
                break

        if found_device_data:
            # The key for connected clients count might be 'connected_clients' or 'connected_clients_count'
            # Based on device_setup.py, it was 'connected_clients_count' after processing.
            # Original code here used 'connected_clients'. Let's try to be
            # robust.
            client_count = found_device_data.get("connected_clients_count")
            if client_count is None:
                client_count = found_device_data.get("connected_clients")

            if client_count is None:
                return 0
            if isinstance(client_count, int):
                return client_count

            _LOGGER.warning(
                "Connected clients data for device '%s' (Serial: %s) is not an integer: %s. Defaulting to 0.",
                self._device_info_data.get("name", "N/A"),
                device_serial,
                client_count,
            )
            return 0  # Default if data is malformed
        else:
            _LOGGER.warning(
                "Device data not found in coordinator for serial '%s' (sensor: %s). Defaulting client count to 0.",
                device_serial,
                self.unique_id,
            )
            return 0  # Default if device not found in update

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        This method is called by the CoordinatorEntity base class when new data
        is available from the coordinator. It updates the sensor's state.
        """
        self._update_sensor_state()
        self.async_write_ha_state()

    def _update_sensor_state(self) -> None:
        """Update the native value of the sensor based on coordinator data."""
        self._attr_native_value = self._get_client_count()

    # The native_value property is now handled by _attr_native_value,
    # set by _update_sensor_state during initialization and coordinator updates.
    # Explicit property definition can be removed if SensorEntity handles _attr_native_value correctly.
    # @property
    # def native_value(self) -> Optional[int]:
    #     """Return the state of the sensor (number of connected clients)."""
    #     return self._attr_native_value

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for linking this entity to the device registry.

        This links the sensor to the physical Meraki device it represents.
        """
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_info_data["serial"])}
            # No other fields like name, model, manufacturer, sw_version.
            # These should be inherited from the device entry already created by MerakiDataUpdateCoordinator.
        )

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return additional state attributes for the sensor.

        These attributes provide more context about the device the sensor
        is associated with, such as its model, serial number, and firmware version.
        """
        # The original code copied from self._attr_extra_state_attributes.
        # It's generally better to construct this dynamically or ensure it's updated
        # if device info can change (though for serial, model it's unlikely).
        attrs: Dict[str, Any] = {
            "device_name": self._device_info_data.get("name"),
            "model": self._device_info_data.get("model"),
            "serial_number": self._device_info_data.get("serial"),
            "firmware_version": self._device_info_data.get("firmware"),
            # Example of another useful attribute
            "lan_ip": self._device_info_data.get("lanIp"),
            "mac_address": self._device_info_data.get("mac"),
        }
        # Filter out None values to keep attributes clean
        return {k: v for k, v in attrs.items() if v is not None}
