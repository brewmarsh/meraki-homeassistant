"""Tests for the Meraki camera person detection sensor."""

import time
from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.binary_sensor.device.camera_person import (
    MerakiPersonSensor,
)


@pytest.mark.asyncio
async def test_person_sensor_on(mock_coordinator, mock_config_entry):
    """Test the person sensor when a person is detected."""
    # Arrange
    mock_device = MagicMock()
    mock_device.serial = "ABC"
    mock_device.last_person_detected_event = {"timestamp": time.time(), "alertData": {}}

    mock_coordinator.get_device.return_value = mock_device
    mock_coordinator.data = {"devices": [mock_device]}

    sensor = MerakiPersonSensor(
        mock_coordinator, mock_device, MagicMock(), mock_config_entry
    )

    # Assert
    assert sensor.is_on is True
    assert (
        sensor.extra_state_attributes["last_person_detected_event"]
        == mock_device.last_person_detected_event
    )


@pytest.mark.asyncio
async def test_person_sensor_off(mock_coordinator, mock_config_entry):
    """Test the person sensor when no person is detected."""
    # Arrange
    mock_device = MagicMock()
    mock_device.serial = "ABC"
    mock_device.last_person_detected_event = None

    mock_coordinator.get_device.return_value = mock_device
    mock_coordinator.data = {"devices": [mock_device]}

    sensor = MerakiPersonSensor(
        mock_coordinator, mock_device, MagicMock(), mock_config_entry
    )

    # Assert
    assert sensor.is_on is False


@pytest.mark.asyncio
async def test_person_sensor_stale(mock_coordinator, mock_config_entry):
    """Test the person sensor when detection is stale."""
    # Arrange
    mock_device = MagicMock()
    mock_device.serial = "ABC"
    # 40 seconds ago (threshold is 30s)
    mock_device.last_person_detected_event = {
        "timestamp": time.time() - 40,
        "alertData": {},
    }

    mock_coordinator.get_device.return_value = mock_device
    mock_coordinator.data = {"devices": [mock_device]}

    sensor = MerakiPersonSensor(
        mock_coordinator, mock_device, MagicMock(), mock_config_entry
    )

    # Assert
    assert sensor.is_on is False
