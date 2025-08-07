"""Tests for the Meraki network info sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.network.meraki_network_info import MerakiNetworkInfoSensor

@pytest.fixture
def mock_network_coordinator():
    """Fixture for a mocked MerakiNetworkCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        'networks': [
            {
                'id': 'net1',
                'name': 'Network 1',
                'productType': 'network',
                'timeZone': 'America/Los_Angeles',
            }
        ]
    }
    return coordinator

def test_network_info_sensor(mock_network_coordinator):
    """Test the network info sensor."""
    network = mock_network_coordinator.data['networks'][0]

    # Test with prefix format
    mock_network_coordinator.config_entry.options = {'device_name_format': 'prefix'}
    sensor = MerakiNetworkInfoSensor(mock_network_coordinator, network, MagicMock())
    assert sensor.unique_id == 'net1_network_info'
    assert sensor.name == '[Sensor] Network 1 Network Information'
    assert sensor.state == 'Network 1'
    assert sensor.extra_state_attributes['time_zone'] == 'America/Los_Angeles'

    # Test with omit format
    mock_network_coordinator.config_entry.options = {'device_name_format': 'omit'}
    sensor = MerakiNetworkInfoSensor(mock_network_coordinator, network, MagicMock())
    assert sensor.name == 'Network 1 Network Information'
