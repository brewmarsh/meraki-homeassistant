"""Tests for the MRHandler."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.discovery.handlers.mr import MRHandler
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_control_service() -> MagicMock:
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


@pytest.fixture
def mock_camera_service() -> AsyncMock:
    """Fixture for a mocked CameraService."""
    return AsyncMock()


<<<<<<< HEAD
=======
@pytest.fixture
def mock_network_control_service() -> MagicMock:
    """Fixture for a mock NetworkControlService."""
    return MagicMock()


>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
@pytest.mark.asyncio
async def test_mr_handler_discover_entities(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_control_service: MagicMock,
<<<<<<< HEAD
=======
    mock_network_control_service: MagicMock,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
) -> None:
    """Test that the MRHandler's discover_entities returns an empty list (for now)."""
    handler = MRHandler(
        mock_coordinator,
        MOCK_DEVICE,
        mock_config_entry,
        mock_control_service,
<<<<<<< HEAD
=======
        mock_network_control_service,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    )
    entities = await handler.discover_entities()
    assert entities == []
