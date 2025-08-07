"""Tests for the Meraki SSID sensors."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.network.ssid_splash_page import (
    MerakiSSIDSplashPageSensor,
)
from custom_components.meraki_ha.sensor.network.ssid_auth_mode import (
    MerakiSSIDAuthModeSensor,
)
from custom_components.meraki_ha.sensor.network.ssid_encryption_mode import (
    MerakiSSIDEncryptionModeSensor,
)
from custom_components.meraki_ha.sensor.network.ssid_wpa_encryption_mode import (
    MerakiSSIDWPAEncryptionModeSensor,
)
from custom_components.meraki_ha.sensor.network.ssid_ip_assignment_mode import (
    MerakiSSIDIPAssignmentModeSensor,
)
from custom_components.meraki_ha.sensor.network.ssid_band_selection import (
    MerakiSSIDBandSelectionSensor,
)
from custom_components.meraki_ha.sensor.network.ssid_per_client_bandwidth_limit import (
    MerakiSSIDPerClientBandwidthLimitSensor,
)
from custom_components.meraki_ha.sensor.network.ssid_per_ssid_bandwidth_limit import (
    MerakiSSIDPerSsidBandwidthLimitSensor,
)
from custom_components.meraki_ha.sensor.network.ssid_visible import (
    MerakiSSIDVisibleSensor,
)


@pytest.fixture
def mock_network_coordinator():
    """Fixture for a mocked MerakiNetworkCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "ssids": [
            {
                "number": 1,
                "name": "SSID 1",
                "splashPage": "None",
                "authMode": "open",
                "encryptionMode": "wpa",
                "wpaEncryptionMode": "WPA2 only",
                "ipAssignmentMode": "NAT mode",
                "bandSelection": "Dual band operation",
                "perClientBandwidthLimitUp": 0,
                "perClientBandwidthLimitDown": 0,
                "perSsidBandwidthLimitUp": 0,
                "perSsidBandwidthLimitDown": 0,
                "visible": True,
                "networkId": "net-123",
            }
        ]
    }
    return coordinator


def test_ssid_sensors(mock_network_coordinator):
    """Test the SSID sensors."""
    ssid_data = mock_network_coordinator.data["ssids"][0]

    # Test with prefix format
    mock_network_coordinator.config_entry.options = {'device_name_format': 'prefix'}
    splash_page_sensor = MerakiSSIDSplashPageSensor(mock_network_coordinator, "net-123", ssid_data)
    assert splash_page_sensor.unique_id == "net-123_1_splash_page"
    assert splash_page_sensor.name == "[Sensor] SSID 1 Splash Page"
    assert splash_page_sensor.native_value == "None"

    # Test with omit format
    mock_network_coordinator.config_entry.options = {'device_name_format': 'omit'}
    splash_page_sensor = MerakiSSIDSplashPageSensor(mock_network_coordinator, "net-123", ssid_data)
    assert splash_page_sensor.name == "SSID 1 Splash Page"
