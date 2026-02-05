"""Uplink performance sensors for Meraki appliances."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN
from ..entity import MerakiEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from ..coordinator import MerakiDataUpdateCoordinator
    from ..core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiSensor(MerakiEntity, SensorEntity):
    """Base class for Meraki sensors."""


class MerakiUplinkPerformanceSensor(MerakiSensor):
    """Representation of a Meraki uplink performance sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        interface: str,
        metric: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        if not device.serial:
            raise ValueError(
                "Device serial is required for uplink performance sensor "
                f"(Device: {device.name})"
            )
        self._device_serial: str = device.serial
        self._interface = interface
        self._metric = metric
        self.entity_description = description

        # Use Home Assistant Sentence Case for names
        # Entity name will be e.g. "WAN1 Latency"
        # Since _attr_has_entity_name is True in MerakiEntity,
        # the final name will be "Device Name WAN1 Latency"

        self._attr_unique_id = f"{self._device_serial}_{interface}_{metric}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
        )
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the sensor state from the coordinator data."""
        device = self.coordinator.get_device(self._device_serial)
        if not device or not device.uplinks:
            self._attr_native_value = None
            return

        for uplink in device.uplinks:
            if uplink.get("interface") == self._interface:
                value = uplink.get(self._metric)
                if value is not None:
                    try:
                        self._attr_native_value = float(value)
                    except (ValueError, TypeError):
                        self._attr_native_value = value
                else:
                    self._attr_native_value = None
                return
        self._attr_native_value = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()
