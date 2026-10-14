"""Tests for the Meraki camera analytics sensors."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.sensor.device.camera_analytics import (
    MerakiPersonCountSensor,
    MerakiVehicleCountSensor,
)
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiMainCoordinator."""
    return MagicMock()


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    service = AsyncMock()
    service.get_analytics_data = AsyncMock(return_value=[{"person": 5, "vehicle": 2}])
    return service


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
        camera_analytics=[{"zoneId": 0, "person_count": 5}],
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
        camera_analytics=[{"zoneId": 0, "vehicle_count": 10}],
    )
    mock_coordinator.get_device.return_value = device
    sensor = MerakiVehicleCountSensor(mock_coordinator, device)

    # Act
    # The value is updated through the coordinator, so no need to call async_update

    # Assert
    assert sensor.native_value == 10


@pytest.mark.asyncio
async def test_independent_imager_analytics(mock_coordinator):
    """Test that two imagers of the same unit have independent sensors."""
    # Unit base serial: QXXX-XXXX-XXXX
    imager1 = MerakiDevice(
        serial="QXXX-XXXX-XXXX-1",
        model="MV84X",
        product_type="camera",
        camera_analytics=[{"zoneId": 0, "person_count": 3}],
    )
    imager2 = MerakiDevice(
        serial="QXXX-XXXX-XXXX-2",
        model="MV84X",
        product_type="camera",
        camera_analytics=[{"zoneId": 0, "person_count": 7}],
    )

    def side_effect(serial):
        if serial == "QXXX-XXXX-XXXX-1":
            return imager1
        if serial == "QXXX-XXXX-XXXX-2":
            return imager2
        return None

    mock_coordinator.get_device.side_effect = side_effect

    sensor1 = MerakiPersonCountSensor(mock_coordinator, imager1)
    sensor2 = MerakiPersonCountSensor(mock_coordinator, imager2)

    # Unique IDs should be distinct (using the full serial)
    assert sensor1.unique_id == "QXXX-XXXX-XXXX-1-person-count"
    assert sensor2.unique_id == "QXXX-XXXX-XXXX-2-person-count"

    # Values should be independent
    assert sensor1.native_value == 3
    assert sensor2.native_value == 7
