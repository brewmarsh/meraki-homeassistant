"""Base class for Meraki MT sensor entities."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class MTSensorEntityDescription(SensorEntityDescription):
    """Describes a Meraki MT sensor entity."""

    value_key: str | None = None


class MerakiMtSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki MT sensor."""

    entity_description: MTSensorEntityDescription

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: dict[str, Any],
        entity_description: MTSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
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
            name=format_device_name(self._device, self.coordinator.config_entry),
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.coordinator.data and (
            device := self.coordinator.data.devices.get(self._device["serial"])
        ):
            self._device = device
            self.async_write_ha_state()

    @property
    def native_value(self) -> float | bool | None:
        """Return the state of the sensor."""
        if (
            not self.entity_description.value_key
            or not (readings := self._device.get("readings"))
            or not isinstance(readings, list)
        ):
            return None

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                if metric_data := reading.get(self.entity_description.key):
                    if isinstance(metric_data, dict):
                        if self.entity_description.value_key == "ambient":
                            return metric_data.get("ambient", {}).get("level")
                        return metric_data.get(self.entity_description.value_key)
        return None

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
        # The sensor is available if there is a reading for its metric.
        # This prevents creating sensors for metrics that a device doesn't support.
        readings = self._device.get("readings")
        if not readings or not isinstance(readings, list):
            return False

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                return True
        return False
