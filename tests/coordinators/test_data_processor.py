"""Tests for the Meraki data processor."""
from unittest.mock import MagicMock

from custom_components.meraki_ha.coordinators.data_processor import (
    MerakiDataProcessor,
)


async def test_meraki_data_processor() -> None:
    """Test the Meraki data processor."""
    coordinator = MagicMock()
    processor = MerakiDataProcessor(coordinator)
    devices = [
            {"serial": "Q234-ABCD-5678", "tags": ["tag1", "tag2"]},
            {"serial": "Q234-ABCD-5679", "tags": ["tag3", "tag4"]},
    ]
    processed_devices = await processor.process_devices(devices)
    assert processed_devices[0]["tags"] == ["tag1", "tag2"]
    assert processed_devices[1]["tags"] == ["tag3", "tag4"]
