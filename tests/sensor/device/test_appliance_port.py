"""Tests for Meraki appliance port sensor."""

from unittest.mock import MagicMock
import pytest

from custom_components.meraki_ha.sensor.device.appliance_port import MerakiAppliancePortSensor
from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.core.models import MerakiAppliancePort

@pytest.mark.asyncio
async def test_meraki_appliance_port_sensor():
    """Test the MerakiAppliancePortSensor."""
    mock_coordinator = MagicMock()

    device = MerakiDevice(serial="SERIAL123", model="MX64")
    port = MerakiAppliancePort(
        number=1,
        enabled=True,
        status="Connected",
        speed="1 Gbps",
        vlan=10,
        type="access",
        access_policy="Open"
    )
    device.appliance_ports = [port]

    mock_coordinator.get_device.return_value = device
    mock_coordinator.config_entry.options = {}

    # Instantiate sensor
    sensor = MerakiAppliancePortSensor(mock_coordinator, device, port)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()

    # Assert properties
    assert sensor.unique_id == "SERIAL123_appliance_port_1_status"
    assert sensor.native_value == "connected"
    assert sensor.name == "Port 1"
    assert sensor.icon == "mdi:ethernet"
    assert sensor.extra_state_attributes["port_number"] == 1
    assert sensor.extra_state_attributes["link_speed"] == "1 Gbps"

    # Test update to disconnected
    new_port = MerakiAppliancePort(
        number=1,
        enabled=True,
        status="Disconnected",
        speed="None",
        vlan=10,
        type="access",
        access_policy="Open"
    )
    new_device = MerakiDevice(serial="SERIAL123")
    new_device.appliance_ports = [new_port]
    mock_coordinator.get_device.return_value = new_device

    sensor._handle_coordinator_update()
    assert sensor.native_value == "disconnected"
    assert sensor.icon == "mdi:ethernet-cable-off"
    sensor.async_write_ha_state.assert_called()
