"""Tests for the Meraki VLANs list sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.setup_helpers import async_setup_sensors
from custom_components.meraki_ha.const import (
    CONF_ENABLE_VLAN_MANAGEMENT,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {
        "device_name_format": "omit",
        CONF_ENABLE_VLAN_MANAGEMENT: True,
    }
    coordinator.data = {
        "networks": [{"id": "net1", "name": "Test Network"}],
        "vlans": {
            "net1": [
                {
                    "id": 1,
                    "name": "VLAN 1",
                    "subnet": "192.168.1.0/24",
                    "applianceIp": "192.168.1.1",
                    "enabled": True,
                },
                {
                    "id": 2,
                    "name": "VLAN 2",
                    "subnet": "192.168.2.0/24",
                    "applianceIp": "192.168.2.1",
                    "enabled": True,
                },
            ]
        },
        "devices": [],
        "clients": [],
        "ssids": [],
    }
    return coordinator


def test_vlans_list_sensor_creation(mock_coordinator):
    """Test that the VLANs list sensor is created correctly."""
    hass = MagicMock()

    # Run the setup
    sensors = async_setup_sensors(hass, mock_coordinator.config_entry, mock_coordinator)

    # Find the specific sensor
    vlans_list_sensor = next(
        s for s in sensors if "VLANs" in s.name
    )

    # Assertions for VLANs List Sensor
    assert vlans_list_sensor.unique_id == "network-net1-vlans"
    assert vlans_list_sensor.name == "Test Network VLANs"
    assert vlans_list_sensor.native_value == 2
    assert len(vlans_list_sensor.extra_state_attributes["vlans"]) == 2
