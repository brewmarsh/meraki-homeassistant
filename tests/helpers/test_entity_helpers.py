"""Tests for the Meraki entity helpers."""

from custom_components.meraki_ha.core.utils.naming_utils import format_entity_name


def test_format_entity_name():
    """Test the format_entity_name function."""
    assert format_entity_name("Device Name", "Sensor") == "Device Name Sensor"
    assert format_entity_name("Device Name", "") == "Device Name"
    assert format_entity_name("Device Name", " ") == "Device Name"
    assert format_entity_name("[Wireless] AP", "Status") == "[Wireless] AP Status"
