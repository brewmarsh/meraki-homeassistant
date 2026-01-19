"""Tests for the Meraki camera motion sensor."""

import dataclasses
from unittest.mock import AsyncMock

import pytest

from custom_components.meraki_ha.binary_sensor.device.camera_motion import (
    MerakiMotionSensor,
)
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    service = AsyncMock()
    service.get_motion_history = AsyncMock(
        return_value=[{"type": "person", "ts": "2022-01-01T00:00:00Z"}]
    )
    return service


@pytest.mark.asyncio
async def test_motion_sensor_on(
    mock_coordinator, mock_camera_service, mock_config_entry
):
    """Test the motion sensor when motion is detected."""
    # Arrange
    device = dataclasses.replace(MOCK_DEVICE)
    sensor = MerakiMotionSensor(
        mock_coordinator, device, mock_camera_service, mock_config_entry
    )

    # Act
    await sensor.async_update()

    # Assert
    assert sensor.is_on is True
    assert sensor.extra_state_attributes["motion_events"] == [
        {"type": "person", "ts": "2022-01-01T00:00:00Z"}
    ]


@pytest.mark.asyncio
async def test_motion_sensor_off(
    mock_coordinator, mock_camera_service, mock_config_entry
):
    """Test the motion sensor when no motion is detected."""
    # Arrange
    device = dataclasses.replace(MOCK_DEVICE)
    mock_camera_service.get_motion_history.return_value = []
    sensor = MerakiMotionSensor(
        mock_coordinator, device, mock_camera_service, mock_config_entry
    )

    # Act
    await sensor.async_update()

    # Assert
    assert sensor.is_on is False
    assert sensor.extra_state_attributes["motion_events"] == []
