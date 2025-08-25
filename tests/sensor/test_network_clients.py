"""Tests for the Meraki network clients sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.network.network_clients import (
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
    config_entry = MagicMock()
    network_data = {"id": "N_123", "name": "Test Network"}
    sensor = MerakiNetworkClientsSensor(coordinator, config_entry, network_data)
    sensor.hass = hass
    sensor.entity_id = "sensor.test_network_clients"
    await sensor.async_added_to_hass()
    sensor._handle_coordinator_update()
    assert sensor.native_value == 2
