"""Tests for the Meraki MT sensor."""

from unittest.mock import MagicMock

import pytest
from homeassistant.components.sensor import SensorDeviceClass

from custom_components.meraki_ha.sensor.device.meraki_mt_base import MerakiMtSensor
from custom_components.meraki_ha.sensor_defs.mt_sensors import (
    MT_BATTERY_DESCRIPTION,
    MT_BUTTON_DESCRIPTION,
    MT_TEMPERATURE_DESCRIPTION,
)


@pytest.fixture
def mock_coordinator_mt_sensor(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataCoordinator with MT sensor data."""
    mock_coordinator.data = {
        "devices": [
            {
                "serial": "mt10-1",
                "name": "MT10 Sensor",
                "model": "MT10",
                "productType": "sensor",
                "readings": [
                    {
                        "metric": "temperature",
                        "temperature": {"celsius": 25.5},
                    },
                    {
                        "metric": "humidity",
                        "humidity": {"relativePercentage": 50},
                    },
                    {
                        "metric": "battery",
                        "battery": {"percentage": 95},
                    },
                ],
            },
            {
                "serial": "mt30-1",
                "name": "MT30 Button",
                "model": "MT30",
                "productType": "sensor",
                "readings": [
                    {
                        "metric": "battery",
                        "battery": {"percentage": 88},
                    },
                    {
                        "metric": "button",
                        "button": {"pressType": "short"},
                    },
                ],
            },
        ]
    }
    return mock_coordinator


def test_mt10_temperature_sensor(
    mock_coordinator_mt_sensor: MagicMock,
):
    """Test the MT10 temperature sensor."""
    device_info = mock_coordinator_mt_sensor.data["devices"][0]
    sensor = MerakiMtSensor(
        mock_coordinator_mt_sensor, device_info, MT_TEMPERATURE_DESCRIPTION
    )

    assert sensor.unique_id == "mt10-1_temperature"
    assert sensor.name == "MT10 Sensor Temperature"
    assert sensor.native_value == 25.5
    assert sensor.device_class == SensorDeviceClass.TEMPERATURE
    assert sensor.available is True


def test_mt10_battery_sensor(
    mock_coordinator_mt_sensor: MagicMock,
):
    """Test the MT10 battery sensor."""
    device_info = mock_coordinator_mt_sensor.data["devices"][0]
    sensor = MerakiMtSensor(
        mock_coordinator_mt_sensor, device_info, MT_BATTERY_DESCRIPTION
    )

    assert sensor.unique_id == "mt10-1_battery"
    assert sensor.name == "MT10 Sensor Battery"
    assert sensor.native_value == 95
    assert sensor.device_class == SensorDeviceClass.BATTERY
    assert sensor.available is True


def test_mt30_button_sensor(
    mock_coordinator_mt_sensor: MagicMock,
):
    """Test the MT30 button sensor."""
    device_info = mock_coordinator_mt_sensor.data["devices"][1]
    sensor = MerakiMtSensor(
        mock_coordinator_mt_sensor, device_info, MT_BUTTON_DESCRIPTION
    )

    assert sensor.unique_id == "mt30-1_button"
    assert sensor.name == "MT30 Button Last Button Press"
    assert sensor.native_value == "short"
    assert sensor.available is True


def test_sanitize_value_filters_unknown(
    mock_coordinator_mt_sensor: MagicMock,
):
    """Test that _sanitize_value filters 'unknown' string values."""
    device_info = mock_coordinator_mt_sensor.data["devices"][0]
    sensor = MerakiMtSensor(
        mock_coordinator_mt_sensor, device_info, MT_TEMPERATURE_DESCRIPTION
    )

    # Test filtering of invalid string values
    assert sensor._sanitize_value("unknown") is None
    assert sensor._sanitize_value("unavailable") is None
    assert sensor._sanitize_value("") is None

    # Test that valid values pass through
    assert sensor._sanitize_value(25.5) == 25.5
    assert sensor._sanitize_value(0) == 0
    assert sensor._sanitize_value(None) is None
    assert sensor._sanitize_value("valid_string") == "valid_string"
    assert sensor._sanitize_value(True) is True
    assert sensor._sanitize_value(False) is False


def test_extra_state_attributes_api_source(
    mock_coordinator_mt_sensor: MagicMock,
):
    """Test extra_state_attributes includes data source for API."""
    mock_coordinator_mt_sensor.mqtt_enabled = False
    mock_coordinator_mt_sensor.get_mqtt_last_update = MagicMock(return_value=None)
    mock_coordinator_mt_sensor.last_successful_update = None

    device_info = mock_coordinator_mt_sensor.data["devices"][0]
    sensor = MerakiMtSensor(
        mock_coordinator_mt_sensor, device_info, MT_TEMPERATURE_DESCRIPTION
    )

    attrs = sensor.extra_state_attributes
    assert attrs["data_source"] == "api"


def test_extra_state_attributes_mqtt_pending(
    mock_coordinator_mt_sensor: MagicMock,
):
    """Test extra_state_attributes shows mqtt_pending when enabled but no update."""
    mock_coordinator_mt_sensor.mqtt_enabled = True
    mock_coordinator_mt_sensor.get_mqtt_last_update = MagicMock(return_value=None)
    mock_coordinator_mt_sensor.last_successful_update = None

    device_info = mock_coordinator_mt_sensor.data["devices"][0]
    sensor = MerakiMtSensor(
        mock_coordinator_mt_sensor, device_info, MT_TEMPERATURE_DESCRIPTION
    )

    attrs = sensor.extra_state_attributes
    assert attrs["data_source"] == "mqtt_pending"
