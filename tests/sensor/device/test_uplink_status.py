"""Tests for the Meraki uplink status sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.uplink_status import MerakiUplinkStatusSensor

@pytest.fixture
def mock_data_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    return coordinator


def test_uplink_status_online(mock_data_coordinator):
    """Test the uplink status sensor when online."""
    mock_data_coordinator.data = {
        "devices": [
            {
                "serial": "dev1",
                "name": "Appliance",
                "model": "MX64",
                "productType": "appliance",
                "uplinks": [
                    {"interface": "WAN 1", "status": "active", "ip": "1.1.1.1"},
                    {"interface": "WAN 2", "status": "ready", "ip": "2.2.2.2"},
                ],
            }
        ]
    }
    device = mock_data_coordinator.data["devices"][0]
    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiUplinkStatusSensor(mock_data_coordinator, device, config_entry)
    assert sensor.unique_id == "dev1_uplink_status"
    assert sensor.name == "Uplink Status"
    assert sensor.native_value == "online"
    assert sensor.extra_state_attributes["WAN 1_status"] == "active"
    assert sensor.extra_state_attributes["WAN 2_status"] == "ready"


def test_uplink_status_ready(mock_data_coordinator):
    """Test the uplink status sensor when ready."""
    mock_data_coordinator.data = {
        "devices": [
            {
                "serial": "dev1",
                "name": "Appliance",
                "model": "MX64",
                "productType": "appliance",
                "uplinks": [
                    {"interface": "WAN 1", "status": "failed", "ip": "1.1.1.1"},
                    {"interface": "WAN 2", "status": "ready", "ip": "2.2.2.2"},
                ],
            }
        ]
    }
    device = mock_data_coordinator.data["devices"][0]
    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiUplinkStatusSensor(mock_data_coordinator, device, config_entry)
    assert sensor.native_value == "ready"
    assert sensor.extra_state_attributes["WAN 1_status"] == "failed"
    assert sensor.extra_state_attributes["WAN 2_status"] == "ready"


def test_uplink_status_offline(mock_data_coordinator):
    """Test the uplink status sensor when offline."""
    mock_data_coordinator.data = {
        "devices": [
            {
                "serial": "dev1",
                "name": "Appliance",
                "model": "MX64",
                "productType": "appliance",
                "uplinks": [
                    {"interface": "WAN 1", "status": "failed", "ip": "1.1.1.1"},
                    {"interface": "WAN 2", "status": "failed", "ip": "2.2.2.2"},
                ],
            }
        ]
    }
    device = mock_data_coordinator.data["devices"][0]
    config_entry = mock_data_coordinator.config_entry
    sensor = MerakiUplinkStatusSensor(mock_data_coordinator, device, config_entry)
    assert sensor.native_value == "offline"
    assert sensor.extra_state_attributes["WAN 1_status"] == "failed"
    assert sensor.extra_state_attributes["WAN 2_status"] == "failed"
