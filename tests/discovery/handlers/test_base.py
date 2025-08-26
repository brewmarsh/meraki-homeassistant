"""Tests for the BaseDeviceHandler."""

import pytest
from unittest.mock import MagicMock
from custom_components.meraki_ha.discovery.handlers.base import BaseDeviceHandler
from tests.const import MOCK_DEVICE

@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    return MagicMock()

@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked config entry."""
    return MagicMock()

def test_base_handler_init(mock_coordinator, mock_config_entry):
    """Test the initialization of the BaseDeviceHandler."""
    handler = BaseDeviceHandler(mock_coordinator, MOCK_DEVICE, mock_config_entry)
    assert handler.device is MOCK_DEVICE

def test_base_handler_discover_entities_raises_not_implemented(
    mock_coordinator, mock_config_entry
):
    """Test that the base handler's discover_entities raises NotImplementedError."""
    handler = BaseDeviceHandler(mock_coordinator, MOCK_DEVICE, mock_config_entry)
    with pytest.raises(NotImplementedError):
        handler.discover_entities()
