"""Tests for the Meraki SSID status calculator."""
from custom_components.meraki_ha.helpers.ssid_status_calculator import (
    SSIDStatusCalculator as calc,
)


def test_calculate_ssid_status():
    """Test the calculate_ssid_status function."""
    calculator = calc()
    assert calculator.calculate_ssid_status(True, 1) == "online"
    assert calculator.calculate_ssid_status(True, 0) == "online"
    assert calculator.calculate_ssid_status(False, 1) == "offline"
    assert calculator.calculate_ssid_status(False, 0) == "offline"
