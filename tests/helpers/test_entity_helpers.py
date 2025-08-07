"""Tests for the Meraki entity helpers."""

from custom_components.meraki_ha.helpers.entity_helpers import format_entity_name


def test_format_entity_name():
    """Test the format_entity_name function."""
    assert (
        format_entity_name("Test Device", "wireless", "prefix", "")
        == "[Wireless] Test Device"
    )
    assert (
        format_entity_name("Test Device", "wireless", "suffix", "")
        == "Test Device [Wireless]"
    )
    assert format_entity_name("Test Device", "wireless", "omit", "") == "Test Device"
    assert (
        format_entity_name("Test Device", "wireless", "prefix", "Sensor")
        == "[Wireless] Test Device Sensor"
    )
