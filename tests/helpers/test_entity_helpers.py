"""Tests for the Meraki entity helpers."""

from custom_components.meraki_ha.const import (
    DEVICE_NAME_FORMAT_NONE,
    DEVICE_NAME_FORMAT_PREFIX,
    DEVICE_NAME_FORMAT_SUFFIX,
)
from custom_components.meraki_ha.helpers.entity_helpers import format_entity_name


def test_format_entity_name_none_format():
    """Test the format_entity_name function with no format."""
    # With DEVICE_NAME_FORMAT_NONE, just returns the device name
    result = format_entity_name(
        "Device Name", "wireless", name_format=DEVICE_NAME_FORMAT_NONE
    )
    assert result == "Device Name"


def test_format_entity_name_prefix_format():
    """Test the format_entity_name function with prefix format."""
    # With DEVICE_NAME_FORMAT_PREFIX, prepends the device type
    result = format_entity_name(
        "Device Name", "wireless", name_format=DEVICE_NAME_FORMAT_PREFIX
    )
    assert result == "[Wireless] Device Name"


def test_format_entity_name_suffix_format():
    """Test the format_entity_name function with suffix format."""
    # With DEVICE_NAME_FORMAT_SUFFIX, appends the device type
    result = format_entity_name(
        "Device Name", "wireless", name_format=DEVICE_NAME_FORMAT_SUFFIX
    )
    assert result == "Device Name [Wireless]"


def test_format_entity_name_sensor_type_ignores_format():
    """Test that sensor device type ignores formatting."""
    # When device_type is "sensor", no formatting is applied
    result = format_entity_name(
        "Device Name", "sensor", name_format=DEVICE_NAME_FORMAT_PREFIX
    )
    assert result == "Device Name"
