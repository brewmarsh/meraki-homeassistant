"""Tests for the Meraki entity helpers."""

from custom_components.meraki_ha.helpers.entity_helpers import format_name


def test_format_name():
    """Test the format_name function."""
    # Test with apply_format=True
    assert (
        format_name("Test Device", "wireless", "prefix", apply_format=True)
        == "[Wireless] Test Device"
    )
    assert (
        format_name("Test Device", "wireless", "suffix", apply_format=True)
        == "Test Device [Wireless]"
    )
    assert (
        format_name("Test Device", "wireless", "omit", apply_format=True)
        == "Test Device"
    )

    # Test with apply_format=False
    assert (
        format_name("Test Device", "wireless", "prefix", apply_format=False)
        == "Test Device"
    )
    assert (
        format_name("Test Device", "wireless", "suffix", apply_format=False)
        == "Test Device"
    )
    assert (
        format_name("Test Device", "wireless", "omit", apply_format=False)
        == "Test Device"
    )

    # Test with different device types
    assert (
        format_name("My Camera", "camera", "prefix", apply_format=True)
        == "[Camera] My Camera"
    )
    assert (
        format_name("My Switch", "switch", "suffix", apply_format=True)
        == "My Switch [Switch]"
    )
