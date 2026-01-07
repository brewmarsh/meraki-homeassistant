"""Tests for the naming utils."""

from custom_components.meraki_ha.core.utils.naming_utils import (
    format_device_name,
)


def test_format_device_name_prefix():
    """Test the format_device_name function with prefix format."""
    device = {"name": "My AP", "model": "MR33", "productType": "wireless"}
    config = {"device_name_format": "prefix"}
    # Wireless devices use [MR] prefix (Meraki model prefix)
    assert format_device_name(device, config) == "[MR] My AP"


def test_format_device_name_omit():
    """Test the format_device_name function with omit format."""
    device = {"name": "My AP", "model": "MR33", "productType": "wireless"}
    config = {"device_name_format": "omit"}
    assert format_device_name(device, config) == "My AP"


def test_format_device_name_no_name():
    """Test the format_device_name function with no name."""
    device = {"productType": "wireless", "model": "MR33", "serial": "Q234-ABCD-5678"}
    config = {"device_name_format": "prefix"}
    # Wireless devices use [MR] prefix (Meraki model prefix)
    assert format_device_name(device, config) == "[MR] Meraki MR33 Q234-ABCD-5678"


def test_format_device_name_no_product_type():
    """Test the format_device_name function with no product type but known model."""
    device = {"name": "My AP", "model": "MR33"}
    config = {"device_name_format": "prefix"}
    # Model prefix MR is recognized, so uses [MR] even without productType
    assert format_device_name(device, config) == "[MR] My AP"


def test_format_device_name_camera():
    """Test the format_device_name function for camera (should have prefix)."""
    device = {"name": "Big Boss", "model": "MV13", "productType": "camera"}
    config = {"device_name_format": "prefix"}
    # Camera devices use [MV] prefix (Meraki model prefix)
    assert format_device_name(device, config) == "[MV] Big Boss"


def test_format_device_name_switch():
    """Test the format_device_name function for switch."""
    device = {"name": "Core Switch", "model": "MS225", "productType": "switch"}
    config = {"device_name_format": "prefix"}
    # Switch devices use [MS] prefix (Meraki model prefix)
    assert format_device_name(device, config) == "[MS] Core Switch"


def test_format_device_name_sensor():
    """Test the format_device_name function for sensor."""
    device = {"name": "Office Sensor", "model": "MT15", "productType": "sensor"}
    config = {"device_name_format": "prefix"}
    # Sensor devices use [MT] prefix (Meraki model prefix)
    assert format_device_name(device, config) == "[MT] Office Sensor"


def test_format_device_name_appliance():
    """Test the format_device_name function for appliance."""
    device = {"name": "Edge Router", "model": "MX67", "productType": "appliance"}
    config = {"device_name_format": "prefix"}
    # Appliance devices use [MX] prefix (Meraki model prefix)
    assert format_device_name(device, config) == "[MX] Edge Router"
