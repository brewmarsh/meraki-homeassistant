
import pytest
from custom_components.meraki_ha.core.utils.naming_utils import standardize_device_name, format_device_name

def test_standardize_device_name():
    assert standardize_device_name("Kitchen MT14") == "Meraki Kitchen MT14"
    assert standardize_device_name("Meraki Kitchen MT14") == "Meraki Kitchen MT14"
    assert standardize_device_name("meraki Kitchen MT14") == "meraki Kitchen MT14"
    assert standardize_device_name("") == "Meraki Device"
    assert standardize_device_name(None) == "Meraki Device"

def test_format_device_name():
    config = {"options": {}}
    device = {"name": "Kitchen MT14", "model": "MT14", "serial": "Q2XX-XXXX-XXXX"}
    # format_device_name now calls _standardize_device_name internally
    assert format_device_name(device, config) == "Meraki Kitchen MT14"

    device_no_name = {"name": None, "model": "MT14", "serial": "Q2XX-XXXX-XXXX"}
    assert format_device_name(device_no_name, config) == "Meraki MT14 Q2XX-XXXX-XXXX"

    device_meraki_name = {"name": "Meraki Kitchen", "model": "MT14", "serial": "Q2XX-XXXX-XXXX"}
    assert format_device_name(device_meraki_name, config) == "Meraki Kitchen"
