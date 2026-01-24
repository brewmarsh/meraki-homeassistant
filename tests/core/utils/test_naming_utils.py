"""Tests for the naming utils."""

from custom_components.meraki_ha.core.utils.naming_utils import (
    format_device_name,
)


def test_format_device_name():
    """Test the format_device_name function."""
    device = {"name": "My AP", "model": "MR33", "productType": "wireless"}
    config = {}
    assert format_device_name(device, config) == "My AP"


def test_format_device_name_no_name():
    """Test the format_device_name function with no name."""
    device = {"productType": "wireless", "model": "MR33", "serial": "Q234-ABCD-5678"}
    config = {}
    assert format_device_name(device, config) == "Meraki MR33 Q234-ABCD-5678"
