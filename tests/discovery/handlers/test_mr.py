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
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
@pytest.fixture
def mock_network_control_service() -> MagicMock:
    """Fixture for a mock NetworkControlService."""
    return MagicMock()


<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
@pytest.mark.asyncio
async def test_mr_handler_discover_entities(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_control_service: MagicMock,
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
    mock_network_control_service: MagicMock,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    mock_network_control_service: MagicMock,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
) -> None:
    """Test that the MRHandler's discover_entities returns an empty list (for now)."""
    handler = MRHandler(
        mock_coordinator,
        MOCK_DEVICE,
        mock_config_entry,
        mock_control_service,
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
        mock_network_control_service,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
        mock_network_control_service,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    )
    entities = await handler.discover_entities()
    assert entities == []
