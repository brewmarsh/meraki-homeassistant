"""Tests for the Meraki MT sensor setup."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.sensor.setup_mt_sensors import async_setup_mt_sensors


@pytest.fixture
def mock_coordinator_with_mt_devices(mock_coordinator: MagicMock) -> MagicMock:
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataCoordinator with MT sensor data."""
=======
    """Fixture for a mocked MerakiDataUpdateCoordinator with MT sensor data."""
>>>>>>> origin/beta
    mock_coordinator.data = {
        "devices": [
            {
                "serial": "mt10-1",
                "name": "MT10 Sensor",
                "model": "MT10",
                "productType": "sensor",
                "readings": [
                    {"metric": "temperature", "temperature": {"celsius": 25.5}},
                    {"metric": "humidity", "humidity": {"relativePercentage": 60.0}},
                ],
            },
            {
                "serial": "mt15-1",
                "name": "MT15 Sensor",
                "model": "MT15",
                "productType": "sensor",
                "readings": [
                    {"metric": "temperature", "temperature": {"celsius": 22.1}},
                    {"metric": "humidity", "humidity": {"relativePercentage": 45.2}},
                    {"metric": "co2", "co2": {"concentration": 450}},
                    {"metric": "tvoc", "tvoc": {"concentration": 150}},
                    {"metric": "pm25", "pm25": {"concentration": 10.5}},
                    {"metric": "noise", "noise": {"ambient": {"level": 35.2}}},
                ],
            },
            {
                "serial": "mt12-1",
                "name": "MT12 Sensor",
                "model": "MT12",
                "productType": "sensor",
                "readings": [
                    {"metric": "water", "water": {"present": False}},
                ],
            },
            {
                "serial": "mt40-1",
                "name": "MT40 Power Controller",
                "model": "MT40",
                "productType": "sensor",
                "readings": [
                    {"metric": "power", "power": {"draw": 120.5}},
                    {"metric": "voltage", "voltage": {"level": 120.1}},
                    {"metric": "current", "current": {"draw": 1.0}},
                ],
            },
        ]
    }
    return mock_coordinator


def test_async_setup_mt10_sensors(
    mock_coordinator_with_mt_devices: MagicMock,
) -> None:
    """Test the setup of sensors for an MT10 device."""
    device_info = mock_coordinator_with_mt_devices.data["devices"][0]
    entities = async_setup_mt_sensors(mock_coordinator_with_mt_devices, device_info)
<<<<<<< HEAD

    assert len(entities) == 2
=======
    for entity in entities:
        entity._handle_coordinator_update()

    assert len(entities) == 3
>>>>>>> origin/beta

    sensors_by_key = {entity.entity_description.key: entity for entity in entities}

    # Test Temperature Sensor
    assert "temperature" in sensors_by_key
    temp_sensor = sensors_by_key["temperature"]
    assert temp_sensor.unique_id == "mt10-1_temperature"
    assert temp_sensor.name == "MT10 Sensor Temperature"
<<<<<<< HEAD
    assert temp_sensor.native_value == 25.5  # type: ignore[attr-defined]
=======
    assert temp_sensor.native_value == 25.5
>>>>>>> origin/beta
    assert temp_sensor.available is True

    # Test Humidity Sensor
    assert "humidity" in sensors_by_key
    humidity_sensor = sensors_by_key["humidity"]
    assert humidity_sensor.unique_id == "mt10-1_humidity"
    assert humidity_sensor.name == "MT10 Sensor Humidity"
<<<<<<< HEAD
    assert humidity_sensor.native_value == 60.0  # type: ignore[attr-defined]
=======
    assert humidity_sensor.native_value == 60.0
>>>>>>> origin/beta
    assert humidity_sensor.available is True


def test_async_setup_mt15_sensors(
    mock_coordinator_with_mt_devices: MagicMock,
) -> None:
    """Test the setup of sensors for an MT15 device."""
    device_info = mock_coordinator_with_mt_devices.data["devices"][1]
    entities = async_setup_mt_sensors(mock_coordinator_with_mt_devices, device_info)
<<<<<<< HEAD

    assert len(entities) == 6
=======
    for entity in entities:
        entity._handle_coordinator_update()

    assert len(entities) == 7
>>>>>>> origin/beta

    sensors_by_key = {entity.entity_description.key: entity for entity in entities}

    # Verify Temperature Sensor
    temp_sensor = sensors_by_key.get("temperature")
    assert temp_sensor is not None
    assert temp_sensor.unique_id == "mt15-1_temperature"
    assert temp_sensor.name == "MT15 Sensor Temperature"
<<<<<<< HEAD
    assert temp_sensor.native_value == 22.1  # type: ignore[attr-defined]
=======
    assert temp_sensor.native_value == 22.1
>>>>>>> origin/beta
    assert temp_sensor.available is True

    # Verify Humidity Sensor
    humidity_sensor = sensors_by_key.get("humidity")
    assert humidity_sensor is not None
    assert humidity_sensor.unique_id == "mt15-1_humidity"
    assert humidity_sensor.name == "MT15 Sensor Humidity"
<<<<<<< HEAD
    assert humidity_sensor.native_value == 45.2  # type: ignore[attr-defined]
=======
    assert humidity_sensor.native_value == 45.2
>>>>>>> origin/beta
    assert humidity_sensor.available is True

    # Verify CO2 Sensor
    co2_sensor = sensors_by_key.get("co2")
    assert co2_sensor is not None
    assert co2_sensor.unique_id == "mt15-1_co2"
    assert co2_sensor.name == "MT15 Sensor CO2"
<<<<<<< HEAD
    assert co2_sensor.native_value == 450  # type: ignore[attr-defined]
