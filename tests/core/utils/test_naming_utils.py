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
    config = {"device_name_format": "prefix"}
    assert format_device_name(device, config) == "Meraki MR33 Q234-ABCD-5678"


def test_format_device_name_no_product_type():
    """Test the format_device_name function with no product type."""
    device = {"name": "My AP", "model": "MR33"}
    config = {"device_name_format": "prefix"}
    assert format_device_name(device, config) == "My AP"


def test_format_device_name_camera_inferred():
    """Test the format_device_name function for camera inferred from model."""
    device = {"name": "My Cam", "model": "MV12"}
    config = {"device_name_format": "prefix"}
    assert format_device_name(device, config) == "My Cam"


def test_format_device_name_camera():
    """Test the format_device_name function for camera (should have prefix)."""
    device = {"name": "Big Boss", "model": "MV13", "productType": "camera"}
    config = {"device_name_format": "prefix"}
    assert format_device_name(device, config) == "Big Boss"
