"""Tests for the MRHandler."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from custom_components.meraki_ha.discovery.handlers.mr import MRHandler
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    return MagicMock()


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked config entry."""
    return MagicMock()


@pytest.fixture
def mock_control_service():
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    return AsyncMock()


@pytest.mark.asyncio
async def test_mr_handler_discover_entities(
    mock_coordinator, mock_config_entry, mock_camera_service, mock_control_service
):
    """Test that the MRHandler's discover_entities returns an empty list (for now)."""
    handler = MRHandler(
        mock_coordinator,
        MOCK_DEVICE,
        mock_config_entry,
        mock_control_service,
    )
    entities = await handler.discover_entities()
    assert entities == []
