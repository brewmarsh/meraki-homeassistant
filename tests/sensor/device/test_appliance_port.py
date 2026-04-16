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
    coordinator.config_entry.options = {"enable_port_sensors": True}

    return coordinator


def test_appliance_port_sensor(mock_device_coordinator):
    """Test the appliance port sensor."""
    device = mock_device_coordinator.data["devices"][0]
    port1 = device.appliance_ports[0]
    port2 = device.appliance_ports[1]
    port3 = device.appliance_ports[2]

    # Test connected port
    sensor1 = MerakiAppliancePortSensor(mock_device_coordinator, device, port1)
    assert (
        sensor1.unique_id == "dev1_appliance_port_1_status"
    )  # Action 2: Updated unique ID
    assert sensor1.name == "Port 1"
    assert sensor1.native_value == "connected"
    assert sensor1.extra_state_attributes["link_speed"] == "1000 Mbps"
    assert sensor1.extra_state_attributes["vlan"] == 1
    assert sensor1.extra_state_attributes["type"] == "access"
    assert sensor1.extra_state_attributes["icon_color"] == "green"
    assert sensor1.icon == "mdi:ethernet"

    # Test disconnected port
    sensor2 = MerakiAppliancePortSensor(mock_device_coordinator, device, port2)
    assert (
        sensor2.unique_id == "dev1_appliance_port_2_status"
    )  # Action 2: Updated unique ID
    assert sensor2.name == "Port 2"
    assert sensor2.native_value == "disconnected"
    assert sensor2.extra_state_attributes["link_speed"] is None
    assert sensor2.extra_state_attributes["icon_color"] == "grey"
    assert sensor2.icon == "mdi:ethernet-cable-off"

    # Test disabled port
    sensor3 = MerakiAppliancePortSensor(mock_device_coordinator, device, port3)
    assert (
        sensor3.unique_id == "dev1_appliance_port_3_status"
    )  # Action 2: Updated unique ID
    assert sensor3.name == "Port 3"
    assert sensor3.native_value == "disconnected"
    assert sensor3.extra_state_attributes["enabled"] is False
    assert sensor3.extra_state_attributes["icon_color"] == "grey"
    assert sensor3.icon == "mdi:ethernet-cable-off"


def test_appliance_port_sensor_update(mock_device_coordinator):
    """Test the coordinator update handler for the appliance port sensor."""
    device = mock_device_coordinator.data["devices"][0]
    port1 = device.appliance_ports[0]

    sensor = MerakiAppliancePortSensor(mock_device_coordinator, device, port1)
    sensor.async_write_ha_state = MagicMock()

    # Update port status to disconnected
    new_port = MerakiAppliancePort(
        number=1,
        enabled=True,
        status="disconnected",
        speed=None,
        vlan=1,
        type="access",
    )
    new_device = MagicMock(spec=MerakiDevice)
    new_device.serial = "dev1"
    new_device.appliance_ports = [new_port]
    mock_device_coordinator.get_device.return_value = new_device

    sensor._handle_coordinator_update()

    assert sensor.native_value == "disconnected"
    sensor.async_write_ha_state.assert_called_once()


def test_appliance_port_sensor_update_no_change(mock_device_coordinator):
    """Test the coordinator update handler when no state change occurs."""
    device = mock_device_coordinator.data["devices"][0]
    port1 = device.appliance_ports[0]

    sensor = MerakiAppliancePortSensor(mock_device_coordinator, device, port1)
    sensor.async_write_ha_state = MagicMock()

    # Update port status but it stays "connected"
    new_port = MerakiAppliancePort(
        number=1,
        enabled=True,
        status="connected",
        speed="1000 Mbps",
        vlan=1,
        type="access",
    )
    new_device = MagicMock(spec=MerakiDevice)
    new_device.serial = "dev1"
    new_device.appliance_ports = [new_port]
    mock_device_coordinator.get_device.return_value = new_device

    sensor._handle_coordinator_update()

    assert sensor.native_value == "connected"
    sensor.async_write_ha_state.assert_not_called()


def test_appliance_port_sensor_edge_cases(mock_device_coordinator):
    """Test edge cases for the appliance port sensor."""
    device = mock_device_coordinator.data["devices"][0]

    # Port with missing status
    port_no_status = MerakiAppliancePort(
        number=4,
        enabled=True,
        status=None,
    )
    sensor = MerakiAppliancePortSensor(mock_device_coordinator, device, port_no_status)
    assert sensor.native_value == "disconnected"

    # Port with empty list of appliance_ports in update
    sensor.async_write_ha_state = MagicMock()
    new_device = MagicMock(spec=MerakiDevice)
    new_device.serial = "dev1"
    new_device.appliance_ports = []
    mock_device_coordinator.get_device.return_value = new_device

    sensor._handle_coordinator_update()
    sensor.async_write_ha_state.assert_not_called()
