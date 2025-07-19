"""Tests for the Meraki naming utils."""

from custom_components.meraki_ha.helpers.naming_utils import format_device_name


def test_format_device_name():
    """Test the format_device_name function."""
    assert (
        format_device_name("Test Device", "MR42", "prefix", False)
        == "[Wireless] Test Device"
    )
    assert (
        format_device_name("Test Device", "MR42", "suffix", False)
        == "Test Device [Wireless]"
    )
    assert format_device_name("Test Device", "MR42", "omitted", False) == "Test Device"
    assert (
        format_device_name("Test Org", "Organization", "prefix", True)
        == "[Org] Test Org"
    )
