"""Tests for the Meraki network info sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.network.meraki_network_info import (
    MerakiNetworkInfoSensor,
)


@pytest.fixture
def mock_data_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "networks": [
            {
                "id": "net1",
                "name": "Network 1",
                "productType": "network",
                "timeZone": "America/Los_Angeles",
            }
        ]
    }
    return coordinator


def test_network_info_sensor(mock_data_coordinator):
    """Test the network info sensor."""
    network = mock_data_coordinator.data["networks"][0]
    config_entry = mock_data_coordinator.config_entry

    # Test with prefix format
    config_entry.options = {"device_name_format": "prefix"}
    sensor = MerakiNetworkInfoSensor(mock_data_coordinator, network, config_entry)
    assert sensor.unique_id == "net1_network_info"
    assert sensor.name == "Network Information"
    assert sensor.device_info["name"] == "[Network] Network 1"
    assert sensor.state == "Network 1"
    assert sensor.extra_state_attributes["time_zone"] == "America/Los_Angeles"

    # Test with omit format
    config_entry.options = {"device_name_format": "omit"}
    sensor = MerakiNetworkInfoSensor(mock_data_coordinator, network, config_entry)
    assert sensor.name == "Network Information"
    assert sensor.device_info["name"] == "Network 1"
