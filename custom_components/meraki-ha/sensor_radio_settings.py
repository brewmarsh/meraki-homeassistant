"""Sensor platform for the meraki_ha integration."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .meraki_api.wireless import get_meraki_device_wireless_radio_settings
from .meraki_api.exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


class MerakiRadioSettingsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Radio Settings sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki Radio Settings sensor."""
        super().__init__(coordinator)
        self._device = device
        _LOGGER.debug(f"Meraki: Device data: {device}")
        self._attr_name = f"{device['name']} Radio Settings"
        self._attr_unique_id = f"{device['serial']}_radio_settings"
        self._attr_icon = "mdi:wifi"
        self._attr_extra_state_attributes = {
            "model": device.get("model"),
            "serial_number": device.get("serial"),
            "firmware_version": device.get("firmware"),
        }
        self._attr_extra_state_attributes["serial_number"] = device.get("serial")
        _LOGGER.debug(f"Meraki: Radio Sensor Initialized: {self._attr_name}")

    async def async_update(self) -> None:
        """Update the sensor state."""
        _LOGGER.debug(f"Meraki: Updating sensor state for {self._attr_name}")
        try:
            radio_settings = await get_meraki_device_wireless_radio_settings(
                self.coordinator.api_key,
                self.coordinator.org_id,
                self._device["serial"],
            )
            if radio_settings and radio_settings.get("channel"):
                self._attr_native_value = radio_settings["channel"]
                self._attr_extra_state_attributes.update(radio_settings)
            else:
                self._attr_native_value = "Unavailable"
                self._attr_extra_state_attributes.update({"channel": None})
        except MerakiApiError as e:
            _LOGGER.error(f"Meraki: Error fetching radio settings: {e}")
            self._attr_native_value = "Error"
        except Exception as e:
            _LOGGER.error(f"Meraki: Unexpected error fetching radio settings: {e}")
            self._attr_native_value = "Error"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes of the sensor."""
        _LOGGER.debug(f"Meraki: Getting extra state attributes for {self._attr_name}")
        return self._attr_extra_state_attributes.copy()
