"""Tests for the Meraki radio settings sensor."""
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.radio_settings import (
    MerakiRadioSettingsSensor,
)


async def test_meraki_radio_settings_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki radio settings sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "radio_settings": {"band": "2.4", "channel": 1, "power": 10},
            }
        ]
    }
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    sensor = MerakiRadioSettingsSensor(coordinator, device_data)
    sensor._update_sensor_state()
    assert sensor.native_value == "1"
