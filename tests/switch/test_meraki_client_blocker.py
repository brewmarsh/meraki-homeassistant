"""Tests for the Meraki Client Blocker switch."""

from unittest.mock import AsyncMock, MagicMock, PropertyMock

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.switch.meraki_client_blocker import (
    MerakiClientBlockerSwitch,
)
from custom_components.meraki_ha.core.coordinators.ssid_firewall_coordinator import (
    SsidFirewallCoordinator,
)

MOCK_CLIENT = {
    "mac": "00:11:22:33:44:55",
    "ip": "192.168.1.100",
    "description": "Test Client",
    "networkId": "N_12345",
}

MOCK_BLOCKED_RULE = {
    "policy": "deny",
    "type": "ipRange",
    "value": "192.168.1.100",
    "comment": "Managed by Home Assistant",
}


@pytest.fixture
def mock_coordinator():
    """Mock the SsidFirewallCoordinator."""
    coordinator = MagicMock(spec=SsidFirewallCoordinator)
    coordinator.async_block_client = AsyncMock()
    coordinator.async_unblock_client = AsyncMock()
    type(coordinator).data = PropertyMock(return_value={"rules": []})
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Mock the ConfigEntry."""
    return MockConfigEntry(domain="meraki_ha", entry_id="test_entry")


def test_initial_state_unblocked(mock_coordinator, mock_config_entry):
    """Test the initial state when the client is not blocked."""
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        client_data=MOCK_CLIENT,
    )
    assert not switch.is_on


def test_initial_state_blocked(mock_coordinator, mock_config_entry):
    """Test the initial state when the client is blocked."""
    type(mock_coordinator).data = PropertyMock(
        return_value={"rules": [MOCK_BLOCKED_RULE]}
    )
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        client_data=MOCK_CLIENT,
    )
    assert switch.is_on


async def test_turn_on_blocks_client(mock_coordinator, mock_config_entry):
    """Test that turning the switch on calls the block_client method."""
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        client_data=MOCK_CLIENT,
    )
    await switch.async_turn_on()
    mock_coordinator.async_block_client.assert_called_once_with(MOCK_CLIENT["ip"])


async def test_turn_off_unblocks_client(mock_coordinator, mock_config_entry):
    """Test that turning the switch off calls the unblock_client method."""
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        client_data=MOCK_CLIENT,
    )
    await switch.async_turn_off()
    mock_coordinator.async_unblock_client.assert_called_once_with(MOCK_CLIENT["ip"])


def test_state_updates_on_coordinator_update(mock_coordinator, mock_config_entry):
    """Test that the switch state updates when the coordinator data changes."""
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        client_data=MOCK_CLIENT,
    )
    switch.async_write_ha_state = MagicMock()
    assert not switch.is_on

    # Simulate coordinator update with a blocking rule
    type(mock_coordinator).data = PropertyMock(
        return_value={"rules": [MOCK_BLOCKED_RULE]}
    )
    switch._handle_coordinator_update()

    assert switch.is_on

    # Simulate coordinator update with no rules
    type(mock_coordinator).data = PropertyMock(return_value={"rules": []})
    switch._handle_coordinator_update()

    assert not switch.is_on