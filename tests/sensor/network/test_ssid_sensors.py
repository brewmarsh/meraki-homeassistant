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
        "ssid_1": {
            "unique_id": "ssid_1",
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
        }
    }
    return coordinator


def test_ssid_sensors(mock_network_coordinator):
    """Test the SSID sensors."""
    ssid_data = mock_network_coordinator.data["ssid_1"]

    splash_page_sensor = MerakiSSIDSplashPageSensor(mock_network_coordinator, ssid_data)
    assert splash_page_sensor.unique_id == "ssid_1_splash_page"
    assert splash_page_sensor.name == "SSID 1 Splash Page"
    assert splash_page_sensor.native_value == "None"

    auth_mode_sensor = MerakiSSIDAuthModeSensor(mock_network_coordinator, ssid_data)
    assert auth_mode_sensor.unique_id == "ssid_1_auth_mode"
    assert auth_mode_sensor.name == "SSID 1 Auth Mode"
    assert auth_mode_sensor.native_value == "open"

    encryption_mode_sensor = MerakiSSIDEncryptionModeSensor(
        mock_network_coordinator, ssid_data
    )
    assert encryption_mode_sensor.unique_id == "ssid_1_encryption_mode"
    assert encryption_mode_sensor.name == "SSID 1 Encryption Mode"
    assert encryption_mode_sensor.native_value == "wpa"

    wpa_encryption_mode_sensor = MerakiSSIDWPAEncryptionModeSensor(
        mock_network_coordinator, ssid_data
    )
    assert wpa_encryption_mode_sensor.unique_id == "ssid_1_wpa_encryption_mode"
    assert wpa_encryption_mode_sensor.name == "SSID 1 WPA Encryption Mode"
    assert wpa_encryption_mode_sensor.native_value == "WPA2 only"

    ip_assignment_mode_sensor = MerakiSSIDIPAssignmentModeSensor(
        mock_network_coordinator, ssid_data
    )
    assert ip_assignment_mode_sensor.unique_id == "ssid_1_ip_assignment_mode"
    assert ip_assignment_mode_sensor.name == "SSID 1 IP Assignment Mode"
    assert ip_assignment_mode_sensor.native_value == "NAT mode"

    band_selection_sensor = MerakiSSIDBandSelectionSensor(
        mock_network_coordinator, ssid_data
    )
    assert band_selection_sensor.unique_id == "ssid_1_band_selection"
    assert band_selection_sensor.name == "SSID 1 Band Selection"
    assert band_selection_sensor.native_value == "Dual band operation"

    per_client_bw_up_sensor = MerakiSSIDPerClientBandwidthLimitSensor(
        mock_network_coordinator, ssid_data, "up"
    )
    assert (
        per_client_bw_up_sensor.unique_id
        == "ssid_1_per_client_bandwidth_limit_up"
    )
    assert (
        per_client_bw_up_sensor.name == "SSID 1 Per-Client Bandwidth Limit Up"
    )
    assert per_client_bw_up_sensor.native_value == 0

    per_client_bw_down_sensor = MerakiSSIDPerClientBandwidthLimitSensor(
        mock_network_coordinator, ssid_data, "down"
    )
    assert (
        per_client_bw_down_sensor.unique_id
        == "ssid_1_per_client_bandwidth_limit_down"
    )
    assert (
        per_client_bw_down_sensor.name
        == "SSID 1 Per-Client Bandwidth Limit Down"
    )
    assert per_client_bw_down_sensor.native_value == 0

    per_ssid_bw_up_sensor = MerakiSSIDPerSsidBandwidthLimitSensor(
        mock_network_coordinator, ssid_data, "up"
    )
    assert (
        per_ssid_bw_up_sensor.unique_id == "ssid_1_per_ssid_bandwidth_limit_up"
    )
    assert (
        per_ssid_bw_up_sensor.name == "SSID 1 Per-SSID Bandwidth Limit Up"
    )
    assert per_ssid_bw_up_sensor.native_value == 0

    per_ssid_bw_down_sensor = MerakiSSIDPerSsidBandwidthLimitSensor(
        mock_network_coordinator, ssid_data, "down"
    )
    assert (
        per_ssid_bw_down_sensor.unique_id
        == "ssid_1_per_ssid_bandwidth_limit_down"
    )
    assert (
        per_ssid_bw_down_sensor.name == "SSID 1 Per-SSID Bandwidth Limit Down"
    )
    assert per_ssid_bw_down_sensor.native_value == 0

    visible_sensor = MerakiSSIDVisibleSensor(mock_network_coordinator, ssid_data)
    assert visible_sensor.unique_id == "ssid_1_visible"
    assert visible_sensor.name == "SSID 1 Visible"
    assert visible_sensor.native_value is True
