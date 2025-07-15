"""Tests for the Meraki SSID status calculator."""
from custom_components.meraki_ha.helpers.ssid_status_calculator import (
    SsidStatusCalculator as calc,
)


def test_calculate_ssid_status():
    """Test the calculate_ssid_status function."""
    ssids = [
        {"enabled": True, "name": "SSID 1", "tags": ["tag1"], "networkId": "N_123"},
        {"enabled": False, "name": "SSID 2", "tags": ["tag2"], "networkId": "N_123"},
    ]
    devices = [
        {"model": "MR33", "status": "online", "tags": ["tag1"], "networkId": "N_123"},
        {"model": "MR33", "status": "offline", "tags": ["tag2"], "networkId": "N_123"},
    ]
    result = calc.calculate_ssid_status(ssids, devices)
    assert result[0]["status"] == "online"
    assert result[1]["status"] == "disabled"
