"""Tests for the Meraki uplink status sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.uplink_status import MerakiUplinkStatusSensor

@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
    return coordinator

def test_uplink_status_online(mock_device_coordinator):
    """Test the uplink status sensor when online."""
    mock_device_coordinator.data = {
        'devices': [
            {
                'serial': 'dev1',
                'name': 'Appliance',
                'model': 'MX64',
                'productType': 'appliance',
                'uplinks': [
                    {'interface': 'WAN 1', 'status': 'active', 'ip': '1.1.1.1'},
                    {'interface': 'WAN 2', 'status': 'ready', 'ip': '2.2.2.2'},
                ],
            }
        ]
    }
    device = mock_device_coordinator.data['devices'][0]
    sensor = MerakiUplinkStatusSensor(mock_device_coordinator, device)
    assert sensor.unique_id == 'dev1_uplink_status'
    assert sensor.name == 'Appliance Uplink Status'
    assert sensor.state == 'online'
    assert sensor.extra_state_attributes['WAN 1_status'] == 'active'
    assert sensor.extra_state_attributes['WAN 2_status'] == 'ready'

def test_uplink_status_ready(mock_device_coordinator):
    """Test the uplink status sensor when ready."""
    mock_device_coordinator.data = {
        'devices': [
            {
                'serial': 'dev1',
                'name': 'Appliance',
                'model': 'MX64',
                'productType': 'appliance',
                'uplinks': [
                    {'interface': 'WAN 1', 'status': 'failed', 'ip': '1.1.1.1'},
                    {'interface': 'WAN 2', 'status': 'ready', 'ip': '2.2.2.2'},
                ],
            }
        ]
    }
    device = mock_device_coordinator.data['devices'][0]
    sensor = MerakiUplinkStatusSensor(mock_device_coordinator, device)
    assert sensor.state == 'ready'
    assert sensor.extra_state_attributes['WAN 1_status'] == 'failed'
    assert sensor.extra_state_attributes['WAN 2_status'] == 'ready'

def test_uplink_status_offline(mock_device_coordinator):
    """Test the uplink status sensor when offline."""
    mock_device_coordinator.data = {
        'devices': [
            {
                'serial': 'dev1',
                'name': 'Appliance',
                'model': 'MX64',
                'productType': 'appliance',
                'uplinks': [
                    {'interface': 'WAN 1', 'status': 'failed', 'ip': '1.1.1.1'},
                    {'interface': 'WAN 2', 'status': 'failed', 'ip': '2.2.2.2'},
                ],
            }
        ]
    }
    device = mock_device_coordinator.data['devices'][0]
    sensor = MerakiUplinkStatusSensor(mock_device_coordinator, device)
    assert sensor.state == 'offline'
    assert sensor.extra_state_attributes['WAN 1_status'] == 'failed'
    assert sensor.extra_state_attributes['WAN 2_status'] == 'failed'
