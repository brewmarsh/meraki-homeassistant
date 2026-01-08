"""Tests for the naming utils."""

from custom_components.meraki_ha.core.utils.naming_utils import (
    format_device_name,
)


def test_format_device_name_prefix():
    """Test the format_device_name function with prefix format."""
    device = {"name": "My AP", "model": "MR33", "productType": "wireless"}
    config = {"device_name_format": "prefix"}
    assert format_device_name(device, config) == "[Wireless] My AP"


def test_format_device_name_omit():
    """Test the format_device_name function with omit format."""
    device = {"name": "My AP", "model": "MR33", "productType": "wireless"}
    config = {"device_name_format": "omit"}
    assert format_device_name(device, config) == "My AP"


def test_format_device_name_no_name():
    """Test the format_device_name function with no name."""
    device = {"productType": "wireless", "model": "MR33", "serial": "Q234-ABCD-5678"}
    config = {"device_name_format": "prefix"}
    assert format_device_name(device, config) == "[Wireless] Meraki MR33 Q234-ABCD-5678"


def test_format_device_name_no_product_type():
    """Test the format_device_name function with no product type."""
    device = {"name": "My AP", "model": "MR33"}
    config = {"device_name_format": "prefix"}
    assert format_device_name(device, config) == "[Device] My AP"


def test_format_device_name_camera():
    """Test the format_device_name function for camera (should have prefix)."""
    device = {"name": "Big Boss", "model": "MV13", "productType": "camera"}
    config = {"device_name_format": "prefix"}
    assert format_device_name(device, config) == "[Camera] Big Boss"
