"""Tests for Meraki Wireless Radio sensors."""

from unittest.mock import MagicMock, patch

from homeassistant.components.sensor import SensorEntityDescription

from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.discovery.providers import WirelessRadioProvider
from custom_components.meraki_ha.sensor.device.wireless_radio import (
    MerakiWirelessRadioSensor,
)


def test_wireless_radio_sensor_update():
    """Test the wireless radio sensor update."""
    coordinator = MagicMock()
    device = MerakiDevice(
        serial="serial1",
        wireless_radio_settings={
            "twoFourGhzSettings": {"channel": 6, "targetPower": 15},
            "fiveGhzSettings": {"channel": 149, "targetPower": 18},
        }
    )
    coordinator.get_device.return_value = device

    config_entry = MagicMock()

    description = SensorEntityDescription(
        key="2.4ghz_channel",
        name="2.4GHz channel",
    )

    # Mock resolve_device_info to avoid issues in test
    with patch(
        "custom_components.meraki_ha.sensor.device.wireless_radio.resolve_device_info",
        return_value={},
    ):
        sensor = MerakiWirelessRadioSensor(
            coordinator,
            device,
            config_entry,
            description,
            "twoFourGhzSettings",
            "channel"
        )

        # Mock async_write_ha_state
        sensor.async_write_ha_state = MagicMock()

        assert sensor.native_value == 6

        # Test update
        device.wireless_radio_settings["twoFourGhzSettings"]["channel"] = 11
        sensor._update_state()
        assert sensor.native_value == 11

def test_wireless_radio_provider():
    """Test the wireless radio provider."""
    coordinator = MagicMock()
    device = MerakiDevice(
        serial="serial1",
        wireless_radio_settings={
            "twoFourGhzSettings": {"channel": 6, "targetPower": 15},
            "fiveGhzSettings": {"channel": 149, "targetPower": 18},
        }
    )
    config_entry = MagicMock()

    with patch(
        "custom_components.meraki_ha.sensor.device.wireless_radio.resolve_device_info",
        return_value={},
    ):
        entities = WirelessRadioProvider.get_entities(
            coordinator, device, config_entry
        )

        assert len(entities) == 4
        assert any(e.entity_description.key == "2.4ghz_channel" for e in entities)
        assert any(e.entity_description.key == "5ghz_channel" for e in entities)
        assert any(e.entity_description.key == "2.4ghz_target_power" for e in entities)
        assert any(e.entity_description.key == "target_power" for e in entities)
