"""Tests for the Switch Port Power and Energy sensors."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfEnergy, UnitOfPower
from homeassistant.core import State

from custom_components.meraki_ha.sensor.device.switch_port import (
    MerakiSwitchPortEnergySensor,
    MerakiSwitchPortPowerSensor,
)
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_coordinator_and_device():
    """Fixture for a mocked coordinator and device."""
    coordinator = MagicMock()
    # Mock total_seconds() to simulate interval, though our new logic ignores it for Power
    coordinator.update_interval.total_seconds.return_value = 86400.0
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
    coordinator.last_successful_update = None
    return coordinator, device


def test_switch_port_power_sensor(mock_coordinator_and_device):
    """Test the switch port power sensor."""
    coordinator, device = mock_coordinator_and_device
    coordinator.update_interval.total_seconds.return_value = 300.0  # 5 minutes
    port = device.ports_statuses[0]
    config_entry = MagicMock()

    sensor = MerakiSwitchPortPowerSensor(coordinator, device, port, config_entry)
    sensor.async_write_ha_state = MagicMock()
    sensor._handle_coordinator_update()

    assert sensor.unique_id == "Q234-ABCD-5678_port_1_power"
    assert sensor.translation_key == "power"
    assert sensor.device_class == SensorDeviceClass.POWER
    assert sensor.native_unit_of_measurement == UnitOfPower.WATT
    assert sensor.state_class == SensorStateClass.MEASUREMENT

    # MANUAL FIX: Updated to match fixed 24h logic (86400s)
    # 240 Wh * 3600 / 86400 = 10 W
    assert sensor.native_value == 10.0


def test_switch_port_power_sensor_long_interval(mock_coordinator_and_device):
    """Test the switch port power sensor with a long interval."""
    coordinator, device = mock_coordinator_and_device
    coordinator.update_interval.total_seconds.return_value = 86400.0  # 24 hours
    port = device.ports_statuses[0]
    config_entry = MagicMock()

    sensor = MerakiSwitchPortPowerSensor(coordinator, device, port, config_entry)

    # 240 Wh * 3600 / 86400 = 10 W
    assert sensor.native_value == 10.0


def test_switch_port_power_sensor_invalid_interval(mock_coordinator_and_device):
    """Test the switch port power sensor with an invalid interval."""
    coordinator, device = mock_coordinator_and_device
    coordinator.update_interval.total_seconds.return_value = 0.0
    port = device.ports_statuses[0]
    config_entry = MagicMock()

    sensor = MerakiSwitchPortPowerSensor(coordinator, device, port, config_entry)

    # Defaults to 24h: 240 Wh * 3600 / 86400 = 10 W
    assert sensor.native_value == 10.0


def test_switch_port_energy_sensor(mock_coordinator_and_device):
    """Test the switch port energy sensor initial state."""
    coordinator, device = mock_coordinator_and_device
    port = device.ports_statuses[0]
    config_entry = MagicMock()

    sensor = MerakiSwitchPortEnergySensor(coordinator, device, port, config_entry)
    sensor.async_write_ha_state = MagicMock()

    assert sensor.unique_id == "Q234-ABCD-5678_port_1_energy"
    assert sensor.translation_key == "energy"
    assert sensor.device_class == SensorDeviceClass.ENERGY
    assert sensor.native_unit_of_measurement == UnitOfEnergy.WATT_HOUR
    # Changed from MEASUREMENT to TOTAL_INCREASING
    assert sensor.state_class == SensorStateClass.TOTAL_INCREASING

    # Initially 0 until update is processed
    assert sensor.native_value == 0.0

    # Trigger first update
    coordinator.last_successful_update = datetime(2023, 1, 1, 12, 0, 0)
    sensor._handle_coordinator_update()
    assert sensor.native_value == 240.0


def test_switch_port_energy_sensor_accumulation(mock_coordinator_and_device):
    """Test that the energy sensor accumulates value over multiple updates."""
    coordinator, device = mock_coordinator_and_device
    port = device.ports_statuses[0]  # Initially 240 Wh
    config_entry = MagicMock()

    sensor = MerakiSwitchPortEnergySensor(coordinator, device, port, config_entry)
    sensor.async_write_ha_state = MagicMock()

    # 1. First update
    coordinator.last_successful_update = datetime(2023, 1, 1, 12, 0, 0)
    sensor._handle_coordinator_update()
    assert sensor.native_value == 240.0

    # 2. Second update with new data
    # Simulate API returning new data (same object modified for simplicity in mock)
    # Let's say next interval used 100 Wh
    device.ports_statuses[0]["powerUsageInWh"] = 100
    coordinator.last_successful_update = datetime(2023, 1, 1, 12, 5, 0)

    sensor._handle_coordinator_update()
    # Should be 240 + 100 = 340
    assert sensor.native_value == 340.0

    # 3. Duplicate update (same timestamp)
    # Should NOT accumulate
    sensor._handle_coordinator_update()
    assert sensor.native_value == 340.0


async def test_switch_port_energy_sensor_restore():
    """Test that the energy sensor restores state from registry."""
    coordinator = MagicMock()
    device = MerakiDevice(
        serial="Q234-ABCD-5678",
        name="Test Switch",
        model="MS220-8P",
        product_type="switch",
        ports_statuses=[{"portId": "1", "powerUsageInWh": 50}],
    )
    coordinator.data = {"devices": [device]}
    coordinator.get_device.return_value = device
    coordinator.last_successful_update = None

    port = device.ports_statuses[0]
    config_entry = MagicMock()

    sensor = MerakiSwitchPortEnergySensor(coordinator, device, port, config_entry)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()

    # Mock async_get_last_state
    mock_restore = AsyncMock(return_value=State("sensor.test", "1000.5"))
    with patch.object(sensor, "async_get_last_state", mock_restore):
        await sensor.async_added_to_hass()

    # Should have restored 1000.5
    assert sensor.native_value == 1000.5

    # Now verify new update adds to restored value
    coordinator.last_successful_update = datetime(2023, 1, 1, 12, 0, 0)
    sensor._handle_coordinator_update()

    # 1000.5 + 50 = 1050.5
    assert sensor.native_value == 1050.5


def test_switch_port_power_sensor_missing_data(mock_coordinator_and_device):
    """Test the switch port power sensor with missing data."""
    coordinator, device = mock_coordinator_and_device
    port = device.ports_statuses[2]  # No powerUsageInWh
    config_entry = MagicMock()

    sensor = MerakiSwitchPortPowerSensor(coordinator, device, port, config_entry)
    sensor.async_write_ha_state = MagicMock()
    sensor._handle_coordinator_update()
    assert sensor.native_value == 0.0


def test_switch_port_energy_sensor_missing_data(mock_coordinator_and_device):
    """Test the switch port energy sensor with missing data."""
    coordinator, device = mock_coordinator_and_device
    port = device.ports_statuses[2]  # No powerUsageInWh
    config_entry = MagicMock()

    sensor = MerakiSwitchPortEnergySensor(coordinator, device, port, config_entry)
    sensor.async_write_ha_state = MagicMock()

    coordinator.last_successful_update = datetime(2023, 1, 1, 12, 0, 0)
    sensor._handle_coordinator_update()

    assert sensor.native_value == 0.0