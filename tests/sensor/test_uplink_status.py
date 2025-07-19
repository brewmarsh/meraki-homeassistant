"""Tests for the Meraki uplink status sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.uplink_status import (
    MerakiUplinkStatusSensor,
)


async def test_meraki_uplink_status_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki uplink status sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "status": "online",
            }
        ]
    }
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    sensor = MerakiUplinkStatusSensor(coordinator, device_data)
    sensor._update_sensor_state()
    assert sensor.native_value == "Online"
