"""Sensors for Meraki wireless radio settings."""

from __future__ import annotations

import logging
from dataclasses import asdict
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback

from ...coordinators import MerakiMainCoordinator
from ...entity import MerakiSensor
from ...helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ...core.models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiWirelessRadioSensor(MerakiSensor):
    """Sensor for Meraki wireless radio settings."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        device_data: MerakiDevice,
        config_entry: ConfigEntry,
        description: SensorEntityDescription,
        band_key: str,
        setting_key: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_serial: str | None = device_data.serial
        self._config_entry = config_entry
        self.entity_description = description
        self._band_key = band_key
        self._setting_key = setting_key

        self._attr_device_info = resolve_device_info(
            entity_data=asdict(device_data),
            config_entry=self._config_entry,
        )
        self._update_state()

    def _get_current_device_data(self) -> MerakiDevice | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self._device_serial:
            return self.coordinator.get_device(self._device_serial)
        return None

    @callback
    def _update_state(self) -> None:
        """Update the native value of the sensor based on coordinator data."""
        device = self._get_current_device_data()
        if not device or not device.wireless_radio_settings:
            self._attr_native_value = None
            return

        settings = device.wireless_radio_settings
        band_settings = settings.get(self._band_key)
        if isinstance(band_settings, dict):
            self._attr_native_value = band_settings.get(self._setting_key)
        else:
            self._attr_native_value = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._get_current_device_data() is not None
