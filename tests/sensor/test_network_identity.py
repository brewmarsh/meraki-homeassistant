"""Tests for the Meraki network identity sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.network_identity import (
    MerakiNetworkIdentitySensor,
)


async def test_meraki_network_identity_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki network identity sensor."""
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
    sensor = MerakiNetworkIdentitySensor(coordinator, network_data)
    sensor._update_sensor_state()
    assert sensor.native_value == "Test Network"
