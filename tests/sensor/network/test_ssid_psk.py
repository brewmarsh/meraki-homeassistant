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

    # Rule 1: Prefer 'has_entity_name = True' and 'name = None'
    assert sensor.has_entity_name is True
    assert sensor.name is None

    # Rule 2: Prefer the robust 'unique_id' format (serial_classname_key)
    # Network ID acts as the serial for network-scoped entities.
    assert sensor.unique_id == "N_123_merakissidpsksensor_0"
    assert sensor.native_value == "secret123"

    # Test update with new PSK
    updated_ssid = ssid_data_psk.copy()
    updated_ssid["psk"] = "newsecret"
    coordinator.data["ssids"] = [updated_ssid]

    object.__setattr__(sensor, "async_write_ha_state", MagicMock())
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
