"""Sensor for Meraki wireless device radio settings."""

import logging
from typing import Any, Dict

from ....core.entities.device import MerakiDeviceEntity

_LOGGER = logging.getLogger(__name__)

STATE_UNAVAILABLE = "unavailable"


class MerakiRadioSettingsSensor(MerakiDeviceEntity):
    """Representation of a Meraki Radio Settings Sensor."""

    _attr_icon = "mdi:radio-tower"

    def __init__(
        self,
        coordinator,
        device_serial: str,
    ) -> None:
        """Initialize the radio settings sensor."""
        super().__init__(
            coordinator=coordinator,
            device_serial=device_serial,
            name="Radio Settings",
            unique_id_suffix="radio_settings",
        )

    @property
    def native_value(self) -> str:
        """Return the radio status."""
        return self.device_data.get("radio_settings", {}).get(
            "status", STATE_UNAVAILABLE
        )

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        radio_settings = self.device_data.get("radio_settings", {})
        radio_24ghz = radio_settings.get("2.4", {})
        radio_5ghz = radio_settings.get("5", {})

        return {
            "2_4ghz_channel": radio_24ghz.get("channel"),
            "2_4ghz_power": radio_24ghz.get("power"),
            "5ghz_channel": radio_5ghz.get("channel"),
            "5ghz_power": radio_5ghz.get("power"),
            "network_id": self.device_data.get("networkId"),
            "tags": self.device_data.get("tags", []),
        }
