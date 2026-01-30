"""Tests for the Meraki MT sensor."""

from unittest.mock import MagicMock

import pytest
from homeassistant.components.sensor import SensorDeviceClass

from custom_components.meraki_ha.descriptions import (
    MT_BATTERY_DESCRIPTION,
    MT_BUTTON_DESCRIPTION,
    MT_TEMPERATURE_DESCRIPTION,
)
from custom_components.meraki_ha.sensor.device.meraki_mt_base import MerakiMtSensor
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_coordinator_mt_sensor(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataCoordinator with MT sensor data."""
    devices_data = [
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

    # Convert to objects
    devices = [MerakiDevice.from_dict(d) for d in devices_data]

    mock_coordinator.data = {
        "devices": devices
    }

    # Also mock get_device to return the device object
    def get_device(serial):
        for d in devices:
            if d.serial == serial:
                return d
        return None
    mock_coordinator.get_device.side_effect = get_device

    return mock_coordinator


def test_mt10_temperature_sensor(
    mock_coordinator_mt_sensor: MagicMock,
):
    """Test the MT10 temperature sensor."""
    device_info = mock_coordinator_mt_sensor.data["devices"][0]
    sensor = MerakiMtSensor(
        mock_coordinator_mt_sensor, device_info, MT_TEMPERATURE_DESCRIPTION
    )
    sensor.hass = MagicMock()
    sensor.entity_id = "sensor.mt10_temperature"
    object.__setattr__(sensor, "async_write_ha_state", MagicMock())

    # Force update logic since __init__ doesn't do it
    sensor._handle_coordinator_update()

    assert sensor.unique_id == "mt10-1_temperature"
    assert sensor.name == "Temperature"
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
    sensor.hass = MagicMock()
    sensor.entity_id = "sensor.mt10_battery"
    object.__setattr__(sensor, "async_write_ha_state", MagicMock())

    sensor._handle_coordinator_update()

    assert sensor.unique_id == "mt10-1_battery"
    assert sensor.name == "Battery" # Updated expectation
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
    sensor.hass = MagicMock()
    sensor.entity_id = "sensor.mt30_button"
    object.__setattr__(sensor, "async_write_ha_state", MagicMock())

    sensor._handle_coordinator_update()

    assert sensor.unique_id == "mt30-1_button"
    assert sensor.name == "Last Button Press" # Updated expectation
    assert sensor.native_value == "short"
    assert sensor.available is True
