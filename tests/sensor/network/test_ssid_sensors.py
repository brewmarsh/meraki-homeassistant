"""Tests for the Meraki SSID sensors."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.network.ssid import (
    MerakiSSIDAvailabilitySensor,
    MerakiSSIDChannelSensor,
    MerakiSSIDClientCountSensor,
    MerakiSSIDSplashPageSensor,
    MerakiSSIDAuthModeSensor,
    MerakiSSIDEncryptionModeSensor,
    MerakiSSIDWPAEncryptionModeSensor,
    MerakiSSIDIPAssignmentModeSensor,
    MerakiSSIDBandSelectionSensor,
    MerakiSSIDPerClientBandwidthLimitSensor,
    MerakiSSIDPerSsidBandwidthLimitSensor,
    MerakiSSIDVisibleSensor,
)


@pytest.fixture
def mock_data_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "ssids": [
            {
                "number": 1,
                "name": "SSID 1",
                "enabled": True,
                "splashPage": "None",
                "authMode": "open",
                "encryptionMode": "wpa",
                "wpaEncryptionMode": "WPA2 only",
                "ipAssignmentMode": "NAT mode",
                "bandSelection": "Dual band operation",
                "perClientBandwidthLimitUp": 10,
                "perClientBandwidthLimitDown": 20,
                "perSsidBandwidthLimitUp": 30,
                "perSsidBandwidthLimitDown": 40,
                "visible": True,
                "availability": "Available",
                "channel": 6,
                "clientCount": 5,
                "networkId": "net-123",
                "productType": "ssid",
            }
        ]
    }
    return coordinator


def test_all_ssid_sensors(mock_data_coordinator):
    """Test all the SSID sensors."""
    ssid_data = mock_data_coordinator.data["ssids"][0]
    config_entry = mock_data_coordinator.config_entry
    config_entry.options = {"device_name_format": "prefix"}

    # Test each sensor
    sensors_to_test = [
        (MerakiSSIDAvailabilitySensor, "enabled", "Availability", "ssid-net-123-1-enabled"),
        (MerakiSSIDChannelSensor, "channel", "Channel", "ssid-net-123-1-channel"),
        (MerakiSSIDClientCountSensor, "clientCount", "Client Count", "ssid-net-123-1-clientCount"),
        (MerakiSSIDSplashPageSensor, "splashPage", "Splash Page", "ssid-net-123-1-splashPage"),
        (MerakiSSIDAuthModeSensor, "authMode", "Auth Mode", "ssid-net-123-1-authMode"),
        (MerakiSSIDEncryptionModeSensor, "encryptionMode", "Encryption Mode", "ssid-net-123-1-encryptionMode"),
        (MerakiSSIDWPAEncryptionModeSensor, "wpaEncryptionMode", "WPA Encryption Mode", "ssid-net-123-1-wpaEncryptionMode"),
        (MerakiSSIDIPAssignmentModeSensor, "ipAssignmentMode", "IP Assignment Mode", "ssid-net-123-1-ipAssignmentMode"),
        (MerakiSSIDBandSelectionSensor, "bandSelection", "Band Selection", "ssid-net-123-1-bandSelection"),
        (MerakiSSIDVisibleSensor, "visible", "Visible", "ssid-net-123-1-visible"),
    ]

    for sensor_class, attribute, name, unique_id_suffix in sensors_to_test:
        sensor = sensor_class(mock_data_coordinator, config_entry, ssid_data)
        assert sensor.unique_id == unique_id_suffix
        assert sensor.name == name
        assert sensor.device_info["name"] == "[Ssid] SSID 1"
        assert sensor.native_value == ssid_data[attribute]

    # Test bandwidth sensors
    up_client_sensor = MerakiSSIDPerClientBandwidthLimitSensor(mock_data_coordinator, config_entry, ssid_data, "up")
    assert up_client_sensor.unique_id == "ssid-net-123-1-per-client-bandwidth-limit-up"
    assert up_client_sensor.name == "Per-Client Bandwidth Limit Up"
    assert up_client_sensor.native_value == 10

    down_client_sensor = MerakiSSIDPerClientBandwidthLimitSensor(mock_data_coordinator, config_entry, ssid_data, "down")
    assert down_client_sensor.unique_id == "ssid-net-123-1-per-client-bandwidth-limit-down"
    assert down_client_sensor.name == "Per-Client Bandwidth Limit Down"
    assert down_client_sensor.native_value == 20

    up_ssid_sensor = MerakiSSIDPerSsidBandwidthLimitSensor(mock_data_coordinator, config_entry, ssid_data, "up")
    assert up_ssid_sensor.unique_id == "ssid-net-123-1-per-ssid-bandwidth-limit-up"
    assert up_ssid_sensor.name == "Per-SSID Bandwidth Limit Up"
    assert up_ssid_sensor.native_value == 30

    down_ssid_sensor = MerakiSSIDPerSsidBandwidthLimitSensor(mock_data_coordinator, config_entry, ssid_data, "down")
    assert down_ssid_sensor.unique_id == "ssid-net-123-1-per-ssid-bandwidth-limit-down"
    assert down_ssid_sensor.name == "Per-SSID Bandwidth Limit Down"
    assert down_ssid_sensor.native_value == 40
