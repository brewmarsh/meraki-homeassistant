"""Tests for the Meraki network info sensor."""
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.meraki_network_info import (
    MerakiNetworkInfoSensor,
)


async def test_meraki_network_info_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki network info sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "networks": [
            {
                "id": "N_123",
                "name": "Test Network",
            }
        ]
    }
    network_data = {
        "id": "N_123",
    }
    sensor = MerakiNetworkInfoSensor(coordinator, network_data)
    sensor._update_state()
    assert sensor.native_value == "Test Network"
