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
            {"portId": "1", "powerUsageInWh": 5},  # 5 Wh over 5 min = 60 W
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
    coordinator.update_interval.total_seconds.return_value = 300.0  # 5 minutes
    port = device.ports_statuses[0]
    config_entry = MagicMock()

    sensor = MerakiSwitchPortPowerSensor(coordinator, device, port, config_entry)

    assert sensor.unique_id == "Q234-ABCD-5678_port_1_power"
    assert sensor.translation_key == "power"
    assert sensor.device_class == SensorDeviceClass.POWER
    assert sensor.native_unit_of_measurement == UnitOfPower.WATT
    assert sensor.state_class == SensorStateClass.MEASUREMENT

    # 5 Wh * 3600 s/h / 300 s = 60 W
    assert sensor.native_value == 60.0


def test_switch_port_energy_sensor(mock_coordinator_and_device):
    """Test the switch port energy sensor."""
    from datetime import datetime, timedelta

    coordinator, device = mock_coordinator_and_device
    port = device.ports_statuses[0]
    config_entry = MagicMock()

    # Mock last_successful_update
    coordinator.last_successful_update = datetime.now()

    sensor = MerakiSwitchPortEnergySensor(coordinator, device, port, config_entry)
    sensor.async_write_ha_state = MagicMock()

    assert sensor.unique_id == "Q234-ABCD-5678_port_1_energy"
    assert sensor.translation_key == "energy"
    assert sensor.device_class == SensorDeviceClass.ENERGY
    assert sensor.native_unit_of_measurement == UnitOfEnergy.WATT_HOUR
    assert sensor.state_class == SensorStateClass.TOTAL_INCREASING

    # Initial state should be 0
    assert sensor.native_value == 0.0

    # Simulate update
    sensor._handle_coordinator_update()

    # Should accumulate 5 Wh
    assert sensor.native_value == 5.0

    # Simulate another update with new data and new timestamp
    coordinator.last_successful_update += timedelta(minutes=5)
    # Assume 5 Wh again
    sensor._handle_coordinator_update()

    assert sensor.native_value == 10.0


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
    sensor.async_write_ha_state = MagicMock()
    sensor._handle_coordinator_update()
    assert sensor.native_value == 0.0
