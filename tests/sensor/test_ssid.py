"""Tests for the Meraki SSID sensor."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.sensor.ssid import (
    create_ssid_sensors,
)
from custom_components.meraki_ha.sensor.ssid_availability import (
    MerakiSSIDAvailabilitySensor,
)
from custom_components.meraki_ha.sensor.ssid_channel import MerakiSSIDChannelSensor
from custom_components.meraki_ha.sensor.ssid_client_count import (
    MerakiSSIDClientCountSensor,
)


async def test_create_ssid_sensors(
    hass: HomeAssistant,
) -> None:
    """Test the create_ssid_sensors function."""
    coordinator = MagicMock()
    coordinator.data = {
        "ssid_0": {
            "number": 0,
            "name": "Test SSID",
            "enabled": True,
            "splashPage": "None",
            "ssidAdminAccessible": False,
            "authMode": "open",
            "encryptionMode": "wpa",
            "wpaEncryptionMode": "WPA2",
            "ipAssignmentMode": "nat",
            "useVlanTagging": False,
            "walledGardenEnabled": False,
            "minBitrate": 11,
            "bandSelection": "dual",
            "perClientBandwidthLimitUp": 0,
            "perClientBandwidthLimitDown": 0,
            "channel": 1,
            "client_count": 2,
        }
    }
    device_data = {
        "serial": "Q234-ABCD-5678",
    }
    ssid_data = {
        "number": 0,
        "name": "Test SSID",
        "unique_id": "ssid_0",
    }
    coordinator.data["ssid_0"]["unique_id"] = "ssid_0"
    sensors = create_ssid_sensors(coordinator, device_data, ssid_data)
    assert len(sensors) == 3
    for sensor in sensors:
        if isinstance(sensor, MerakiSSIDAvailabilitySensor):
            sensor._update_sensor_state()
            assert sensor.native_value == "on"
        elif isinstance(sensor, MerakiSSIDChannelSensor):
            sensor._update_sensor_state()
            assert int(sensor.native_value) == 1
        elif isinstance(sensor, MerakiSSIDClientCountSensor):
            sensor._update_sensor_state()
            assert sensor.native_value == 2
