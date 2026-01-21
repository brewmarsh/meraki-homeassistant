"""Tests for the Meraki appliance port sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.appliance_port import (
    MerakiAppliancePortSensor,
)
<<<<<<< HEAD
=======
from custom_components.meraki_ha.types import MerakiDevice, MerakiAppliancePort
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
<<<<<<< HEAD
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
=======

    device = MerakiDevice(
        serial="dev1",
        name="Appliance",
        model="MX64",
        mac="00:11:22:33:44:55",
        product_type="appliance",
    )

    device.appliance_ports = [
        MerakiAppliancePort(
            number=1,
            enabled=True,
            status="connected",
            speed="1000 Mbps",
            vlan=1,
            type="access",
            access_policy=None,
        ),
        MerakiAppliancePort(
            number=2,
            enabled=True,
            status="disconnected",
            speed=None,
            vlan=1,
            type="access",
            access_policy=None,
        ),
        MerakiAppliancePort(
            number=3,
            enabled=False,
            status="disconnected",
            speed=None,
            vlan=1,
            type="access",
            access_policy=None,
        ),
    ]

    coordinator.data = {
        "devices": [device]
    }
    # coordinator.get_device needs to return the device
    coordinator.get_device.return_value = device

    # Mock config entry options
    coordinator.config_entry.options = {}

>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    return coordinator


def test_appliance_port_sensor(mock_device_coordinator):
    """Test the appliance port sensor."""
    device = mock_device_coordinator.data["devices"][0]
<<<<<<< HEAD
    port1 = device["ports"][0]
    port2 = device["ports"][1]
    port3 = device["ports"][2]
=======
    port1 = device.appliance_ports[0]
    port2 = device.appliance_ports[1]
    port3 = device.appliance_ports[2]
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    # Test connected port
    sensor1 = MerakiAppliancePortSensor(mock_device_coordinator, device, port1)
    assert sensor1.unique_id == "dev1_port_1"
<<<<<<< HEAD
    assert sensor1.name == "Appliance Port 1"
    assert sensor1.state == "connected"
=======
    assert sensor1.name == "[Appliance] Appliance Port 1"
    assert sensor1.native_value == "connected"
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    assert sensor1.extra_state_attributes["link_speed"] == "1000 Mbps"
    assert sensor1.extra_state_attributes["vlan"] == 1
    assert sensor1.extra_state_attributes["type"] == "access"

    # Test disconnected port
    sensor2 = MerakiAppliancePortSensor(mock_device_coordinator, device, port2)
    assert sensor2.unique_id == "dev1_port_2"
<<<<<<< HEAD
    assert sensor2.name == "Appliance Port 2"
    assert sensor2.state == "disconnected"
=======
    assert sensor2.name == "[Appliance] Appliance Port 2"
    assert sensor2.native_value == "disconnected"
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    assert sensor2.extra_state_attributes["link_speed"] is None

    # Test disabled port
    sensor3 = MerakiAppliancePortSensor(mock_device_coordinator, device, port3)
    assert sensor3.unique_id == "dev1_port_3"
<<<<<<< HEAD
    assert sensor3.name == "Appliance Port 3"
    assert sensor3.state == "disabled"
=======
    assert sensor3.name == "[Appliance] Appliance Port 3"
    assert sensor3.native_value == "disabled"
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
