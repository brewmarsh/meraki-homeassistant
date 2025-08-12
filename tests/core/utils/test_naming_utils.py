"""Tests for the naming utils."""

from custom_components.meraki_ha.core.utils.naming_utils import (
    format_device_name,
)


def test_format_device_name_prefix():
    """Test the format_device_name function with a prefix."""
    device = {"name": "My AP", "model": "MR33", "productType": "wireless"}
    options = {"device_name_format": "prefix"}
    assert format_device_name(device, options) == "[Wireless] My AP"


def test_format_device_name_suffix():
    """Test the format_device_name function with a suffix."""
    device = {"name": "My AP", "model": "MR33", "productType": "wireless"}
    options = {"device_name_format": "suffix"}
    assert format_device_name(device, options) == "My AP [Wireless]"


def test_format_device_name_omit():
    """Test the format_device_name function with omit."""
    device = {"name": "My AP", "model": "MR33"}
    options = {"device_name_format": "omit"}
    assert format_device_name(device, options) == "My AP"


def test_format_device_name_no_name():
    """Test the format_device_name function with no name."""
    device = {"productType": "wireless", "model": "MR33", "serial": "Q234-ABCD-5678"}
    options = {"device_name_format": "prefix"}
    assert (
        format_device_name(device, options) == "[Wireless] Meraki MR33 Q234-ABCD-5678"
    )


def test_format_device_name_no_product_type():
    """Test the format_device_name function with no product type."""
    device = {"name": "My AP", "model": "MR33"}
    options = {"device_name_format": "prefix"}
    assert format_device_name(device, options) == "[Device] My AP"
