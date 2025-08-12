"""Tests for the Meraki WAN2 connectivity sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.device.meraki_wan2_connectivity import (
    MerakiWAN2ConnectivitySensor,
)


async def test_meraki_wan2_connectivity_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki WAN2 connectivity sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "wan2Ip": "1.2.3.4",
                "status": "online",
            }
        ]
    }
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    config_entry = MagicMock()
    config_entry.options = {}
    sensor = MerakiWAN2ConnectivitySensor(coordinator, device_data, config_entry)
    sensor._update_state()
    assert sensor.native_value == "Connected"
