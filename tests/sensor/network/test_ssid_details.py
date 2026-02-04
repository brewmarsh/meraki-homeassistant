"""Test the Meraki SSID detail sensors."""

from unittest.mock import MagicMock
from homeassistant.const import UnitOfDataRate
from custom_components.meraki_ha.sensor.network.ssid_details import (
    MerakiSSIDTotalUploadLimitSensor,
    MerakiSSIDMinBitrate24GhzSensor,
)

async def test_ssid_total_upload_limit_sensor() -> None:
    """Test the SSID total upload limit sensor."""
    coordinator = MagicMock()
    config_entry = MagicMock()
    ssid_data = {
        "networkId": "N_123",
        "number": 0,
        "name": "Test SSID",
        "enabled": True,
        "perSsidBandwidthLimitUp": 1000,
    }

    coordinator.data = {
        "wireless_settings": {
            "N_123": [ssid_data]
        }
    }

    sensor = MerakiSSIDTotalUploadLimitSensor(coordinator, config_entry, ssid_data, None)

    assert sensor.name == "Total upload limit"
    assert sensor.native_value == 1000
    assert sensor.native_unit_of_measurement == UnitOfDataRate.KILOBITS_PER_SECOND

    # Test update
    new_ssid_data = ssid_data.copy()
    new_ssid_data["perSsidBandwidthLimitUp"] = 2000
    coordinator.data["wireless_settings"]["N_123"] = [new_ssid_data]

    object.__setattr__(sensor, "async_write_ha_state", MagicMock())

    sensor._handle_coordinator_update()
    assert sensor.native_value == 2000

async def test_ssid_min_bitrate_24ghz_sensor() -> None:
    """Test the SSID minimum bitrate 2.4GHz sensor."""
    coordinator = MagicMock()
    config_entry = MagicMock()
    ssid_data = {
        "networkId": "N_123",
        "number": 0,
        "name": "Test SSID",
        "enabled": True,
    }
    rf_profile = {
        "id": "rf_1",
        "twoFourGhzSettings": {"minBitrate": 11}
    }

    coordinator.data = {
        "wireless_settings": {"N_123": [ssid_data]},
        "rf_profiles": {"N_123": [rf_profile]}
    }

    sensor = MerakiSSIDMinBitrate24GhzSensor(coordinator, config_entry, ssid_data, rf_profile)

    assert sensor.name == "Minimum bitrate 2.4GHz"
    assert sensor.native_value == 11

    # Test update
    new_rf_profile = {
        "id": "rf_1",
        "twoFourGhzSettings": {"minBitrate": 12}
    }
    coordinator.data["rf_profiles"]["N_123"] = [new_rf_profile]

    object.__setattr__(sensor, "async_write_ha_state", MagicMock())

    sensor._handle_coordinator_update()
    assert sensor.native_value == 12
