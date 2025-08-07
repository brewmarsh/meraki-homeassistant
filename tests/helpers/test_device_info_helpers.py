"""Tests for the device info helpers."""

from unittest.mock import MagicMock

from custom_components.meraki_ha.helpers.device_info_helpers import (
    resolve_device_info,
)


def test_resolve_device_info_physical_device():
    """Test the resolve_device_info function for a physical device."""
    entity_data = {
        "serial": "Q234-ABCD-5678",
        "name": "My AP",
        "model": "MR33",
        "firmware": "26.1",
    }
    config_entry = MagicMock()
    config_entry.options = {}
    device_info = resolve_device_info(entity_data, config_entry)
    assert device_info["identifiers"] == {("meraki_ha", "Q234-ABCD-5678")}
    assert device_info["name"] == "[Device] My AP"
    assert device_info["model"] == "MR33"
    assert device_info["sw_version"] == "26.1"
    assert device_info["manufacturer"] == "Cisco Meraki"


def test_resolve_device_info_ssid_device():
    """Test the resolve_device_info function for an SSID."""
    entity_data = {"networkId": "N_123"}
    ssid_data = {"number": 0, "name": "My SSID"}
    config_entry = MagicMock()
    config_entry.options = {}
    device_info = resolve_device_info(entity_data, config_entry, ssid_data)
    assert device_info["identifiers"] == {("meraki_ha", "N_123_0")}
    assert device_info["name"] == "My SSID"
    assert device_info["model"] == "Wireless SSID"
    assert device_info["manufacturer"] == "Cisco Meraki"
