"""Tests for the MRHandler."""

from custom_components.meraki_ha.discovery.handlers.mr import MRHandler
from tests.const import MOCK_DEVICE

def test_mr_handler_discover_entities():
    """Test that the MRHandler's discover_entities returns an empty list (for now)."""
    handler = MRHandler(MOCK_DEVICE)
    entities = handler.discover_entities()
    assert entities == []
