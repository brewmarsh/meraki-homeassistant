"""Tests for the Meraki MT20 open/close binary sensor."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.binary_sensor.device.mt20_open_close import (
    MerakiMt20OpenCloseSensor,
)


@pytest.fixture
def mock_coordinator_mt20(mock_coordinator: MagicMock) -> MagicMock:
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataUpdateCoordinator with MT20 data."""
=======
    """Fixture for a mocked MerakiDataCoordinator with MT20 data."""
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
    mock_coordinator.data = {
        "devices": [
            {
                "serial": "mt20-1",
                "name": "MT20 Sensor",
                "model": "MT20",
                "productType": "sensor",
                "readings": [
                    {"metric": "door", "value": True},  # Door is open
                ],
            },
            {
                "serial": "mt20-2",
                "name": "MT20 Sensor Closed",
                "model": "MT20",
                "productType": "sensor",
                "readings": [
                    {"metric": "door", "value": False},  # Door is closed
                ],
            },
        ]
    }
    return mock_coordinator


def test_mt20_open_sensor(
    mock_coordinator_mt20: MagicMock, mock_config_entry: MagicMock
):
    """Test the MT20 open/close sensor when the door is open."""
    device_info = mock_coordinator_mt20.data["devices"][0]
    sensor = MerakiMt20OpenCloseSensor(
        mock_coordinator_mt20, device_info, mock_config_entry
    )

    assert sensor.unique_id == "mt20-1-door"
    assert sensor.name == "MT20 Sensor Door"
    assert sensor.is_on is True
    assert sensor.available is True


def test_mt20_closed_sensor(
    mock_coordinator_mt20: MagicMock, mock_config_entry: MagicMock
):
    """Test the MT20 open/close sensor when the door is closed."""
    device_info = mock_coordinator_mt20.data["devices"][1]
    sensor = MerakiMt20OpenCloseSensor(
        mock_coordinator_mt20, device_info, mock_config_entry
    )

    assert sensor.unique_id == "mt20-2-door"
    assert sensor.name == "MT20 Sensor Closed Door"
    assert sensor.is_on is False
    assert sensor.available is True


def test_mt20_availability(
    mock_coordinator_mt20: MagicMock, mock_config_entry: MagicMock
):
    """Test sensor availability for the MT20 sensor."""
    device_info = mock_coordinator_mt20.data["devices"][0]
    sensor = MerakiMt20OpenCloseSensor(
        mock_coordinator_mt20, device_info, mock_config_entry
    )

    # Sensor should be available initially
    assert sensor.available is True

    # Test availability when readings are missing
    device_info["readings"] = []
    assert sensor.available is False

    # Test availability when 'readings' key is absent
    del device_info["readings"]
    assert sensor.available is False
