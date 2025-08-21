"""Tests for the Meraki Client Blocker switch entity."""

import pytest
from unittest.mock import MagicMock, AsyncMock

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.switch.meraki_client_blocker import (
    MerakiClientBlockerSwitch,
)
from custom_components.meraki_ha.core.coordinators.client_firewall_coordinator import (
    ClientFirewallCoordinator,
    FIREWALL_RULE_COMMENT,
)

NETWORK_ID = "N_12345"
CLIENT_IP = "192.168.1.100"
CLIENT_MAC = "00:11:22:33:44:55"
CLIENT_DATA = {"ip": CLIENT_IP, "mac": CLIENT_MAC, "vlan": 10, "ssid": "Test SSID"}


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked ClientFirewallCoordinator."""
    coordinator = MagicMock(spec=ClientFirewallCoordinator)
    coordinator.data = {
        "clients": [CLIENT_DATA],
        "l7_firewall_rules": {"rules": []},
    }
    coordinator.async_block_client = AsyncMock()
    coordinator.async_unblock_client = AsyncMock()
    return coordinator


@pytest.mark.asyncio
async def test_switch_entity_properties(hass: HomeAssistant, mock_coordinator):
    """Test the properties of the switch entity when not blocked."""
    config_entry = MockConfigEntry()
    entity = MerakiClientBlockerSwitch(
        coordinator=mock_coordinator,
        config_entry=config_entry,
        client_data=CLIENT_DATA,
    )

    assert entity.unique_id == f"meraki-client-{CLIENT_MAC}-blocker"
    assert entity.name == "Internet Access"
    assert not entity.is_on
    assert entity.extra_state_attributes["vlan"] == 10
    assert entity.extra_state_attributes["ssid"] == "Test SSID"


@pytest.mark.asyncio
async def test_switch_entity_properties_blocked(hass: HomeAssistant, mock_coordinator):
    """Test the properties of the switch entity when blocked."""
    mock_coordinator.data["l7_firewall_rules"]["rules"] = [
        {
            "policy": "deny",
            "type": "ipRange",
            "value": CLIENT_IP,
            "comment": FIREWALL_RULE_COMMENT,
        }
    ]
    config_entry = MockConfigEntry()
    entity = MerakiClientBlockerSwitch(
        coordinator=mock_coordinator,
        config_entry=config_entry,
        client_data=CLIENT_DATA,
    )

    assert entity.is_on


@pytest.mark.asyncio
async def test_turn_on(hass: HomeAssistant, mock_coordinator):
    """Test that turning on the switch calls the coordinator to block."""
    config_entry = MockConfigEntry()
    entity = MerakiClientBlockerSwitch(
        coordinator=mock_coordinator,
        config_entry=config_entry,
        client_data=CLIENT_DATA,
    )

    await entity.async_turn_on()

    mock_coordinator.async_block_client.assert_called_once_with(CLIENT_IP)


@pytest.mark.asyncio
async def test_turn_off(hass: HomeAssistant, mock_coordinator):
    """Test that turning off the switch calls the coordinator to unblock."""
    config_entry = MockConfigEntry()
    entity = MerakiClientBlockerSwitch(
        coordinator=mock_coordinator,
        config_entry=config_entry,
        client_data=CLIENT_DATA,
    )

    await entity.async_turn_off()

    mock_coordinator.async_unblock_client.assert_called_once_with(CLIENT_IP)
