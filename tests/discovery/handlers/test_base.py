"""Tests for the BaseDeviceHandler."""

import pytest
from custom_components.meraki_ha.discovery.handlers.base import BaseDeviceHandler
from tests.const import MOCK_DEVICE

def test_base_handler_init():
    """Test the initialization of the BaseDeviceHandler."""
    handler = BaseDeviceHandler(MOCK_DEVICE)
    assert handler.device is MOCK_DEVICE

def test_base_handler_discover_entities_raises_not_implemented():
    """Test that the base handler's discover_entities raises NotImplementedError."""
    handler = BaseDeviceHandler(MOCK_DEVICE)
    with pytest.raises(NotImplementedError):
        handler.discover_entities()
