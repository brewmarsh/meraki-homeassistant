"""Tests for the Meraki port count sensors."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.port_counts import (
    MerakiPortsInUseSensor,
    MerakiPortsAvailableSensor,
)


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
    coordinator.scan_interval = 300
    coordinator.config_entry.options = {}
    coordinator.data = {
        'devices': [
            {
                'serial': 'dev1',
                'name': 'Switch',
                'model': 'MS220-8P',
                'productType': 'switch',
                'port_statuses': [
                    {'portId': 1, 'status': 'Connected'},
                    {'portId': 2, 'status': 'Connected'},
                    {'portId': 3, 'status': 'Disconnected'},
                    {'portId': 4, 'status': 'Disabled'},
                ]
            }
        ]
    }
    return coordinator


def test_port_counts_sensors(mock_device_coordinator):
    """Test the port count sensors."""
    device = mock_device_coordinator.data['devices'][0]

    ports_in_use_sensor = MerakiPortsInUseSensor(mock_device_coordinator, device)
    assert ports_in_use_sensor.unique_id == 'dev1_ports_in_use'
    assert ports_in_use_sensor.name == 'Switch Ports In Use'
    assert ports_in_use_sensor.native_value == 2

    ports_available_sensor = MerakiPortsAvailableSensor(mock_device_coordinator, device)
    assert ports_available_sensor.unique_id == 'dev1_ports_available'
    assert ports_available_sensor.name == 'Switch Ports Available'
    assert ports_available_sensor.native_value == 2
