"""Sensor for Meraki wireless device radio settings."""

import logging
from typing import Any, Dict

from ....entities import MerakiDeviceEntity

_LOGGER = logging.getLogger(__name__)

STATE_UNAVAILABLE = "unavailable"


class MerakiRadioSettingsSensor(MerakiDeviceEntity):
    """Representation of a Meraki Radio Settings Sensor."""

    _attr_icon = "mdi:radio-tower"

    def __init__(
        self,
        coordinator,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the radio settings sensor."""
        super().__init__(
            coordinator=coordinator,
            device_data=device_data,
            name="Radio Settings",
            unique_id_suffix="radio_settings",
        )
        self._update_sensor_state()

    def _update_sensor_state(self) -> None:
        """Update sensor state and attributes from coordinator data."""
        current_device_data = self._get_device_data()

        if not current_device_data:
            self._attr_native_value = STATE_UNAVAILABLE
            self._attr_extra_state_attributes = {}
            return

        radio_settings = current_device_data.get("radio_settings")
        if not radio_settings:
            _LOGGER.warning(
                "Radio settings for device '%s' (Serial: %s) not found in coordinator data. Setting state to unavailable.",
                current_device_data.get("name", "Unknown"),
                self._device_serial,
            )
            self._attr_native_value = STATE_UNAVAILABLE
            self._attr_extra_state_attributes = {}
            return

        self._attr_native_value = radio_settings.get("status", STATE_UNAVAILABLE)

        # Create attributes with both 2.4GHz and 5GHz radio settings
        radio_24ghz = radio_settings.get("24", {})
        radio_5ghz = radio_settings.get("5", {})

        self._attr_extra_state_attributes = {
            "2_4ghz_channel": radio_24ghz.get("channel", 0),
            "2_4ghz_power": radio_24ghz.get("power", 0),
            "5ghz_channel": radio_5ghz.get("channel", 0),
            "5ghz_power": radio_5ghz.get("power", 0),
            "network_id": current_device_data.get("networkId"),
            "tags": current_device_data.get("tags", []),
        }
