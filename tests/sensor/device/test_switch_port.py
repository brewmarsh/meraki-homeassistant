"""Tests for the Switch Port Power and Energy sensors."""

from unittest.mock import MagicMock

import pytest
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy, UnitOfPower

from custom_components.meraki_ha.sensor.device.switch_port import (
    MerakiSwitchPortEnergySensor,
    MerakiSwitchPortPowerSensor,
)
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_coordinator_and_device():
    """Fixture for a mocked coordinator and device."""
    coordinator = MagicMock()
    device = MerakiDevice(
        serial="Q234-ABCD-5678",
        name="Test Switch",
        model="MS220-8P",
        product_type="switch",
        ports_statuses=[
            {"portId": "1", "powerUsageInWh": 240},
            {"portId": "2", "powerUsageInWh": 0},
            {"portId": "3"},  # Missing powerUsageInWh
        ],
    )
    coordinator.data = {"devices": [device]}
    coordinator.get_device.return_value = device
    return coordinator, device


def test_switch_port_power_sensor(mock_coordinator_and_device):
    """Test the switch port power sensor."""
    coordinator, device = mock_coordinator_and_device
    port = device.ports_statuses[0]
    config_entry = MagicMock()

    sensor = MerakiSwitchPortPowerSensor(coordinator, device, port, config_entry)

    assert sensor.unique_id == "Q234-ABCD-5678_port_1_power"
    assert sensor.translation_key == "power"
    assert sensor.device_class == SensorDeviceClass.POWER
    assert sensor.native_unit_of_measurement == UnitOfPower.WATT
    assert sensor.state_class == SensorStateClass.MEASUREMENT

    # 240 Wh / 24 h = 10 W
    assert sensor.native_value == 10.0


def test_switch_port_energy_sensor(mock_coordinator_and_device):
    """Test the switch port energy sensor."""
    coordinator, device = mock_coordinator_and_device
    port = device.ports_statuses[0]
    config_entry = MagicMock()

    sensor = MerakiSwitchPortEnergySensor(coordinator, device, port, config_entry)

    assert sensor.unique_id == "Q234-ABCD-5678_port_1_energy"
    assert sensor.translation_key == "energy"
    assert sensor.device_class == SensorDeviceClass.ENERGY
    assert sensor.native_unit_of_measurement == UnitOfEnergy.WATT_HOUR
    assert sensor.state_class == SensorStateClass.MEASUREMENT

    assert sensor.native_value == 240


def test_switch_port_power_sensor_missing_data(mock_coordinator_and_device):
    """Test the switch port power sensor with missing data."""
    coordinator, device = mock_coordinator_and_device
    port = device.ports_statuses[2]  # No powerUsageInWh
    config_entry = MagicMock()

    sensor = MerakiSwitchPortPowerSensor(coordinator, device, port, config_entry)
    assert sensor.native_value == 0.0


def test_switch_port_energy_sensor_missing_data(mock_coordinator_and_device):
    """Test the switch port energy sensor with missing data."""
    coordinator, device = mock_coordinator_and_device
    port = device.ports_statuses[2]  # No powerUsageInWh
    config_entry = MagicMock()

    sensor = MerakiSwitchPortEnergySensor(coordinator, device, port, config_entry)
    assert sensor.native_value == 0
