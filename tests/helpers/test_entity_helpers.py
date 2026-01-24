"""Tests for the Meraki entity helpers."""

from custom_components.meraki_ha.core.utils.naming_utils import format_entity_name


def test_format_entity_name():
    """Test the format_entity_name function."""
    device = {"name": "Device Name"}
    config = {}
    assert format_entity_name(device, config, "Sensor") == "Device Name Sensor"
    assert format_entity_name(device, config, "") == "Device Name"
    assert format_entity_name(device, config, " ") == "Device Name"
