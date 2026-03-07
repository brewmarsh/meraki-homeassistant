from unittest.mock import MagicMock

from homeassistant.helpers.device_registry import DeviceEntryType

from custom_components.meraki_ha.const.integration import DOMAIN, from custom_components.meraki_ha.helpers.device_info_helpers import resolve_device_info


def test_resolve_device_info_network_virtual_controller():
    """Test resolving device info for network as Virtual Controller."""
    config_entry = MagicMock()
    config_entry.entry_id = "test_entry"

    # Case 1: Name without prefix
    entity_data_1 = {"id": "net1", "name": "Site A", "productTypes": ["appliance"]}
    device_info_1 = resolve_device_info(entity_data_1, config_entry)
    # New Format: Site: {Name}
    assert device_info_1["name"] == "Site: Site A"
    assert device_info_1["identifiers"] == {(DOMAIN, "network_net1")}
    assert device_info_1["model"] == "Network Controller Service"
    assert device_info_1["entry_type"] == DeviceEntryType.SERVICE

    # Case 2: Name with prefix (should not double prefix)
    entity_data_2 = {
        "id": "net2",
        "name": "Site: Site B",
        "productTypes": ["appliance"],
    }
    device_info_2 = resolve_device_info(entity_data_2, config_entry)
    assert device_info_2["name"] == "Site: Site B"
    assert device_info_2["identifiers"] == {(DOMAIN, "network_net2")}


def test_resolve_device_info_ssid_virtual_controller_attachment():
    """Test resolving device info for SSID attaches to Virtual Controller."""
    config_entry = MagicMock()
    config_entry.entry_id = "test_entry"

    # Case 1: SSID data
    ssid_data_1 = {"networkId": "net1", "number": 0, "name": "Guest WiFi"}
    # Passing ssid_data as entity_data (simulating how it's called for SSIDs)
    device_info_1 = resolve_device_info(ssid_data_1, config_entry)

    # Should only return identifiers pointing to the network device
    assert device_info_1["identifiers"] == {(DOMAIN, "network_net1")}
    assert "name" not in device_info_1
    assert "model" not in device_info_1


def test_resolve_device_info_device_prefix():
    """Test resolving device info with device prefix (Physical Devices)."""
    config_entry = MagicMock()
    config_entry.entry_id = "test_entry"

    # Case 1: Name without prefix (Switch)
    device_data_1 = {
        "serial": "Q234-5678-90AB",
        "name": "Core Switch",
        "productType": "switch",
        "model": "MS220-8P",
    }
    device_info_1 = resolve_device_info(device_data_1, config_entry)
    # Physical devices still use [Type] prefix logic as before
    # (Physical Devices remain as is per design doc)
    assert device_info_1["name"] == "[Switch] Core Switch"

    # Case 2: Name with prefix (Camera)
    device_data_2 = {
        "serial": "Q234-5678-90AC",
        "name": "[Camera] Front Door",
        "productType": "camera",
        "model": "MV12",
    }
    device_info_2 = resolve_device_info(device_data_2, config_entry)
    assert device_info_2["name"] == "[Camera] Front Door"

    # Case 3: CS-WE Camera
    device_data_3 = {
        "serial": "Q234-5678-90AD",
        "name": "Backyard",
        "productType": "camera",
        "model": "CS-WE",
    }
    device_info_3 = resolve_device_info(device_data_3, config_entry)
    assert device_info_3["name"] == "[Camera] Backyard"

    # Case 4: No name (fallback to serial)
    device_data_4 = {
        "serial": "Q234-5678-90AE",
        "name": None,
        "productType": "switch",
        "model": "MS220-8P",
    }
    device_info_4 = resolve_device_info(device_data_4, config_entry)
    assert device_info_4["name"] == "[Switch] Q234-5678-90AE"
