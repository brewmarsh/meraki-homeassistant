"""Tests for the Meraki guest clients sensor."""

from unittest.mock import MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.network.guest_clients import (
    MerakiGuestClientsSensor,
)


@pytest.fixture
def mock_network_control_service():
    """Fixture for a mock NetworkControlService."""
    service = MagicMock()
    service.get_guest_client_count.return_value = 3
    return service


async def test_guest_clients_sensor(
    hass: HomeAssistant,
    mock_network_control_service,
) -> None:
    """Test the Meraki guest clients sensor."""
    coordinator = MagicMock()
    coordinator.data = {}
    config_entry = MagicMock()
    network_data = {"id": "N_123", "name": "Test Network"}
    sensor = MerakiGuestClientsSensor(
        coordinator, config_entry, network_data, mock_network_control_service
    )
    sensor.hass = hass
    sensor.entity_id = "sensor.test_guest_clients"
    await sensor.async_added_to_hass()
    sensor._handle_coordinator_update()
    assert sensor.native_value == 3
    mock_network_control_service.get_guest_client_count.assert_called_with("N_123")
