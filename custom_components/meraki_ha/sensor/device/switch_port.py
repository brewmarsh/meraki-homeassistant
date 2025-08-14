"""Sensor for Meraki switch port status."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)


class MerakiSwitchPortSensor(CoordinatorEntity[MerakiDataCoordinator], SensorEntity):
    """Representation of a Meraki switch port sensor."""

    _attr_icon = "mdi:ethernet-port"
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_data: Dict[str, Any],
        config_entry: ConfigEntry,
        port_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._port_id: str = port_data["portId"]
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device_serial}_port_{self._port_id}"
        self._attr_name = f"Port {self._port_id} Status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, self._config_entry.options),
            model=device_data.get("model"),
            manufacturer="Cisco Meraki",
            sw_version=device_data.get("firmware"),
        )
        self._update_state()

    def _get_current_port_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this port from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for device in self.coordinator.data["devices"]:
                if device.get("serial") == self._device_serial:
                    for port in device.get("ports_statuses", []):
                        if port.get("portId") == self._port_id:
                            return port
        return None

    @callback
    def _update_state(self) -> None:
        """Update the state of the sensor."""
        port_data = self._get_current_port_data()
        if port_data:
            if not port_data.get("enabled"):
                self._attr_native_value = "disabled"
            else:
                self._attr_native_value = port_data.get("status", "unknown").lower()

            self._attr_extra_state_attributes = {
                k: v for k, v in port_data.items() if k != "status"
            }
        else:
            self._attr_native_value = "unknown"
            self._attr_extra_state_attributes = {}

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_current_port_data() is not None
