"""Tests for the MXHandler."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.button.reboot import MerakiRebootButton
from custom_components.meraki_ha.discovery.handlers.mx import MXHandler

from ...const import MOCK_CONFIG_ENTRY, MOCK_MX_DEVICE


@pytest.fixture
def mock_coordinator():
<<<<<<< HEAD
    """Fixture for a mock MerakiDataCoordinator."""
=======
    """Fixture for a mock MerakiDataUpdateCoordinator."""
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    coordinator = MagicMock()
    coordinator.data = {"devices": [MOCK_MX_DEVICE]}
    return coordinator


@pytest.fixture
def mock_control_service():
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    return AsyncMock()


@pytest.mark.asyncio
async def test_discover_entities_creates_reboot_button(
    mock_coordinator, mock_camera_service, mock_control_service
):
    """Test that discover_entities creates a MerakiRebootButton."""
    handler = MXHandler(
        mock_coordinator,
        MOCK_MX_DEVICE,
        MOCK_CONFIG_ENTRY,
        mock_camera_service,
        mock_control_service,
    )

    entities = await handler.discover_entities()

    assert len(entities) == 1
    assert isinstance(entities[0], MerakiRebootButton)
