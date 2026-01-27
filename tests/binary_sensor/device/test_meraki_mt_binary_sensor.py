"""Tests for the Meraki MT binary sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.binary_sensor.device.meraki_mt_binary_base import (
    MerakiMtBinarySensor,
)
from custom_components.meraki_ha.sensor_defs.mt_sensors import (
    MT_DOOR_DESCRIPTION,
    MT_WATER_DESCRIPTION,
)


@pytest.fixture
def mock_coordinator_mt_binary(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataCoordinator with MT binary data."""
    mock_coordinator.data = {
        "devices": [
            {
                "serial": "mt20-1",
                "name": "MT20 Sensor",
                "model": "MT20",
                "productType": "sensor",
                "readings": [
                    {
                        "metric": "door",
                        "door": {"open": True},
                    },  # Door is open
                    {
                        "metric": "temperature",
                        "temperature": {"celsius": 20.0},
                    },
                ],
            },
            {
                "serial": "mt12-1",
                "name": "MT12 Sensor",
                "model": "MT12",
                "productType": "sensor",
                "readings": [
                    {
                        "metric": "water",
                        "water": {"present": True},
                    },  # Water detected
                ],
            },
            {
                "serial": "mt12-2",
                "name": "MT12 Sensor Dry",
                "model": "MT12",
                "productType": "sensor",
                "readings": [
                    {
                        "metric": "water",
                        "water": {"present": False},
                    },  # Dry
                ],
            },
        ]
    }
    return mock_coordinator


def test_mt20_open_sensor(
    mock_coordinator_mt_binary: MagicMock,
):
    """Test the MT20 open/close sensor when the door is open."""
    device_info = mock_coordinator_mt_binary.data["devices"][0]
    sensor = MerakiMtBinarySensor(
        mock_coordinator_mt_binary, device_info, MT_DOOR_DESCRIPTION
    )

    assert sensor.unique_id == "mt20-1_door"
    assert sensor.name == "MT20 Sensor Door"
    assert sensor.is_on is True
    assert sensor.available is True


def test_mt12_water_sensor(
    mock_coordinator_mt_binary: MagicMock,
):
    """Test the MT12 water sensor when water is present."""
    device_info = mock_coordinator_mt_binary.data["devices"][1]
    sensor = MerakiMtBinarySensor(
        mock_coordinator_mt_binary, device_info, MT_WATER_DESCRIPTION
    )

    assert sensor.unique_id == "mt12-1_water"
    assert sensor.name == "MT12 Sensor Water Leak"
    assert sensor.is_on is True
    assert sensor.available is True


def test_mt12_dry_sensor(
    mock_coordinator_mt_binary: MagicMock,
):
    """Test the MT12 water sensor when it is dry."""
    device_info = mock_coordinator_mt_binary.data["devices"][2]
    sensor = MerakiMtBinarySensor(
        mock_coordinator_mt_binary, device_info, MT_WATER_DESCRIPTION
    )

    assert sensor.unique_id == "mt12-2_water"
    assert sensor.name == "MT12 Sensor Dry Water Leak"
    assert sensor.is_on is False
    assert sensor.available is True


def test_sensor_availability(
    mock_coordinator_mt_binary: MagicMock,
):
    """Test sensor availability."""
    device_info = mock_coordinator_mt_binary.data["devices"][0]
    # Remove readings to test unavailability
    device_info_no_readings = device_info.copy()
    device_info_no_readings["readings"] = []

    sensor = MerakiMtBinarySensor(
        mock_coordinator_mt_binary, device_info_no_readings, MT_DOOR_DESCRIPTION
    )
    assert sensor.available is False

    # Test with readings but missing specific metric
    device_info_missing_metric = device_info.copy()
    device_info_missing_metric["readings"] = [
        {
            "metric": "temperature",
            "temperature": {"celsius": 20.0},
        }
    ]
    sensor = MerakiMtBinarySensor(
        mock_coordinator_mt_binary, device_info_missing_metric, MT_DOOR_DESCRIPTION
    )
    assert sensor.available is False
