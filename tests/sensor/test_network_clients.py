"""Tests for the Meraki network clients sensor."""

from unittest.mock import MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.network.network_clients import (
    MerakiNetworkClientsSensor,
)
from custom_components.meraki_ha.types import MerakiNetwork


@pytest.fixture
def mock_network_control_service():
    """Fixture for a mock NetworkControlService."""
    service = MagicMock()
    service.get_network_client_count.return_value = 5
    return service


async def test_network_clients_sensor(
    hass: HomeAssistant,
    mock_network_control_service,
) -> None:
    """Test the Meraki network clients sensor."""
    coordinator = MagicMock()
    coordinator.data = {}  # Data is no longer read from coordinator
    config_entry = MagicMock()
    network_data = {
        "id": "N_123",
        "name": "Test Network",
        "productTypes": [],
        "organizationId": "org",
        "clientCount": 5,
    }
    sensor = MerakiNetworkClientsSensor(
        coordinator,
        config_entry,
        MerakiNetwork.from_dict(network_data),
        mock_network_control_service,
    )
    sensor.hass = hass
    sensor.entity_id = "sensor.test_network_clients"
    await sensor.async_added_to_hass()
    sensor._handle_coordinator_update()
    assert sensor.native_value == 5
    mock_network_control_service.get_network_client_count.assert_called_with("N_123")
