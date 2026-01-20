"""Tests for the Meraki entity helpers."""

from custom_components.meraki_ha.core.utils.naming_utils import format_entity_name


def test_format_entity_name():
    """Test the format_entity_name function."""
    device = {"name": "Device Name"}
    config = {"device_name_format": "omit"}
    assert format_entity_name(device, config, "Sensor") == "Device Name Sensor"
    assert format_entity_name(device, config, "") == "Device Name"
    assert format_entity_name(device, config, " ") == "Device Name"

    device_with_prefix = {"name": "AP", "productType": "wireless"}
    config_with_prefix = {"device_name_format": "prefix"}
    assert (
        format_entity_name(device_with_prefix, config_with_prefix, "Status")
        == "[Wireless] AP Status"
    )
