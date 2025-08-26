"""
Tests for the GXHandler.
"""
from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.button import MerakiRebootButton
from custom_components.meraki_ha.discovery.handlers.gx import GXHandler
from ...const import MOCK_CONFIG_ENTRY, MOCK_GX_DEVICE


@pytest.fixture
def mock_coordinator():
    """Fixture for a mock MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [MOCK_GX_DEVICE]}
    return coordinator


@pytest.fixture
def mock_control_service():
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


def test_discover_entities_creates_reboot_button(
    mock_coordinator, mock_control_service
):
    """Test that discover_entities creates a MerakiRebootButton."""
    handler = GXHandler(
        mock_coordinator, MOCK_GX_DEVICE, MOCK_CONFIG_ENTRY, mock_control_service
    )

    entities = handler.discover_entities()

    assert len(entities) == 1
    assert isinstance(entities[0], MerakiRebootButton)
