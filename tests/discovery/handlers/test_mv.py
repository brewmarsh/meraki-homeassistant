"""Tests for the MVHandler."""

from unittest.mock import AsyncMock, MagicMock
import pytest

from custom_components.meraki_ha.camera import MerakiCamera
from custom_components.meraki_ha.discovery.handlers.mv import MVHandler
from custom_components.meraki_ha.sensor.device.camera_analytics import (
    MerakiPersonCountSensor,
    MerakiVehicleCountSensor,
)
from custom_components.meraki_ha.binary_sensor.device.camera_motion import (
    MerakiMotionSensor,
)
from custom_components.meraki_ha.button.device.camera_snapshot import (
    MerakiSnapshotButton,
)
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    return MagicMock()


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked config entry."""
    return MagicMock()


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    service = AsyncMock()
    service.get_supported_analytics = AsyncMock(
        return_value=["person_detection", "vehicle_detection"]
    )
    return service


@pytest.fixture
def mock_control_service():
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


@pytest.mark.asyncio
async def test_mv_handler_all_features(
    mock_coordinator, mock_config_entry, mock_camera_service, mock_control_service
):
    """Test that the MVHandler discovers all entities for a capable camera."""
    # Arrange
    device = MOCK_DEVICE.copy()
    handler = MVHandler(mock_coordinator, device, mock_config_entry, mock_camera_service, mock_control_service)

    # Act
    entities = await handler.discover_entities()

    # Assert
    assert len(entities) == 5
    assert any(isinstance(e, MerakiCamera) for e in entities)
    assert any(isinstance(e, MerakiPersonCountSensor) for e in entities)
    assert any(isinstance(e, MerakiVehicleCountSensor) for e in entities)
    assert any(isinstance(e, MerakiMotionSensor) for e in entities)
    assert any(isinstance(e, MerakiSnapshotButton) for e in entities)


@pytest.mark.asyncio
async def test_mv_handler_some_features(
    mock_coordinator, mock_config_entry, mock_camera_service, mock_control_service
):
    """Test that the MVHandler discovers some entities for a less capable camera."""
    # Arrange
    device = MOCK_DEVICE.copy()
    mock_camera_service.get_supported_analytics = AsyncMock(
        return_value=["person_detection"]
    )
    handler = MVHandler(mock_coordinator, device, mock_config_entry, mock_camera_service, mock_control_service)

    # Act
    entities = await handler.discover_entities()

    # Assert
    assert len(entities) == 4
    assert any(isinstance(e, MerakiCamera) for e in entities)
    assert any(isinstance(e, MerakiPersonCountSensor) for e in entities)
    assert not any(isinstance(e, MerakiVehicleCountSensor) for e in entities)
    assert any(isinstance(e, MerakiMotionSensor) for e in entities)
    assert any(isinstance(e, MerakiSnapshotButton) for e in entities)


@pytest.mark.asyncio
async def test_mv_handler_no_extra_features(
    mock_coordinator, mock_config_entry, mock_camera_service, mock_control_service
):
    """Test that the MVHandler discovers only basic entities for a basic camera."""
    # Arrange
    device = MOCK_DEVICE.copy()
    mock_camera_service.get_supported_analytics = AsyncMock(return_value=[])
    handler = MVHandler(mock_coordinator, device, mock_config_entry, mock_camera_service, mock_control_service)

    # Act
    entities = await handler.discover_entities()

    # Assert
    assert len(entities) == 3
    assert any(isinstance(e, MerakiCamera) for e in entities)
    assert not any(isinstance(e, MerakiPersonCountSensor) for e in entities)
    assert not any(isinstance(e, MerakiVehicleCountSensor) for e in entities)
    assert any(isinstance(e, MerakiMotionSensor) for e in entities)
    assert any(isinstance(e, MerakiSnapshotButton) for e in entities)

