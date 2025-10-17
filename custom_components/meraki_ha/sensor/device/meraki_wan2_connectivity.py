"""Sensor for Meraki WAN2 Connectivity."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)

STATE_CONNECTED = "Connected"
STATE_DISCONNECTED = "Disconnected"


class MerakiWAN2ConnectivitySensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki WAN2 Connectivity Sensor."""

    _attr_icon = "mdi:wan"
    _attr_has_entity_name = True
    _attr_device_class = "connectivity"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: Dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_wan2_connectivity"
        self._attr_name = "WAN 2 Connectivity"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, self._config_entry.options),
            model=device_data.get("model"),
            manufacturer="Meraki",
        )
        self._update_state()

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for device in self.coordinator.data["devices"]:
                if device.get("serial") == self._device_serial:
                    return device
        return None

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = STATE_DISCONNECTED
            self._attr_extra_state_attributes = {}
            return

        wan2_ip = current_device_data.get("wan2Ip")
        device_status = str(current_device_data.get("status", "")).lower()

        if wan2_ip and device_status == "online":
            self._attr_native_value = STATE_CONNECTED
        else:
            self._attr_native_value = STATE_DISCONNECTED

        self._attr_extra_state_attributes = {
            "wan2_ip_address": wan2_ip if wan2_ip else "N/A"
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_current_device_data() is not None
