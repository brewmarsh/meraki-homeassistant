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
        ]
    }
    return coordinator


def test_async_setup_mt10_sensors(mock_coordinator):
    """Test the setup of sensors for an MT10 device."""
    device_info = mock_coordinator.data["devices"][0]
    entities = async_setup_mt_sensors(mock_coordinator, device_info)

    assert len(entities) == 1
    temp_sensor = entities[0]
    assert temp_sensor.unique_id == "mt10-1_temperature"
    assert temp_sensor.name == "MT10 Sensor Temperature"
    assert temp_sensor.native_value == 25.5
    assert temp_sensor.available is True


def test_async_setup_mt15_sensors(mock_coordinator):
    """Test the setup of sensors for an MT15 device."""
    device_info = mock_coordinator.data["devices"][1]
    entities = async_setup_mt_sensors(mock_coordinator, device_info)

    assert len(entities) == 6

    expected_sensors = {
        "temperature": 22.1,
        "humidity": 45.2,
        "co2": 450,
        "tvoc": 150,
        "pm25": 10.5,
        "noise": 35.2,
    }

    for entity in entities:
        metric = entity.entity_description.key
        assert metric in expected_sensors
        assert entity.unique_id == f"mt15-1_{metric}"
        assert entity.native_value == expected_sensors[metric]
        assert entity.available is True


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
