"""Tests for the Meraki base entity."""

from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.entity import MerakiEntity


async def test_meraki_entity(hass: HomeAssistant) -> None:
    """Test the Meraki entity."""
    coordinator = MagicMock()
    device_data = {"serial": "test-serial", "name": "Test Device"}
    entity = MerakiEntity(coordinator, device_data)

    assert entity.device_info["identifiers"] == {(DOMAIN, "test-serial")}
    assert entity.device_info["name"] == "Test Device"
    assert entity.device_info["manufacturer"] == "Cisco Meraki"
    assert entity.device_info["model"] == "Unknown"
    assert entity.device_info["sw_version"] == ""


async def test_meraki_entity_with_ssid(hass: HomeAssistant) -> None:
    """Test the Meraki entity with an SSID."""
    coordinator = MagicMock()
    ssid_data = {"name": "Test SSID", "number": 0, "networkId": "test-network-id"}
    entity = MerakiEntity(coordinator, ssid_data, ssid_data)

    assert entity.device_info["identifiers"] == {(DOMAIN, "test-network-id_0")}
