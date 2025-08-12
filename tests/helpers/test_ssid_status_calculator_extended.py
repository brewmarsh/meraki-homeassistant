"""Tests for the SSID status calculator."""

from custom_components.meraki_ha.helpers.ssid_status_calculator import (
    SsidStatusCalculator,
)


def test_ssid_status_calculator_all_enabled():
    """Test the SSID status calculator with all SSIDs enabled."""
    ssids = [
        {"name": "SSID 1", "enabled": True, "broadcasting": True, "networkId": "N_123"},
        {"name": "SSID 2", "enabled": True, "broadcasting": True, "networkId": "N_123"},
    ]
    devices = [
        {"serial": "Q234-ABCD-5678", "status": "online", "model": "MR33", "tags": []}
    ]
    result = SsidStatusCalculator.calculate_ssid_status(ssids, devices)
    assert result[0]["status"] == "online"
    assert result[1]["status"] == "online"


def test_ssid_status_calculator_all_disabled():
    """Test the SSID status calculator with all SSIDs disabled."""
    ssids = [
        {
            "name": "SSID 1",
            "enabled": False,
            "broadcasting": False,
            "networkId": "N_123",
        },
        {
            "name": "SSID 2",
            "enabled": False,
            "broadcasting": False,
            "networkId": "N_123",
        },
    ]
    devices = [
        {"serial": "Q234-ABCD-5678", "status": "online", "model": "MR33", "tags": []}
    ]
    result = SsidStatusCalculator.calculate_ssid_status(ssids, devices)
    assert result[0]["status"] == "disabled"
    assert result[1]["status"] == "disabled"


def test_ssid_status_calculator_mixed():
    """Test the SSID status calculator with a mix of enabled and disabled SSIDs."""
    ssids = [
        {"name": "SSID 1", "enabled": True, "broadcasting": True, "networkId": "N_123"},
        {
            "name": "SSID 2",
            "enabled": False,
            "broadcasting": False,
            "networkId": "N_123",
        },
    ]
    devices = [
        {"serial": "Q234-ABCD-5678", "status": "online", "model": "MR33", "tags": []}
    ]
    result = SsidStatusCalculator.calculate_ssid_status(ssids, devices)
    assert result[0]["status"] == "online"
    assert result[1]["status"] == "disabled"


def test_ssid_status_calculator_no_ssids():
    """Test the SSID status calculator with no SSIDs."""
    ssids = []
    devices = [
        {"serial": "Q234-ABCD-5678", "status": "online", "model": "MR33", "tags": []}
    ]
    result = SsidStatusCalculator.calculate_ssid_status(ssids, devices)
    assert result == []
