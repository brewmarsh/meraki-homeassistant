"""Tests for the Meraki appliance port sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.appliance_port import (
    MerakiAppliancePortSensor,
)
from custom_components.meraki_ha.types import MerakiAppliancePort, MerakiDevice


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()

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

    coordinator.data = {"devices": [device]}
    # coordinator.get_device needs to return the device
    coordinator.get_device.return_value = device

    # Mock config entry options
    coordinator.config_entry.options = {}

    return coordinator


def test_appliance_port_sensor(mock_device_coordinator):
    """Test the appliance port sensor."""
    device = mock_device_coordinator.data["devices"][0]
    port1 = device.appliance_ports[0]
    port2 = device.appliance_ports[1]
    port3 = device.appliance_ports[2]

    # Test connected port
    sensor1 = MerakiAppliancePortSensor(mock_device_coordinator, device, port1)
    assert sensor1.unique_id == "dev1_port_1"
    assert sensor1.name == "[Appliance] Appliance Port 1"
    assert sensor1.native_value == "connected"
    assert sensor1.extra_state_attributes["link_speed"] == "1000 Mbps"
    assert sensor1.extra_state_attributes["vlan"] == 1
    assert sensor1.extra_state_attributes["type"] == "access"

    # Test disconnected port
    sensor2 = MerakiAppliancePortSensor(mock_device_coordinator, device, port2)
    assert sensor2.unique_id == "dev1_port_2"
    assert sensor2.name == "[Appliance] Appliance Port 2"
    assert sensor2.native_value == "disconnected"
    assert sensor2.extra_state_attributes["link_speed"] is None

    # Test disabled port
    sensor3 = MerakiAppliancePortSensor(mock_device_coordinator, device, port3)
    assert sensor3.unique_id == "dev1_port_3"
    assert sensor3.name == "[Appliance] Appliance Port 3"
    assert sensor3.native_value == "disabled"
