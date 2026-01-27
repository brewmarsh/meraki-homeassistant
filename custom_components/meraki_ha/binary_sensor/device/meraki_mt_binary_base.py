"""Base class for Meraki MT binary sensor entities."""

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiMtBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Meraki MT binary sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: dict[str, Any],
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._device = device
        self.entity_description = entity_description
        self._attr_unique_id = f"{self._device['serial']}_{self.entity_description.key}"
        self._attr_name = f"{self._device['name']} {self.entity_description.name}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device["serial"] == self._device["serial"]:
                self._device = device
                self.async_write_ha_state()
                return

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        readings = self._device.get("readings")
        if not readings or not isinstance(readings, list):
            return None

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                metric_data = reading.get(self.entity_description.key)

                if isinstance(metric_data, dict):
                    # Map metric to the key holding its value
                    key_map = {
                        "water": "present",
                        "door": "open",
                    }
                    value_key = key_map.get(self.entity_description.key)
                    if value_key:
                        val = metric_data.get(value_key)
                        if isinstance(val, bool):
                            return val
        return None

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
        # The sensor is available if there is a reading for its metric.
        readings = self._device.get("readings")
        if not readings or not isinstance(readings, list):
            return False

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                return True
        return False
