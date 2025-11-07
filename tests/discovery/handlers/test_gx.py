"""Tests for the GXHandler."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.button.reboot import MerakiRebootButton
from custom_components.meraki_ha.discovery.handlers.gx import GXHandler

from ...const import MOCK_CONFIG_ENTRY, MOCK_GX_DEVICE


@pytest.fixture
def mock_control_service() -> MagicMock:
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


@pytest.fixture
def mock_camera_service() -> AsyncMock:
    """Fixture for a mocked CameraService."""
    return AsyncMock()


@pytest.mark.asyncio
async def test_discover_entities_creates_reboot_button(
    mock_coordinator: MagicMock,
    mock_camera_service: AsyncMock,
    mock_control_service: MagicMock,
) -> None:
    """Test that discover_entities creates a MerakiRebootButton."""
    mock_coordinator.data = {"devices": [MOCK_GX_DEVICE]}
    handler = GXHandler(
        mock_coordinator,
        MOCK_GX_DEVICE,
        MOCK_CONFIG_ENTRY,
        mock_camera_service,
        mock_control_service,
    )

    entities = await handler.discover_entities()

    assert len(entities) == 1
    assert isinstance(entities[0], MerakiRebootButton)
