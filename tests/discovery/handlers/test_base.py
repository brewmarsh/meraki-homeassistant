"""Tests for the BaseDeviceHandler."""

import pytest
from unittest.mock import MagicMock, patch
from custom_components.meraki_ha.discovery.handlers.base import BaseDeviceHandler
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    return MagicMock()


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked config entry."""
    return MagicMock()


from unittest.mock import AsyncMock


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    return AsyncMock()


def test_base_handler_init(mock_coordinator, mock_config_entry):
    """Test the initialization of the BaseDeviceHandler."""
    with patch.multiple(BaseDeviceHandler, __abstractmethods__=set()):
        handler = BaseDeviceHandler(mock_coordinator, MOCK_DEVICE, mock_config_entry)
        assert handler.device is MOCK_DEVICE


@pytest.mark.asyncio
async def test_base_handler_discover_entities_raises_not_implemented(
    mock_coordinator, mock_config_entry
):
    """Test that the base handler's discover_entities raises NotImplementedError."""
    with patch.multiple(BaseDeviceHandler, __abstractmethods__=set()):
        handler = BaseDeviceHandler(mock_coordinator, MOCK_DEVICE, mock_config_entry)
        # The abstract method should raise NotImplementedError
        BaseDeviceHandler.discover_entities.__isabstractmethod__ = False
        with pytest.raises(NotImplementedError):
            await handler.discover_entities()
