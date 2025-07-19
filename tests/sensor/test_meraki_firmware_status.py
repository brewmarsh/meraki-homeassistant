"""Tests for the Meraki firmware status sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.meraki_firmware_status import (
    MerakiFirmwareStatusSensor,
)


async def test_meraki_firmware_status_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki firmware status sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "firmware_up_to_date": True,
            }
        ]
    }
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    sensor = MerakiFirmwareStatusSensor(coordinator, device_data)
    sensor._update_state()
    assert sensor.native_value == "up-to-date"
