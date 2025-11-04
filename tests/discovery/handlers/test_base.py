"""Tests for the BaseDeviceHandler."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.discovery.handlers.base import BaseDeviceHandler
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_camera_service() -> AsyncMock:
    """Fixture for a mocked CameraService."""
    return AsyncMock()


def test_base_handler_init(
    mock_coordinator: MagicMock, mock_config_entry: MagicMock
) -> None:
    """Test the initialization of the BaseDeviceHandler."""
    with patch.multiple(BaseDeviceHandler, __abstractmethods__=set()):
        handler = BaseDeviceHandler(  # type: ignore[abstract]
            mock_coordinator, MOCK_DEVICE, mock_config_entry
        )
        assert handler.device is MOCK_DEVICE


@pytest.mark.asyncio
async def test_base_handler_discover_entities_raises_not_implemented(
    mock_coordinator: MagicMock, mock_config_entry: MagicMock
) -> None:
    """Test that the base handler's discover_entities raises NotImplementedError."""
    with patch.multiple(BaseDeviceHandler, __abstractmethods__=set()):
        handler = BaseDeviceHandler(  # type: ignore[abstract]
            mock_coordinator, MOCK_DEVICE, mock_config_entry
        )
        # The abstract method should raise NotImplementedError
        BaseDeviceHandler.discover_entities.__isabstractmethod__ = False  # type: ignore[attr-defined]
        with pytest.raises(NotImplementedError):
            await handler.discover_entities()
