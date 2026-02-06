"""Sensors for Meraki device network settings."""

from __future__ import annotations

import logging
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback

from ...coordinator import MerakiDataUpdateCoordinator
from ...entity import MerakiEntity
from ...helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceUplinkBaseSensor(MerakiEntity, SensorEntity):
    """Base class for Meraki Device Uplink sensors."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
        interface: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str | None = device_data.serial
        self._config_entry = config_entry
        self._interface = interface

        self._attr_device_info = resolve_device_info(
            entity_data=asdict(device_data),
            config_entry=self._config_entry,
        )

    def _get_uplink_data(self) -> dict[str, Any] | None:
        """Retrieve the latest uplink data from the coordinator."""
        device = self.coordinator.get_device(self._device_serial)
        if device and device.uplinks:
            for uplink in device.uplinks:
                if uplink.get("interface") == self._interface:
                    return uplink
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_uplink_data() is not None


class MerakiDeviceIPSensor(MerakiDeviceUplinkBaseSensor):
    """Sensor for Meraki device IP address."""

    _attr_icon = "mdi:ip-network"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
        interface: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_data, config_entry, interface)
        self._attr_unique_id = f"{self._device_serial}_{interface}_ip"
        self._attr_name = f"{interface.upper()} IP"
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the sensor state."""
        uplink_data = self._get_uplink_data()
        if uplink_data:
            self._attr_native_value = uplink_data.get("ip")
        else:
            self._attr_native_value = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()


class MerakiDeviceGatewaySensor(MerakiDeviceUplinkBaseSensor):
    """Sensor for Meraki device Gateway address."""

    _attr_icon = "mdi:gateway"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
        interface: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_data, config_entry, interface)
        self._attr_unique_id = f"{self._device_serial}_{interface}_gateway"
        self._attr_name = f"{interface.upper()} Gateway"
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the sensor state."""
        uplink_data = self._get_uplink_data()
        if uplink_data:
            self._attr_native_value = uplink_data.get("gateway")
        else:
            self._attr_native_value = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()
