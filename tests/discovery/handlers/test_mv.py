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
def mock_mv_coordinator() -> MagicMock:
    """Fixture for a coordinator with camera device data."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [dict(MOCK_CAMERA_DEVICE)]}
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {"device_name_format": "prefix"}
    return coordinator


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
async def test_mv_handler_discover_entities_disabled_returns_empty(
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

    # When disabled, no entities should be created
    assert len(entities) == 0


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
