"""Tests for the Meraki switch port sensor."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.switch_port import MerakiSwitchPortSensor


@pytest.fixture
def mock_data_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    return coordinator


def test_switch_port_sensor(mock_data_coordinator):
    """Test the switch port sensor."""
    device_data = {
        "serial": "dev1",
        "name": "My Switch",
        "model": "MS220",
        "productType": "switch",
        "firmware": "switch-15-1",
        "ports_statuses": [
            {
                "portId": "1",
                "enabled": True,
                "status": "connected",
                "speed": "1 Gbps",
            },
            {
                "portId": "2",
                "enabled": False,
                "status": "disabled",
            },
        ],
    }
    mock_data_coordinator.data = {"devices": [device_data]}

    config_entry = mock_data_coordinator.config_entry

    # Test port 1
    port1_data = device_data["ports_statuses"][0]
    sensor1 = MerakiSwitchPortSensor(
        mock_data_coordinator, device_data, config_entry, port1_data
    )
    assert sensor1.unique_id == "dev1_port_1"
    assert sensor1.name == "Port 1 Status"
    assert sensor1.native_value == "connected"
    assert sensor1.extra_state_attributes["speed"] == "1 Gbps"
    assert sensor1.device_info["name"] == "[Switch] My Switch"

    # Test port 2
    port2_data = device_data["ports_statuses"][1]
    sensor2 = MerakiSwitchPortSensor(
        mock_data_coordinator, device_data, config_entry, port2_data
    )
    assert sensor2.unique_id == "dev1_port_2"
    assert sensor2.name == "Port 2 Status"
    assert sensor2.native_value == "disabled"
