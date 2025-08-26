"""Tests for the MRHandler."""

import pytest
from unittest.mock import MagicMock
from custom_components.meraki_ha.discovery.handlers.mr import MRHandler
from tests.const import MOCK_DEVICE

@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    return MagicMock()

@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked config entry."""
    return MagicMock()

def test_mr_handler_discover_entities(mock_coordinator, mock_config_entry):
    """Test that the MRHandler's discover_entities returns an empty list (for now)."""
    handler = MRHandler(mock_coordinator, MOCK_DEVICE, mock_config_entry)
    entities = handler.discover_entities()
    assert entities == []
