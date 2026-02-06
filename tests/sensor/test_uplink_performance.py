"""Tests for the Meraki uplink performance sensor."""

from unittest.mock import MagicMock
import pytest
from homeassistant.const import PERCENTAGE, UnitOfTime
from custom_components.meraki_ha.sensor.uplink_performance import MerakiUplinkPerformanceSensor
from custom_components.meraki_ha.core.models.device import MerakiDevice
from homeassistant.components.sensor import SensorEntityDescription

@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    return coordinator

def test_uplink_performance_sensor_mapping(mock_coordinator):
    """Test the uplink performance sensor mapping and units."""
    device = MerakiDevice(serial="dev1", name="Appliance")
    device.uplinks = [
        {"interface": "wan1", "latencyMs": 10, "packetLoss": 0.5, "jitter": 2}
    ]
    mock_coordinator.get_device.return_value = device

    # Test latency with API 2.0 key
    desc = SensorEntityDescription(key="wan1_latency", name="Wan1 latency")
    sensor = MerakiUplinkPerformanceSensor(mock_coordinator, device, MagicMock(), "wan1", "latencyMs", desc)
    assert sensor.native_value == 10.0
    assert sensor.native_unit_of_measurement == UnitOfTime.MILLISECONDS

    # Test jitter unit
    desc_jitter = SensorEntityDescription(key="wan1_jitter", name="WAN1 Jitter")
    sensor_jitter = MerakiUplinkPerformanceSensor(mock_coordinator, device, MagicMock(), "wan1", "jitter", desc_jitter)
    assert sensor_jitter.native_unit_of_measurement == UnitOfTime.MILLISECONDS

    # Test packet loss unit
    desc_loss = SensorEntityDescription(key="wan1_loss", name="WAN1 Loss")
    sensor_loss = MerakiUplinkPerformanceSensor(mock_coordinator, device, MagicMock(), "wan1", "packetLoss", desc_loss)
    assert sensor_loss.native_value == 0.5
    assert sensor_loss.native_unit_of_measurement == PERCENTAGE

def test_uplink_performance_sensor_none_handling(mock_coordinator):
    """Test handling of None and invalid values."""
    device = MerakiDevice(serial="dev1", name="Appliance")
    device.uplinks = [{"interface": "wan1", "latencyMs": None}]
    mock_coordinator.get_device.return_value = device

    desc = SensorEntityDescription(key="wan1_latency", name="Wan1 latency")
    sensor = MerakiUplinkPerformanceSensor(mock_coordinator, device, MagicMock(), "wan1", "latencyMs", desc)
    assert sensor.native_value is None

    # Invalid value
    device.uplinks = [{"interface": "wan1", "latencyMs": "invalid"}]
    sensor._update_state()
    assert sensor.native_value is None
