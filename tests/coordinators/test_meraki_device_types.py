"""Tests for the Meraki device types."""
from custom_components.meraki_ha.coordinators.meraki_device_types import (
    map_meraki_model_to_device_type,
)


def test_map_meraki_model_to_device_type():
    """Test the map_meraki_model_to_device_type function."""
    assert map_meraki_model_to_device_type("MR42") == "Wireless"
    assert map_meraki_model_to_device_type("MS220-8P") == "Switch"
    assert map_meraki_model_to_device_type("MX64") == "Appliance"
    assert map_meraki_model_to_device_type("MV12") == "Camera"
    assert map_meraki_model_to_device_type("MT10") == "Sensor"
    assert map_meraki_model_to_device_type("GR10") == "Wireless"
    assert map_meraki_model_to_device_type("GS110-8P") == "Switch"
    assert map_meraki_model_to_device_type("Z3") == "Appliance"
    assert map_meraki_model_to_device_type("unknown") == "Unknown"
