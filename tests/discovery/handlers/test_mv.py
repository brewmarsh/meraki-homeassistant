"""Tests for the MVHandler (Camera)."""

from typing import cast
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.const import CONF_ENABLE_CAMERA_ENTITIES
from custom_components.meraki_ha.discovery.handlers.mv import MVHandler
from custom_components.meraki_ha.types import MerakiDevice
from tests.const import MOCK_CAMERA_DEVICE

# Cast the mock device to proper type
_CAMERA_DEVICE = cast(MerakiDevice, MOCK_CAMERA_DEVICE)


@pytest.fixture
def mock_mv_coordinator(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a coordinator with camera device data."""
    mock_coordinator.data = {"devices": [dict(MOCK_CAMERA_DEVICE)]}
    return mock_coordinator


@pytest.fixture
def mock_camera_service() -> AsyncMock:
    """Fixture for a mocked CameraService."""
    service = AsyncMock()
    service.get_supported_analytics = AsyncMock(return_value=[])
    return service


@pytest.fixture
def mock_control_service() -> MagicMock:
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


@pytest.fixture
def mock_network_control_service() -> MagicMock:
    """Fixture for a mock NetworkControlService."""
    return MagicMock()


@pytest.mark.asyncio
async def test_mv_handler_initialization(
    mock_mv_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
    mock_network_control_service: MagicMock,
) -> None:
    """Test MVHandler initializes correctly."""
    handler = MVHandler(
        mock_mv_coordinator,
        _CAMERA_DEVICE,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    assert handler._coordinator is mock_mv_coordinator
    assert handler.device == _CAMERA_DEVICE
    assert handler._camera_service is mock_camera_service
    assert handler._control_service is mock_control_service


@pytest.mark.asyncio
async def test_mv_handler_discover_entities_basic(
    mock_mv_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
    mock_network_control_service: MagicMock,
) -> None:
    """Test discover_entities returns base entities."""
    mock_config_entry.options = {CONF_ENABLE_CAMERA_ENTITIES: True}
    mock_camera_service.get_supported_analytics.return_value = []

    handler = MVHandler(
        mock_mv_coordinator,
        _CAMERA_DEVICE,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

    # Should create: Camera, MotionSensor, SnapshotButton, SenseStatus, etc.
    assert len(entities) >= 6

    entity_types = [type(e).__name__ for e in entities]
    assert "MerakiCamera" in entity_types
    assert "MerakiMotionSensor" in entity_types
    assert "MerakiSnapshotButton" in entity_types
    assert "MerakiCameraSenseStatusSensor" in entity_types
    assert "MerakiCameraAudioDetectionSensor" in entity_types
    assert "MerakiFirmwareStatusSensor" in entity_types


@pytest.mark.asyncio
async def test_mv_handler_discover_entities_with_person_detection(
    mock_mv_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
    mock_network_control_service: MagicMock,
) -> None:
    """Test discover_entities includes person count sensor when available."""
    mock_config_entry.options = {CONF_ENABLE_CAMERA_ENTITIES: True}
    mock_camera_service.get_supported_analytics.return_value = ["person_detection"]

    handler = MVHandler(
        mock_mv_coordinator,
        _CAMERA_DEVICE,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

    entity_types = [type(e).__name__ for e in entities]
    assert "MerakiPersonCountSensor" in entity_types


@pytest.mark.asyncio
async def test_mv_handler_discover_entities_with_vehicle_detection(
    mock_mv_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
    mock_network_control_service: MagicMock,
) -> None:
    """Test discover_entities includes vehicle count sensor when available."""
    mock_config_entry.options = {CONF_ENABLE_CAMERA_ENTITIES: True}
    mock_camera_service.get_supported_analytics.return_value = ["vehicle_detection"]

    handler = MVHandler(
        mock_mv_coordinator,
        _CAMERA_DEVICE,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

    entity_types = [type(e).__name__ for e in entities]
    assert "MerakiVehicleCountSensor" in entity_types


@pytest.mark.asyncio
async def test_mv_handler_discover_entities_with_both_detections(
    mock_mv_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
    mock_network_control_service: MagicMock,
) -> None:
    """Test discover_entities includes both person and vehicle sensors."""
    mock_config_entry.options = {CONF_ENABLE_CAMERA_ENTITIES: True}
    mock_camera_service.get_supported_analytics.return_value = [
        "person_detection",
        "vehicle_detection",
    ]

    handler = MVHandler(
        mock_mv_coordinator,
        _CAMERA_DEVICE,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

    entity_types = [type(e).__name__ for e in entities]
    assert "MerakiPersonCountSensor" in entity_types
    assert "MerakiVehicleCountSensor" in entity_types


@pytest.mark.asyncio
async def test_mv_handler_discover_entities_disabled(
    mock_mv_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
    mock_network_control_service: MagicMock,
) -> None:
    """Test discover_entities returns empty when camera entities disabled."""
    mock_config_entry.options = {CONF_ENABLE_CAMERA_ENTITIES: False}

    handler = MVHandler(
        mock_mv_coordinator,
        _CAMERA_DEVICE,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

    assert len(entities) == 0


@pytest.mark.asyncio
async def test_mv_handler_create_factory_method(
    mock_mv_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
    mock_network_control_service: MagicMock,
) -> None:
    """Test MVHandler.create factory method."""
    handler = MVHandler.create(
        mock_mv_coordinator,
        _CAMERA_DEVICE,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    assert isinstance(handler, MVHandler)
    assert handler._coordinator is mock_mv_coordinator
    assert handler.device == _CAMERA_DEVICE
