"""Tests for the Meraki appliance port sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.appliance_port import (
    MerakiAppliancePortSensor,
)


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "dev1",
                "name": "Appliance",
                "model": "MX64",
                "productType": "appliance",
                "ports": [
                    {
                        "number": 1,
                        "enabled": True,
                        "status": "connected",
                        "speed": "1000 Mbps",
                        "vlan": 1,
                        "type": "access",
                        "accessPolicy": None,
                    },
                    {
                        "number": 2,
                        "enabled": True,
                        "status": "disconnected",
                        "speed": None,
                        "vlan": 1,
                        "type": "access",
                        "accessPolicy": None,
                    },
                    {
                        "number": 3,
                        "enabled": False,
                        "status": "disconnected",
                        "speed": None,
                        "vlan": 1,
                        "type": "access",
                        "accessPolicy": None,
                    },
                ],
            }
        ]
    }
    return coordinator


def test_appliance_port_sensor(mock_device_coordinator):
    """Test the appliance port sensor."""
    device = mock_device_coordinator.data["devices"][0]
    port1 = device["ports"][0]
    port2 = device["ports"][1]
    port3 = device["ports"][2]

    # Test connected port
    sensor1 = MerakiAppliancePortSensor(mock_device_coordinator, device, port1)
    assert sensor1.unique_id == "dev1_port_1"
    # Name is the device name (format_entity_name with default NONE format)
    assert sensor1.name == "Appliance"
    assert sensor1.state == "connected"
    assert sensor1.extra_state_attributes["link_speed"] == "1000 Mbps"
    assert sensor1.extra_state_attributes["vlan"] == 1
    assert sensor1.extra_state_attributes["type"] == "access"

    # Test disconnected port
    sensor2 = MerakiAppliancePortSensor(mock_device_coordinator, device, port2)
    assert sensor2.unique_id == "dev1_port_2"
    assert sensor2.name == "Appliance"
    assert sensor2.state == "disconnected"
    assert sensor2.extra_state_attributes["link_speed"] is None

    # Test disabled port
    sensor3 = MerakiAppliancePortSensor(mock_device_coordinator, device, port3)
    assert sensor3.unique_id == "dev1_port_3"
    assert sensor3.name == "Appliance"
    assert sensor3.state == "disabled"
