from unittest.mock import MagicMock

from custom_components.meraki_ha.helpers.device_info_helpers import resolve_device_info


def test_camera_naming_enforcement():
    """Test that [Camera] prefix is enforced for MV devices."""
    config_entry = MagicMock()
    config_entry.entry_id = "test_entry"

    # Case 1: Product type is 'camera'
    device_data_1 = {
        "serial": "SERIAL1",
        "name": "Front Door",
        "productType": "camera",
        "model": "MV12",
    }
    device_info_1 = resolve_device_info(device_data_1, config_entry)
    assert device_info_1["name"] == "[Camera] Front Door"

    # Case 2: Model starts with MV, but productType is something else (hypothetical)
    device_data_2 = {
        "serial": "SERIAL2",
        "name": "Back Yard",
        "productType": "unknown",
        "model": "MV72",
    }
    device_info_2 = resolve_device_info(device_data_2, config_entry)
    assert device_info_2["name"] == "[Camera] Back Yard"

    # Case 3: Already has prefix
    device_data_3 = {
        "serial": "SERIAL3",
        "name": "[Camera] Side Gate",
        "productType": "camera",
        "model": "MV22",
    }
    device_info_3 = resolve_device_info(device_data_3, config_entry)
    assert device_info_3["name"] == "[Camera] Side Gate"

    # Case 4: Non-camera device stays same
    device_data_4 = {
        "serial": "SERIAL4",
        "name": "Main Switch",
        "productType": "switch",
        "model": "MS120",
    }
    device_info_4 = resolve_device_info(device_data_4, config_entry)
    assert device_info_4["name"] == "[Switch] Main Switch"
