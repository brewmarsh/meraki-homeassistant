"""Tests for the Meraki data usage sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.data_usage import MerakiDataUsageSensor

@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        'devices': [
            {
                'serial': 'dev1',
                'name': 'Appliance',
                'model': 'MX64',
                'productType': 'appliance',
                'traffic': [
                    {
                        'sent': 2048, # 2 MB
                        'received': 8192, # 8 MB
                    }
                ]
            }
        ]
    }
    return coordinator

def test_data_usage_sensor(mock_device_coordinator):
    """Test the data usage sensor."""
    device = mock_device_coordinator.data['devices'][0]
    sensor = MerakiDataUsageSensor(mock_device_coordinator, device)
    assert sensor.unique_id == 'dev1_data_usage'
    assert sensor.name == 'Appliance Data Usage'
    assert sensor.native_value == 10.0 # 2 + 8
    assert sensor.extra_state_attributes['sent'] == 2.0
    assert sensor.extra_state_attributes['received'] == 8.0
