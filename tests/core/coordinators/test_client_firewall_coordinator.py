"""Tests for the Meraki client firewall coordinator."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.core.coordinators.client_firewall_coordinator import (
    ClientFirewallCoordinator,
    FIREWALL_RULE_COMMENT,
)

NETWORK_ID = "N_12345"
MOCK_CLIENT_DATA = [{"ip": "192.168.1.100", "mac": "00:11:22:33:44:55"}]
MOCK_FIREWALL_DATA = {"rules": []}


@pytest.mark.asyncio
async def test_fetch_data(hass: HomeAssistant):
    """Test that the coordinator fetches client and firewall data correctly."""
    mock_api_client = MagicMock()
    mock_api_client.network.get_network_clients = AsyncMock(
        return_value=MOCK_CLIENT_DATA
    )
    mock_api_client.appliance.get_network_appliance_l7_firewall_rules = AsyncMock(
        return_value=MOCK_FIREWALL_DATA
    )

    coordinator = ClientFirewallCoordinator(
        hass, mock_api_client, 60, NETWORK_ID
    )

    data = await coordinator._async_update_data()

    assert data["clients"] == MOCK_CLIENT_DATA
    assert data["l7_firewall_rules"] == MOCK_FIREWALL_DATA
    mock_api_client.network.get_network_clients.assert_called_once_with(
        network_id=NETWORK_ID
    )
    mock_api_client.appliance.get_network_appliance_l7_firewall_rules.assert_called_once_with(
        network_id=NETWORK_ID
    )


@pytest.mark.asyncio
async def test_block_client(hass: HomeAssistant):
    """Test that blocking a client calls the API correctly."""
    mock_api_client = MagicMock()
    mock_api_client.appliance.update_network_appliance_l7_firewall_rules = AsyncMock()

    coordinator = ClientFirewallCoordinator(
        hass, mock_api_client, 60, NETWORK_ID
    )
    coordinator.data = {"l7_firewall_rules": {"rules": []}}

    await coordinator.async_block_client("192.168.1.100")

    expected_rules = [
        {
            "policy": "deny",
            "type": "ipRange",
            "value": "192.168.1.100",
            "comment": FIREWALL_RULE_COMMENT,
        }
    ]
    mock_api_client.appliance.update_network_appliance_l7_firewall_rules.assert_called_once_with(
        network_id=NETWORK_ID, rules=expected_rules
    )


@pytest.mark.asyncio
async def test_unblock_client(hass: HomeAssistant):
    """Test that unblocking a client calls the API correctly."""
    mock_api_client = MagicMock()
    mock_api_client.appliance.update_network_appliance_l7_firewall_rules = AsyncMock()

    coordinator = ClientFirewallCoordinator(
        hass, mock_api_client, 60, NETWORK_ID
    )
    coordinator.data = {
        "l7_firewall_rules": {
            "rules": [
                {
                    "policy": "deny",
                    "type": "ipRange",
                    "value": "192.168.1.100",
                    "comment": FIREWALL_RULE_COMMENT,
                }
            ]
        }
    }

    await coordinator.async_unblock_client("192.168.1.100")

    mock_api_client.appliance.update_network_appliance_l7_firewall_rules.assert_called_once_with(
        network_id=NETWORK_ID, rules=[]
    )
