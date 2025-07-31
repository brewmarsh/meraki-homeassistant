"""Tests for the Meraki MT environmental sensors."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.device.mt_environmental import (
    MerakiTemperatureSensor,
    MerakiHumiditySensor,
    MerakiWaterDetectionSensor,
)


@pytest.fixture
def mock_device_coordinator():
    """Fixture for a mocked MerakiDeviceCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        'devices': [
            {
                'serial': 'mt1',
                'name': 'MT Sensor',
                'model': 'MT10',
                'productType': 'sensor',
                'readings': [
                    {'metric': 'temperature', 'value': 25.5},
                    {'metric': 'humidity', 'value': 60.2},
                    {'metric': 'water', 'value': False},
                ]
            }
        ]
    }
    return coordinator


def test_mt_environmental_sensors(mock_device_coordinator):
    """Test the MT environmental sensors."""
    device = mock_device_coordinator.data['devices'][0]

    temp_sensor = MerakiTemperatureSensor(mock_device_coordinator, device)
    assert temp_sensor.unique_id == 'mt1_temperature'
    assert temp_sensor.name == 'MT Sensor Temperature'
    assert temp_sensor.native_value == 25.5

    humidity_sensor = MerakiHumiditySensor(mock_device_coordinator, device)
    assert humidity_sensor.unique_id == 'mt1_humidity'
    assert humidity_sensor.name == 'MT Sensor Humidity'
    assert humidity_sensor.native_value == 60.2

    water_sensor = MerakiWaterDetectionSensor(mock_device_coordinator, device)
    assert water_sensor.unique_id == 'mt1_water'
    assert water_sensor.name == 'MT Sensor Water Detection'
    assert water_sensor.native_value is False
