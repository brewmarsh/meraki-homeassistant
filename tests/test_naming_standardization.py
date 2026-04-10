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
    # MT devices (sensors) now get a [Sensor] prefix
    device = {
        "name": "Kitchen MT14",
        "model": "MT14",
        "serial": "Q2XX-XXXX-XXXX",
        "productType": "sensor",
    }
    assert format_device_name(device, config) == "[Sensor] Kitchen MT14"

    # MS devices (switches) get a [Switch] prefix
    switch_device = {
        "name": "Office Switch",
        "model": "MS120-8LP",
        "serial": "Q2XX-YYYY-YYYY",
        "productType": "switch",
    }
    assert format_device_name(switch_device, config) == "[Switch] Office Switch"

    # MR devices (wireless) get a [Wireless] prefix
    wireless_device = {
        "name": "Living Room AP",
        "model": "MR33",
        "serial": "Q2XX-ZZZZ-ZZZZ",
        "productType": "wireless",
    }
    assert format_device_name(wireless_device, config) == "[Wireless] Living Room AP"

    # MX devices (appliance) get a [Appliance] prefix
    appliance_device = {
        "name": "Home Gateway",
        "model": "MX64",
        "serial": "Q2XX-WWWW-WWWW",
        "productType": "appliance",
    }
    assert format_device_name(appliance_device, config) == "[Appliance] Home Gateway"

    device_no_name = {
        "name": None,
        "model": "MT14",
        "serial": "Q2XX-XXXX-XXXX",
        "productType": "sensor",
    }
    assert format_device_name(device_no_name, config) == "[Sensor] MT14 Q2XX-XXXX-XXXX"

    device_meraki_name = {
        "name": "Meraki Kitchen",
        "model": "MT14",
        "serial": "Q2XX-XXXX-XXXX",
    }
    assert format_device_name(device_meraki_name, config) == "[Sensor] Meraki Kitchen"
