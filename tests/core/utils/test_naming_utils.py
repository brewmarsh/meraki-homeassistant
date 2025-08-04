"""Tests for the Meraki naming utils."""

from custom_components.meraki_ha.core.utils.naming_utils import format_device_name
from custom_components.meraki_ha.const import (
    CONF_DEVICE_NAME_FORMAT,
    DEVICE_NAME_FORMAT_PREFIX,
    DEVICE_NAME_FORMAT_SUFFIX,
    DEVICE_NAME_FORMAT_OMIT,
)

def test_format_device_name_prefix():
    """Test the format_device_name function with prefix."""
    config = {CONF_DEVICE_NAME_FORMAT: DEVICE_NAME_FORMAT_PREFIX}

    # Test with a wireless device
    device = {"name": "Test AP", "productType": "wireless"}
    assert format_device_name(device, config) == "[Wireless] Test AP"

    # Test with an SSID
    device = {"name": "Test SSID", "productType": "ssid"}
    assert format_device_name(device, config) == "Test SSID"

    # Test with a network
    device = {"name": "Test Network", "productType": "network"}
    assert format_device_name(device, config) == "Test Network"

    # Test with an unknown device type
    device = {"name": "Test Device", "productType": "unknown"}
    assert format_device_name(device, config) == "[Device] Test Device"

    # Test with no product type
    device = {"name": "Test Device"}
    assert format_device_name(device, config) == "[Device] Test Device"


def test_format_device_name_suffix():
    """Test the format_device_name function with suffix."""
    config = {CONF_DEVICE_NAME_FORMAT: DEVICE_NAME_FORMAT_SUFFIX}

    # Test with a switch device
    device = {"name": "Test Switch", "productType": "switch"}
    assert format_device_name(device, config) == "Test Switch [Switch]"

    # Test with an SSID
    device = {"name": "Test SSID", "productType": "ssid"}
    assert format_device_name(device, config) == "Test SSID"

    # Test with a network
    device = {"name": "Test Network", "productType": "network"}
    assert format_device_name(device, config) == "Test Network"

    # Test with an unknown device type
    device = {"name": "Test Device", "productType": "unknown"}
    assert format_device_name(device, config) == "Test Device [Device]"

    # Test with no product type
    device = {"name": "Test Device"}
    assert format_device_name(device, config) == "Test Device [Device]"


def test_format_device_name_omit():
    """Test the format_device_name function with omit."""
    config = {CONF_DEVICE_NAME_FORMAT: DEVICE_NAME_FORMAT_OMIT}

    # Test with a camera device
    device = {"name": "Test Camera", "productType": "camera"}
    assert format_device_name(device, config) == "Test Camera"

    # Test with an SSID
    device = {"name": "Test SSID", "productType": "ssid"}
    assert format_device_name(device, config) == "Test SSID"


def test_format_device_name_no_name():
    """Test the format_device_name function when device has no name."""
    config = {CONF_DEVICE_NAME_FORMAT: DEVICE_NAME_FORMAT_PREFIX}

    # Test with a device with no name
    device = {"model": "MR42", "serial": "Q2JC-ABCD-WXYZ", "productType": "wireless"}
    assert format_device_name(device, config) == "[Wireless] Meraki MR42 Q2JC-ABCD-WXYZ"

    # Test with an SSID with no name
    device = {"number": 5, "productType": "ssid"}
    assert format_device_name(device, config) == "SSID 5"
