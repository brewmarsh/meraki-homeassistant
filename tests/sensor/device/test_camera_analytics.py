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
    """Fixture for a mocked MerakiDataCoordinator."""
=======
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    return MagicMock()


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    service = AsyncMock()
    service.get_analytics_data = AsyncMock(return_value=[{"person": 5, "vehicle": 2}])
    return service


<<<<<<< HEAD
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
=======
from custom_components.meraki_ha.types import MerakiDevice


@pytest.mark.asyncio
async def test_person_count_sensor(mock_coordinator):
    """Test the person count sensor."""
    # Arrange
    device = MerakiDevice(
        serial="test_serial",
        name="Test Camera",
        model="MV22",
        mac="00:11:22:33:44:55",
        lan_ip="1.2.3.4",
        product_type="camera",
        analytics=[{"zoneId": 0, "person_count": 5}],
    )
    mock_coordinator.get_device.return_value = device
    sensor = MerakiPersonCountSensor(mock_coordinator, device)

    # Act
    # The value is updated through the coordinator, so no need to call async_update

    # Assert
    assert sensor.native_value == 5


@pytest.mark.asyncio
async def test_vehicle_count_sensor(mock_coordinator):
    """Test the vehicle count sensor."""
    # Arrange
    device = MerakiDevice(
        serial="test_serial",
        name="Test Camera",
        model="MV22",
        mac="00:11:22:33:44:55",
        lan_ip="1.2.3.4",
        product_type="camera",
        analytics=[{"zoneId": 0, "vehicle_count": 10}],
    )
    mock_coordinator.get_device.return_value = device
    sensor = MerakiVehicleCountSensor(mock_coordinator, device)

    # Act
    # The value is updated through the coordinator, so no need to call async_update

    # Assert
    assert sensor.native_value == 10
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
