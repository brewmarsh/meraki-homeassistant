"""Tests for the Meraki network clients sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.core.sensor.network_clients import (
    MerakiNetworkClientsSensor,
)


async def test_network_clients_sensor(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki network clients sensor."""
    coordinator = MagicMock()
    coordinator.data = {
        "clients": [
            {"id": "1", "description": "Client 1", "networkId": "N_123"},
            {"id": "2", "description": "Client 2", "networkId": "N_123"},
        ],
    }
    sensor = MerakiNetworkClientsSensor(coordinator, "N_123", "Test Network")
    sensor._update_state_from_coordinator()
    assert sensor.native_value == 2
