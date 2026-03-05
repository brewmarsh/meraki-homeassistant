
from custom_components.meraki_ha.core.utils.naming_utils import (
    format_device_name,
    standardize_device_name,
)


def test_standardize_device_name():
    assert standardize_device_name("Kitchen MT14") == "Meraki Kitchen MT14"
    assert standardize_device_name("Meraki Kitchen MT14") == "Meraki Kitchen MT14"
    assert standardize_device_name("meraki Kitchen MT14") == "meraki Kitchen MT14"
    assert standardize_device_name("") == "Meraki Device"
    assert standardize_device_name(None) == "Meraki Device"

def test_format_device_name():
    config = {"options": {}}
    # MT devices (sensors) now get a [Sensor] prefix, which is exempted from the Meraki prefix
    device = {"name": "Kitchen MT14", "model": "MT14", "serial": "Q2XX-XXXX-XXXX", "productType": "sensor"}
    assert format_device_name(device, config) == "[Sensor] Kitchen MT14"

    device_no_name = {"name": None, "model": "MT14", "serial": "Q2XX-XXXX-XXXX", "productType": "sensor"}
    assert format_device_name(device_no_name, config) == "[Sensor] MT14 Q2XX-XXXX-XXXX"

    device_meraki_name = {"name": "Meraki Kitchen", "model": "MT14", "serial": "Q2XX-XXXX-XXXX", "productType": "sensor"}
    assert format_device_name(device_meraki_name, config) == "[Sensor] Meraki Kitchen"

    # Non-sensor devices still get the Meraki prefix
    device_ap = {"name": "Office AP", "model": "MR33", "serial": "Q2XX-XXXX-XXXX", "productType": "wireless"}
    assert format_device_name(device_ap, config) == "Meraki Office AP"
