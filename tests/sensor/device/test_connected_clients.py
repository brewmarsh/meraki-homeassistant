"""Tests for the Meraki connected clients sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.connected_clients import MerakiDeviceConnectedClientsSensor

@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
    return coordinator

def test_connected_clients_sensor_appliance(mock_device_coordinator):
    """Test the connected clients sensor for an appliance."""
    mock_device_coordinator.data = {
        'devices': [
            {
                'serial': 'dev1',
                'name': 'Appliance',
                'model': 'MX64',
                'productType': 'appliance',
                'connected_clients_count': 42,
            }
        ]
    }
    device = mock_device_coordinator.data['devices'][0]
    sensor = MerakiDeviceConnectedClientsSensor(mock_device_coordinator, device)
    assert sensor.unique_id == 'dev1_connected_clients'
    assert sensor.name == 'Appliance Connected Clients'
    assert sensor.native_value == 42

def test_connected_clients_sensor_wireless(mock_device_coordinator):
    """Test the connected clients sensor for a wireless device."""
    mock_device_coordinator.data = {
        'devices': [
            {
                'serial': 'dev2',
                'name': 'Access Point',
                'model': 'MR52',
                'productType': 'wireless',
                'connected_clients_count': 10,
            }
        ]
    }
    device = mock_device_coordinator.data['devices'][0]
    sensor = MerakiDeviceConnectedClientsSensor(mock_device_coordinator, device)
    assert sensor.unique_id == 'dev2_connected_clients'
    assert sensor.name == 'Access Point Connected Clients'
    assert sensor.native_value == 10
