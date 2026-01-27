"""Test the Meraki SSID PSK sensor."""

from unittest.mock import MagicMock

from custom_components.meraki_ha.sensor.network.ssid_psk import MerakiSSIDPSKSensor


async def test_ssid_psk_sensor() -> None:
    """Test the SSID PSK sensor."""
    coordinator = MagicMock()
    config_entry = MagicMock()

    # Test with PSK present
    ssid_data_psk = {
        "networkId": "N_123",
        "number": 0,
        "name": "PSK SSID",
        "enabled": True,
        "psk": "secret123",
    }

    coordinator.data = {"ssids": [ssid_data_psk]}

    sensor = MerakiSSIDPSKSensor(coordinator, config_entry, ssid_data_psk)
    assert sensor.name == "PSK"
    assert sensor.unique_id == "ssid-N_123-0-psk"
    assert sensor.native_value == "secret123"

    # Test update with new PSK
    updated_ssid = ssid_data_psk.copy()
    updated_ssid["psk"] = "newsecret"
    coordinator.data["ssids"] = [updated_ssid]

    sensor.async_write_ha_state = MagicMock()
    sensor._handle_coordinator_update()
    assert sensor.native_value == "newsecret"

    # Test with no PSK
    ssid_data_no_psk = {
        "networkId": "N_456",
        "number": 1,
        "name": "Open SSID",
        "enabled": True,
        # No psk key
    }

    sensor_open = MerakiSSIDPSKSensor(coordinator, config_entry, ssid_data_no_psk)
    assert sensor_open.native_value is None
