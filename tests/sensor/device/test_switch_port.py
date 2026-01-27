"""Tests for the Meraki switch port sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.switch_port import (
    MerakiSwitchPortPowerSensor,
    MerakiSwitchPortSensor,
)
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()

    device = MerakiDevice(
        serial="dev1",
        name="Switch",
        model="MS120",
        mac="00:11:22:33:44:55",
        product_type="switch",
    )

    device.ports_statuses = [
        {
            "portId": "1",
            "enabled": True,
            "status": "Connected",
            "speed": "1 Gbps",
            "duplex": "full",
            "usageInKb": {"total": 100, "sent": 50, "recv": 50},
            "cdp": {},
            "lldp": {},
            "clientCount": 0,
            "powerUsageInWh": 240.0,  # 240 Wh -> 10 W
        },
        {
            "portId": "2",
            "enabled": True,
            "status": "Disconnected",
            "powerUsageInWh": 0.0,
        },
    ]

    coordinator.data = {"devices": [device]}
    coordinator.get_device.return_value = device
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}

    return coordinator


def test_switch_port_sensor(mock_device_coordinator):
    """Test the switch port sensor."""
    device = mock_device_coordinator.data["devices"][0]
    port1 = device.ports_statuses[0]

    sensor = MerakiSwitchPortSensor(
        mock_device_coordinator, device, port1, mock_device_coordinator.config_entry
    )
    assert sensor.unique_id == "dev1_port_1"
    assert sensor.name == "Port 1"
    assert sensor.native_value == "Connected"
    assert sensor.extra_state_attributes["speed"] == "1 Gbps"
    assert sensor.extra_state_attributes["duplex"] == "full"


def test_switch_port_power_sensor(mock_device_coordinator):
    """Test the switch port power sensor."""
    device = mock_device_coordinator.data["devices"][0]
    port1 = device.ports_statuses[0]

    sensor = MerakiSwitchPortPowerSensor(
        mock_device_coordinator, device, port1, mock_device_coordinator.config_entry
    )
    assert sensor.unique_id == "dev1_port_1_power"
    assert sensor.name == "Port 1 Power"
    # 240 Wh / 24 h = 10 W
    assert sensor.native_value == 10.0
    assert sensor.unit_of_measurement == "W"
    assert sensor.device_class == "power"
