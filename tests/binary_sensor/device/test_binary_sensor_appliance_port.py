"""Tests for Meraki appliance port binary sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.binary_sensor.device.appliance_port import (
    AppliancePortBinarySensor,
)
from custom_components.meraki_ha.core.models import MerakiAppliancePort
from custom_components.meraki_ha.core.models.device import MerakiDevice


@pytest.mark.asyncio
async def test_appliance_port_binary_sensor():
    """Test the AppliancePortBinarySensor."""
    mock_coordinator = MagicMock()

    device = MerakiDevice(serial="SERIAL123")
    port = MerakiAppliancePort(
        number=1,
        enabled=True,
        status="Connected",
        speed="1 Gbps",
        vlan=10,
        type="access",
    )
    device.appliance_ports = [port]

    mock_coordinator.get_device.return_value = device
    mock_coordinator.data = {"devices_by_serial": {"SERIAL123": device}}

    # Instantiate sensor
    sensor = AppliancePortBinarySensor(mock_coordinator, device, port)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()

    # Assert properties
    assert sensor.unique_id == "SERIAL123_appliance_port_1_connectivity"
    assert sensor.is_on is True
    assert sensor.name == "Port 1"
    assert sensor.extra_state_attributes == {
        "port_number": 1,
        "link_speed": "1 Gbps",
        "vlan": 10,
        "type": "access",
    }

    # Test update to disconnected
    new_port = MerakiAppliancePort(
        number=1,
        enabled=True,
        status="Disconnected",
        speed="None",
        vlan=10,
        type="access",
    )
    new_device = MerakiDevice(serial="SERIAL123")
    new_device.appliance_ports = [new_port]
    mock_coordinator.get_device.return_value = new_device

    sensor._handle_coordinator_update()
    assert sensor.is_on is False
    sensor.async_write_ha_state.assert_called()

    # Test disabled port
    disabled_port = MerakiAppliancePort(number=1, enabled=False, status="Connected")
    new_device.appliance_ports = [disabled_port]
    sensor._handle_coordinator_update()
    assert sensor.is_on is False
