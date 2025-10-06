"""Tests for the Meraki MT sensor setup."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.setup_mt_sensors import async_setup_mt_sensors


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "mt10-1",
                "name": "MT10 Sensor",
                "model": "MT10",
                "productType": "sensor",
                "readings": [
                    {"metric": "temperature", "value": 25.5},
                    {"metric": "humidity", "value": 60.0},
                ],
            },
            {
                "serial": "mt15-1",
                "name": "MT15 Sensor",
                "model": "MT15",
                "productType": "sensor",
                "readings": [
                    {"metric": "temperature", "value": 22.1},
                    {"metric": "humidity", "value": 45.2},
                    {"metric": "co2", "value": 450},
                    {"metric": "tvoc", "value": 150},
                    {"metric": "pm25", "value": 10.5},
                    {"metric": "noise", "value": 35.2},
                ],
            },
            {
                "serial": "mt12-1",
                "name": "MT12 Sensor",
                "model": "MT12",
                "productType": "sensor",
                "readings": [
                    {"metric": "water", "value": False},
                ],
            },
            {
                "serial": "mt40-1",
                "name": "MT40 Power Controller",
                "model": "MT40",
                "productType": "sensor",
                "readings": [
                    {"metric": "power", "value": 120.5},
                    {"metric": "voltage", "value": 120.1},
                    {"metric": "current", "value": 1.0},
                ],
            },
        ]
    }
    return coordinator


def test_async_setup_mt10_sensors(mock_coordinator):
    """Test the setup of sensors for an MT10 device."""
    device_info = mock_coordinator.data["devices"][0]
    entities = async_setup_mt_sensors(mock_coordinator, device_info)

    assert len(entities) == 2

    sensors_by_key = {entity.entity_description.key: entity for entity in entities}

    # Test Temperature Sensor
    assert "temperature" in sensors_by_key
    temp_sensor = sensors_by_key["temperature"]
    assert temp_sensor.unique_id == "mt10-1_temperature"
    assert temp_sensor.name == "MT10 Sensor Temperature"
    assert temp_sensor.native_value == 25.5
    assert temp_sensor.available is True

    # Test Humidity Sensor
    assert "humidity" in sensors_by_key
    humidity_sensor = sensors_by_key["humidity"]
    assert humidity_sensor.unique_id == "mt10-1_humidity"
    assert humidity_sensor.name == "MT10 Sensor Humidity"
    assert humidity_sensor.native_value == 60.0
    assert humidity_sensor.available is True


def test_async_setup_mt15_sensors(mock_coordinator):
    """Test the setup of sensors for an MT15 device."""
    device_info = mock_coordinator.data["devices"][1]
    entities = async_setup_mt_sensors(mock_coordinator, device_info)

    assert len(entities) == 6

    sensors_by_key = {entity.entity_description.key: entity for entity in entities}

    # Verify Temperature Sensor
    temp_sensor = sensors_by_key.get("temperature")
    assert temp_sensor is not None
    assert temp_sensor.unique_id == "mt15-1_temperature"
    assert temp_sensor.name == "MT15 Sensor Temperature"
    assert temp_sensor.native_value == 22.1
    assert temp_sensor.available is True

    # Verify Humidity Sensor
    humidity_sensor = sensors_by_key.get("humidity")
    assert humidity_sensor is not None
    assert humidity_sensor.unique_id == "mt15-1_humidity"
    assert humidity_sensor.name == "MT15 Sensor Humidity"
    assert humidity_sensor.native_value == 45.2
    assert humidity_sensor.available is True

    # Verify CO2 Sensor
    co2_sensor = sensors_by_key.get("co2")
    assert co2_sensor is not None
    assert co2_sensor.unique_id == "mt15-1_co2"
    assert co2_sensor.name == "MT15 Sensor CO2"
    assert co2_sensor.native_value == 450
    assert co2_sensor.available is True

    # Verify TVOC Sensor
    tvoc_sensor = sensors_by_key.get("tvoc")
    assert tvoc_sensor is not None
    assert tvoc_sensor.unique_id == "mt15-1_tvoc"
    assert tvoc_sensor.name == "MT15 Sensor TVOC"
    assert tvoc_sensor.native_value == 150
    assert tvoc_sensor.available is True

    # Verify PM2.5 Sensor
    pm25_sensor = sensors_by_key.get("pm25")
    assert pm25_sensor is not None
    assert pm25_sensor.unique_id == "mt15-1_pm25"
    assert pm25_sensor.name == "MT15 Sensor PM2.5"
    assert pm25_sensor.native_value == 10.5
    assert pm25_sensor.available is True

    # Verify Noise Sensor
    noise_sensor = sensors_by_key.get("noise")
    assert noise_sensor is not None
    assert noise_sensor.unique_id == "mt15-1_noise"
    assert noise_sensor.name == "MT15 Sensor Ambient Noise"
    assert noise_sensor.native_value == 35.2
    assert noise_sensor.available is True


def test_async_setup_mt12_sensors(mock_coordinator):
    """Test the setup of sensors for an MT12 device."""
    device_info = mock_coordinator.data["devices"][2]
    entities = async_setup_mt_sensors(mock_coordinator, device_info)

    assert len(entities) == 1
    water_sensor = entities[0]
    assert water_sensor.unique_id == "mt12-1_water"
    assert water_sensor.name == "MT12 Sensor Water Detection"
    assert water_sensor.native_value is False
    assert water_sensor.available is True


def test_async_setup_mt40_sensors(mock_coordinator):
    """Test the setup of sensors for an MT40 device."""
    device_info = mock_coordinator.data["devices"][3]
    entities = async_setup_mt_sensors(mock_coordinator, device_info)

    assert len(entities) == 3

    sensors_by_key = {entity.entity_description.key: entity for entity in entities}

    # Verify Power Sensor
    power_sensor = sensors_by_key.get("power")
    assert power_sensor is not None
    assert power_sensor.unique_id == "mt40-1_power"
    assert power_sensor.name == "MT40 Power Controller Power"
    assert power_sensor.native_value == 120.5
    assert power_sensor.available is True

    # Verify Voltage Sensor
    voltage_sensor = sensors_by_key.get("voltage")
    assert voltage_sensor is not None
    assert voltage_sensor.unique_id == "mt40-1_voltage"
    assert voltage_sensor.name == "MT40 Power Controller Voltage"
    assert voltage_sensor.native_value == 120.1
    assert voltage_sensor.available is True

    # Verify Current Sensor
    current_sensor = sensors_by_key.get("current")
    assert current_sensor is not None
    assert current_sensor.unique_id == "mt40-1_current"
    assert current_sensor.name == "MT40 Power Controller Current"
    assert current_sensor.native_value == 1.0
    assert current_sensor.available is True


def test_availability(mock_coordinator):
    """Test sensor availability."""
    device_info = mock_coordinator.data["devices"][0]  # MT10
    entities = async_setup_mt_sensors(mock_coordinator, device_info)
    temp_sensor = entities[0]

    # Sensor should be available
    assert temp_sensor.available is True

    # Remove readings and check availability
    device_info["readings"] = []
    assert temp_sensor.available is False

    # No readings key
    del device_info["readings"]
    assert temp_sensor.available is False
