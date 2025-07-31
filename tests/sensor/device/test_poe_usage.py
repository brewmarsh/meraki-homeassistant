"""Tests for the Meraki PoE usage sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.poe_usage import MerakiPoeUsageSensor


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        'devices': [
            {
                'serial': 'dev1',
                'name': 'Switch',
                'model': 'MS220-8P',
                'productType': 'switch',
                'port_statuses': [
                    {'portId': 1, 'poe': {'power': 10.5}},
                    {'portId': 2, 'poe': {'power': 5.2}},
                    {'portId': 3, 'poe': None},
                ]
            }
        ]
    }
    return coordinator


def test_poe_usage_sensor(mock_device_coordinator):
    """Test the PoE usage sensor."""
    device = mock_device_coordinator.data['devices'][0]
    sensor = MerakiPoeUsageSensor(mock_device_coordinator, device)
    assert sensor.unique_id == 'dev1_poe_usage'
    assert sensor.name == 'Switch PoE Usage'
    assert sensor.native_value == 15.7
    assert sensor.extra_state_attributes['port_1_poe_usage'] == 10.5
    assert sensor.extra_state_attributes['port_2_poe_usage'] == 5.2
    assert 'port_3_poe_usage' not in sensor.extra_state_attributes
