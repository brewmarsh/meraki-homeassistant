"""Base class for Meraki MT binary sensor entities."""

from __future__ import annotations

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
        self._attr_unique_id = f"{self._device['serial']}_{entity_description.key}"
        self._attr_name = f"{self._device['name']} {entity_description.name}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device.get("model", "MT Sensor"),
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self.coordinator.data:
            return
        for device in self.coordinator.data.get("devices", []):
            if device.get("serial") == self._device.get("serial"):
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
            metric = reading.get("metric")
            if metric == self.entity_description.key:
                value = reading.get("value")
                if isinstance(value, bool):
                    return value
                if isinstance(value, str):
                    return value.lower() in ("true", "1", "on", "open")
        return None
