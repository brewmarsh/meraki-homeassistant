"""Sensor entity representing the band selection of a Meraki SSID."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from ...core.coordinators.network import MerakiNetworkCoordinator
from ...const import DOMAIN, CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
from ...helpers.entity_helpers import format_entity_name

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDBandSelectionSensor(
    CoordinatorEntity[MerakiNetworkCoordinator], SensorEntity
):
    """Representation of a Meraki SSID Band Selection sensor."""

    _attr_icon = "mdi:wifi-strength-4"

    def __init__(
        self,
        coordinator: MerakiNetworkCoordinator,
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._ssid_data = ssid_data

        ssid_name = self._ssid_data.get("name", "Unknown SSID")
        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            f"{ssid_name} Band Selection", "sensor", name_format, apply_format=False
        )
        self._attr_unique_id = f"{self._ssid_data['unique_id']}_band_selection"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._ssid_data["unique_id"])},
            name=ssid_name,
            model="Wireless SSID",
            manufacturer="Cisco Meraki",
        )
        self._update_sensor_state()

    def _update_sensor_state(self) -> None:
        """Update the sensor's state based on coordinator data for this SSID."""
        current_ssid_data = self.coordinator.data.get(self._ssid_data["unique_id"])

        if current_ssid_data:
            self._ssid_data = current_ssid_data
            self._attr_native_value = self._ssid_data.get("bandSelection")
        else:
            self._attr_native_value = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_state()
        self.async_write_ha_state()
