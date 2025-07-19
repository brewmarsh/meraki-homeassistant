"""Tests for the Meraki WAN1 connectivity sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.meraki_wan1_connectivity import (
    MerakiWAN1ConnectivitySensor,
)


async def test_meraki_wan1_connectivity_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki WAN1 connectivity sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "wan1Ip": "1.2.3.4",
                "status": "online",
            }
        ]
    }
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    sensor = MerakiWAN1ConnectivitySensor(coordinator, device_data)
    sensor._update_state()
    assert sensor.native_value == "Connected"
