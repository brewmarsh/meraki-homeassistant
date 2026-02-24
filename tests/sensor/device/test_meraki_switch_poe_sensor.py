"""Tests for the Meraki Switch PoE sensor."""

from unittest.mock import MagicMock

import pytest
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfPower

from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.sensor.device.switch_poe import MerakiSwitchPoESensor


@pytest.fixture
def mock_coordinator_and_device():
    """Fixture for a mocked coordinator and device."""
    coordinator = MagicMock()
    device = MerakiDevice(
        serial="Q234-ABCD-5678",
        name="Test Switch",
        model="MS220-8P",
        status="online",
        product_type="switch",
        ports_statuses=[
            {
                "portId": "1",
                "powerUsage": {"power": 15.5, "voltage": 54.0, "current": 0.28},
                "powerUsageInWh": 372.0,
            },
            {"portId": "2", "powerUsage": {}},
            {"portId": "3"},  # Missing powerUsage
        ],
    )
    coordinator.data = {"devices": [device]}
    coordinator.get_device.return_value = device
    return coordinator, device


def test_meraki_switch_poe_sensor_init(mock_coordinator_and_device):
    """Test the Meraki switch PoE sensor initialization."""
    coordinator, device = mock_coordinator_and_device
    port = device.ports_statuses[0]
    config_entry = MagicMock()

    sensor = MerakiSwitchPoESensor(coordinator, device, port, config_entry)

    assert sensor.unique_id == "Q234-ABCD-5678_port_1_poe"
    assert sensor.name == "Port 1 PoE"
    assert sensor.device_class == SensorDeviceClass.POWER
    assert sensor.native_unit_of_measurement == UnitOfPower.WATT
    assert sensor.state_class == SensorStateClass.MEASUREMENT


def test_meraki_switch_poe_sensor_native_value(mock_coordinator_and_device):
    """Test the Meraki switch PoE sensor native value."""
    coordinator, device = mock_coordinator_and_device
    config_entry = MagicMock()

    # Port 1: has powerUsage.power
    sensor1 = MerakiSwitchPoESensor(
        coordinator, device, device.ports_statuses[0], config_entry
    )
    assert sensor1.native_value == 15.5

    # Port 2: has powerUsage but no power key
    sensor2 = MerakiSwitchPoESensor(
        coordinator, device, device.ports_statuses[1], config_entry
    )
    assert sensor2.native_value == 0.0

    # Port 3: missing powerUsage
    sensor3 = MerakiSwitchPoESensor(
        coordinator, device, device.ports_statuses[2], config_entry
    )
    assert sensor3.native_value == 0.0


def test_meraki_switch_poe_sensor_extra_state_attributes(mock_coordinator_and_device):
    """Test the Meraki switch PoE sensor extra state attributes."""
    coordinator, device = mock_coordinator_and_device
    config_entry = MagicMock()

    # Port 1
    sensor1 = MerakiSwitchPoESensor(
        coordinator, device, device.ports_statuses[0], config_entry
    )
    attrs1 = sensor1.extra_state_attributes
    assert attrs1["power"] == 15.5
    assert attrs1["voltage"] == 54.0
    assert attrs1["current"] == 0.28

    # Port 2
    sensor2 = MerakiSwitchPoESensor(
        coordinator, device, device.ports_statuses[1], config_entry
    )
    attrs2 = sensor2.extra_state_attributes
    assert attrs2["power"] is None
    assert attrs2["voltage"] is None
    assert attrs2["current"] is None


def test_meraki_switch_poe_sensor_update(mock_coordinator_and_device):
    """Test the Meraki switch PoE sensor update."""
    coordinator, device = mock_coordinator_and_device
    port = device.ports_statuses[0]
    config_entry = MagicMock()

    sensor = MerakiSwitchPoESensor(coordinator, device, port, config_entry)
    sensor.async_write_ha_state = MagicMock()

    # Update data
    device.ports_statuses[0]["powerUsage"]["power"] = 20.0
    coordinator.data = {"devices": [device]}

    sensor._handle_coordinator_update()

    assert sensor.native_value == 20.0
