
from unittest.mock import MagicMock

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.helpers.device_info_helpers import resolve_device_info


def test_resolve_device_info_network_prefix():
    """Test resolving device info with network prefix."""
    config_entry = MagicMock()
    config_entry.entry_id = "test_entry"

    # Case 1: Name without prefix
    entity_data_1 = {
        "id": "net1",
        "name": "Site A",
        "productTypes": ["appliance"]
    }
    device_info_1 = resolve_device_info(entity_data_1, config_entry)
    assert device_info_1["name"] == "[Network] Site A"
    assert device_info_1["identifiers"] == {(DOMAIN, "network_net1")}

    # Case 2: Name with prefix
    entity_data_2 = {
        "id": "net2",
        "name": "[Network] Site B",
        "productTypes": ["appliance"]
    }
    device_info_2 = resolve_device_info(entity_data_2, config_entry)
    assert device_info_2["name"] == "[Network] Site B"
    assert device_info_2["identifiers"] == {(DOMAIN, "network_net2")}

def test_resolve_device_info_ssid_prefix():
    """Test resolving device info with SSID prefix."""
    config_entry = MagicMock()
    config_entry.entry_id = "test_entry"

    # Case 1: Name without prefix
    ssid_data_1 = {
        "networkId": "net1",
        "number": 0,
        "name": "Guest WiFi"
    }
    # Passing ssid_data as entity_data (simulating how it's called for SSIDs)
    device_info_1 = resolve_device_info(ssid_data_1, config_entry)
    assert device_info_1["name"] == "[SSID 0] Guest WiFi"

    # Case 2: Name with prefix
    ssid_data_2 = {
        "networkId": "net1",
        "number": 1,
        "name": "[SSID 1] Corporate WiFi"
    }
    device_info_2 = resolve_device_info(ssid_data_2, config_entry)
    assert device_info_2["name"] == "[SSID 1] Corporate WiFi"

def test_resolve_device_info_device_prefix():
    """Test resolving device info with device prefix."""
    config_entry = MagicMock()
    config_entry.entry_id = "test_entry"

    # Case 1: Name without prefix (Switch)
    device_data_1 = {
        "serial": "Q234-5678-90AB",
        "name": "Core Switch",
        "productType": "switch",
        "model": "MS220-8P"
    }
    device_info_1 = resolve_device_info(device_data_1, config_entry)
    assert device_info_1["name"] == "[Switch] Core Switch"

    # Case 2: Name with prefix (Camera)
    device_data_2 = {
        "serial": "Q234-5678-90AC",
        "name": "[Camera] Front Door",
        "productType": "camera",
        "model": "MV12"
    }
    device_info_2 = resolve_device_info(device_data_2, config_entry)
    assert device_info_2["name"] == "[Camera] Front Door"
