"""Tests for the Meraki appliance port sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.appliance_port import MerakiAppliancePortSensor

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
                'ports': [
                    {'number': 1, 'status': 'connected', 'speed': '1000 Mbps', 'vlan': 1, 'type': 'access', 'accessPolicy': None},
                    {'number': 2, 'status': 'disconnected', 'speed': None, 'vlan': 1, 'type': 'access', 'accessPolicy': None},
                ],
            }
        ]
    }
    return coordinator

def test_appliance_port_sensor(mock_device_coordinator):
    """Test the appliance port sensor."""
    device = mock_device_coordinator.data['devices'][0]
    port1 = device['ports'][0]
    port2 = device['ports'][1]

    sensor1 = MerakiAppliancePortSensor(mock_device_coordinator, device, port1)
    assert sensor1.unique_id == 'dev1_port_1'
    assert sensor1.name == 'Appliance Port 1'
    assert sensor1.state == 'online'
    assert sensor1.extra_state_attributes['link_speed'] == '1000 Mbps'

    sensor2 = MerakiAppliancePortSensor(mock_device_coordinator, device, port2)
    assert sensor2.unique_id == 'dev1_port_2'
    assert sensor2.name == 'Appliance Port 2'
    assert sensor2.state == 'offline'
    assert sensor2.extra_state_attributes['link_speed'] is None