=======
    assert co2_sensor.native_value == 450
>>>>>>> origin/beta
    assert co2_sensor.available is True

    # Verify TVOC Sensor
    tvoc_sensor = sensors_by_key.get("tvoc")
    assert tvoc_sensor is not None
    assert tvoc_sensor.unique_id == "mt15-1_tvoc"
    assert tvoc_sensor.name == "MT15 Sensor TVOC"
<<<<<<< HEAD
    assert tvoc_sensor.native_value == 150  # type: ignore[attr-defined]
=======
    assert tvoc_sensor.native_value == 150
>>>>>>> origin/beta
    assert tvoc_sensor.available is True

    # Verify PM2.5 Sensor
    pm25_sensor = sensors_by_key.get("pm25")
    assert pm25_sensor is not None
    assert pm25_sensor.unique_id == "mt15-1_pm25"
    assert pm25_sensor.name == "MT15 Sensor PM2.5"
<<<<<<< HEAD
    assert pm25_sensor.native_value == 10.5  # type: ignore[attr-defined]
=======
    assert pm25_sensor.native_value == 10.5
>>>>>>> origin/beta
    assert pm25_sensor.available is True

    # Verify Noise Sensor
    noise_sensor = sensors_by_key.get("noise")
    assert noise_sensor is not None
    assert noise_sensor.unique_id == "mt15-1_noise"
    assert noise_sensor.name == "MT15 Sensor Ambient Noise"
<<<<<<< HEAD
    assert noise_sensor.native_value == 35.2  # type: ignore[attr-defined]
=======
    assert noise_sensor.native_value == 35.2
>>>>>>> origin/beta
    assert noise_sensor.available is True


def test_async_setup_mt12_sensors(
    mock_coordinator_with_mt_devices: MagicMock,
) -> None:
    """Test the setup of sensors for an MT12 device."""
    device_info = mock_coordinator_with_mt_devices.data["devices"][2]
    entities = async_setup_mt_sensors(mock_coordinator_with_mt_devices, device_info)
<<<<<<< HEAD

    assert len(entities) == 1
    water_sensor = entities[0]
    assert water_sensor.unique_id == "mt12-1_water"
    assert water_sensor.name == "MT12 Sensor Water Detection"
    assert water_sensor.native_value is False  # type: ignore[attr-defined]
=======
    for entity in entities:
        entity._handle_coordinator_update()

    assert len(entities) == 2
    water_sensor = entities[0]
    assert water_sensor.unique_id == "mt12-1_water"
    assert water_sensor.name == "MT12 Sensor Water Detection"
    assert water_sensor.native_value is False
>>>>>>> origin/beta
    assert water_sensor.available is True


def test_async_setup_mt40_sensors(
    mock_coordinator_with_mt_devices: MagicMock,
) -> None:
    """Test the setup of sensors for an MT40 device."""
    device_info = mock_coordinator_with_mt_devices.data["devices"][3]
    entities = async_setup_mt_sensors(mock_coordinator_with_mt_devices, device_info)
<<<<<<< HEAD
=======
    for entity in entities:
        entity._handle_coordinator_update()
>>>>>>> origin/beta

    assert len(entities) == 3

    sensors_by_key = {entity.entity_description.key: entity for entity in entities}

    # Verify Power Sensor
    power_sensor = sensors_by_key.get("power")
    assert power_sensor is not None
    assert power_sensor.unique_id == "mt40-1_power"
    assert power_sensor.name == "MT40 Power Controller Power"
<<<<<<< HEAD
    assert power_sensor.native_value == 120.5  # type: ignore[attr-defined]
=======
    assert power_sensor.native_value == 120.5
>>>>>>> origin/beta
    assert power_sensor.available is True

    # Verify Voltage Sensor
    voltage_sensor = sensors_by_key.get("voltage")
    assert voltage_sensor is not None
    assert voltage_sensor.unique_id == "mt40-1_voltage"
    assert voltage_sensor.name == "MT40 Power Controller Voltage"
<<<<<<< HEAD
    assert voltage_sensor.native_value == 120.1  # type: ignore[attr-defined]
=======
    assert voltage_sensor.native_value == 120.1
>>>>>>> origin/beta
    assert voltage_sensor.available is True

    # Verify Current Sensor
    current_sensor = sensors_by_key.get("current")
    assert current_sensor is not None
    assert current_sensor.unique_id == "mt40-1_current"
    assert current_sensor.name == "MT40 Power Controller Current"
<<<<<<< HEAD
    assert current_sensor.native_value == 1.0  # type: ignore[attr-defined]
=======
    assert current_sensor.native_value == 1.0
>>>>>>> origin/beta
    assert current_sensor.available is True


def test_availability(mock_coordinator_with_mt_devices: MagicMock) -> None:
    """Test sensor availability."""
    device_info = mock_coordinator_with_mt_devices.data["devices"][0]  # MT10
    entities = async_setup_mt_sensors(mock_coordinator_with_mt_devices, device_info)
    temp_sensor = entities[0]
<<<<<<< HEAD
=======
    temp_sensor._handle_coordinator_update()
>>>>>>> origin/beta

    # Sensor should be available
    assert temp_sensor.available is True

    # Remove readings and check availability
    device_info["readings"] = []
<<<<<<< HEAD
=======
    temp_sensor._handle_coordinator_update()
>>>>>>> origin/beta
    assert temp_sensor.available is False

    # No readings key
    del device_info["readings"]
<<<<<<< HEAD
=======
    temp_sensor._handle_coordinator_update()
>>>>>>> origin/beta
    assert temp_sensor.available is False
