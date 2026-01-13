"""Tests for the Meraki camera analytics sensors."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.camera_analytics import (
    MerakiPersonCountSensor,
    MerakiVehicleCountSensor,
)
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator():
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
=======
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
=======
    """Fixture for a mocked MerakiDataCoordinator."""
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
    return MagicMock()


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    service = AsyncMock()
    service.get_analytics_data = AsyncMock(return_value=[{"person": 5, "vehicle": 2}])
    return service


@pytest.mark.asyncio
async def test_person_count_sensor(mock_coordinator, mock_camera_service):
    """Test the person count sensor."""
    # Arrange
    device = MOCK_DEVICE.copy()
    sensor = MerakiPersonCountSensor(mock_coordinator, device, mock_camera_service)

    # Act
    await sensor.async_update()

    # Assert
    assert sensor.native_value == 5
    assert sensor.extra_state_attributes["raw_data"] == [{"person": 5, "vehicle": 2}]


@pytest.mark.asyncio
async def test_vehicle_count_sensor(mock_coordinator, mock_camera_service):
    """Test the vehicle count sensor."""
    # Arrange
    device = MOCK_DEVICE.copy()
    sensor = MerakiVehicleCountSensor(mock_coordinator, device, mock_camera_service)

    # Act
    await sensor.async_update()

    # Assert
    assert sensor.native_value == 2
    assert sensor.extra_state_attributes["raw_data"] == [{"person": 5, "vehicle": 2}]
