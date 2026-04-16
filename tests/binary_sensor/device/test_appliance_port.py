"""Tests for the Meraki appliance port binary sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.binary_sensor.device.appliance_port import (
    AppliancePortBinarySensor,
)
from custom_components.meraki_ha.core.models import MerakiAppliancePort
from custom_components.meraki_ha.core.models.device import MerakiDevice


@pytest.fixture
def mock_appliance_coordinator():
    """Fixture for a mocked MerakiApplianceCoordinator."""
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
        ),
        MerakiAppliancePort(
            number=2,
            enabled=True,
            status="disconnected",
            speed=None,
            vlan=1,
            type="access",
        ),
        MerakiAppliancePort(
            number=3,
            enabled=False,
            status="connected",
            speed=None,
            vlan=1,
            type="access",
        ),
    ]

    coordinator.data = {"devices": [device]}
    coordinator.get_device.return_value = device

    return coordinator


def test_appliance_port_binary_sensor(mock_appliance_coordinator):
    """Test the appliance port binary sensor."""
    device = mock_appliance_coordinator.data["devices"][0]
    port1 = device.appliance_ports[0]
    port2 = device.appliance_ports[1]
    port3 = device.appliance_ports[2]

    # Test connected and enabled port
    sensor1 = AppliancePortBinarySensor(mock_appliance_coordinator, device, port1)
    assert sensor1.unique_id == "dev1_appliance_port_1_connectivity"
    assert sensor1.name == "Port 1"
    assert sensor1.is_on is True
    assert sensor1.extra_state_attributes["link_speed"] == "1000 Mbps"
    assert sensor1.device_class == "connectivity"

    # Test disconnected and enabled port
    sensor2 = AppliancePortBinarySensor(mock_appliance_coordinator, device, port2)
    assert sensor2.unique_id == "dev1_appliance_port_2_connectivity"
    assert sensor2.is_on is False

    # Test connected but disabled port
    sensor3 = AppliancePortBinarySensor(mock_appliance_coordinator, device, port3)
    assert sensor3.unique_id == "dev1_appliance_port_3_connectivity"
    assert sensor3.is_on is False


def test_handle_coordinator_update(mock_appliance_coordinator):
    """Test the coordinator update handler."""
    device = mock_appliance_coordinator.data["devices"][0]
    port1 = device.appliance_ports[0]

    sensor = AppliancePortBinarySensor(mock_appliance_coordinator, device, port1)
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
    mock_appliance_coordinator.get_device.return_value = new_device

    sensor._handle_coordinator_update()

    assert sensor.is_on is False
    sensor.async_write_ha_state.assert_called_once()


def test_handle_coordinator_update_no_change(mock_appliance_coordinator):
    """Test the coordinator update handler when no state change occurs."""
    device = mock_appliance_coordinator.data["devices"][0]
    port1 = device.appliance_ports[0]

    sensor = AppliancePortBinarySensor(mock_appliance_coordinator, device, port1)
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
    mock_appliance_coordinator.get_device.return_value = new_device

    sensor._handle_coordinator_update()

    assert sensor.is_on is True
    sensor.async_write_ha_state.assert_not_called()
