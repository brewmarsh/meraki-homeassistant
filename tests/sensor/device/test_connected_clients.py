"""Tests for the Meraki connected clients sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.connected_clients import MerakiDeviceConnectedClientsSensor

@pytest.fixture
def mock_data_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    return coordinator


def test_connected_clients_sensor_appliance(mock_data_coordinator):
    """Test the connected clients sensor for an appliance."""
    mock_data_coordinator.data = {
        "devices": [
            {
                "serial": "dev1",
                "name": "Appliance",
                "model": "MX64",
                "productType": "appliance",
                "connected_clients_count": 42,
            }
        ]
    }
    device = mock_data_coordinator.data["devices"][0]
    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiDeviceConnectedClientsSensor(mock_data_coordinator, device, config_entry)
    assert sensor.unique_id == "dev1_connected_clients"
    assert sensor.name == "Connected Clients"
    assert sensor.native_value == 42


def test_connected_clients_sensor_wireless(mock_data_coordinator):
    """Test the connected clients sensor for a wireless device."""
    mock_data_coordinator.data = {
        "devices": [
            {
                "serial": "dev2",
                "name": "Access Point",
                "model": "MR52",
                "productType": "wireless",
                "connected_clients_count": 10,
            }
        ]
    }
    device = mock_data_coordinator.data["devices"][0]
    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiDeviceConnectedClientsSensor(mock_data_coordinator, device, config_entry)
    assert sensor.unique_id == "dev2_connected_clients"
    assert sensor.name == "Connected Clients"
    assert sensor.native_value == 10
