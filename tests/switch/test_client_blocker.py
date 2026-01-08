"""Tests for MerakiClientBlockerSwitch."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.exceptions import HomeAssistantError

from custom_components.meraki_ha.switch.meraki_client_blocker import (
    MerakiClientBlockerSwitch,
)


@pytest.fixture
def mock_client_data() -> dict:
    """Create mock client data."""
    return {
        "id": "client123",
        "mac": "00:11:22:33:44:55",
        "ip": "192.168.1.100",
        "description": "Test Client",
    }


@pytest.fixture
def mock_client_no_ip() -> dict:
    """Create mock client data without IP."""
    return {
        "id": "client456",
        "mac": "AA:BB:CC:DD:EE:FF",
        "description": "Client No IP",
    }


@pytest.fixture
def mock_firewall_coordinator() -> MagicMock:
    """Create a mock SSID firewall coordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "rules": [
            {"policy": "deny", "value": "192.168.1.100"},
        ]
    }
    coordinator.last_update_success = True
    coordinator.async_block_client = AsyncMock()
    coordinator.async_unblock_client = AsyncMock()
    return coordinator


def test_client_blocker_initialization(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_client_data: dict,
) -> None:
    """Test client blocker switch initialization."""
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        client_data=mock_client_data,
    )

    assert switch._client_mac == "00:11:22:33:44:55"
    assert switch._client_ip == "192.168.1.100"
    assert switch._attr_unique_id == "meraki-client-00:11:22:33:44:55-blocker"
    assert switch.entity_description.name == "Internet Access"


def test_client_blocker_blocked_state(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_client_data: dict,
) -> None:
    """Test client blocker shows on when client is blocked."""
    # Client IP is in the deny rules
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        client_data=mock_client_data,
    )

    assert switch._attr_is_on is True  # Client is blocked


def test_client_blocker_unblocked_state(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_client_data: dict,
) -> None:
    """Test client blocker shows off when client is not blocked."""
    # Clear the rules so client is not blocked
    mock_firewall_coordinator.data = {"rules": []}

    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        client_data=mock_client_data,
    )

    assert switch._attr_is_on is False  # Client is not blocked


def test_client_blocker_no_ip_state(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_client_no_ip: dict,
) -> None:
    """Test client blocker with no IP defaults to off."""
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        client_data=mock_client_no_ip,
    )

    assert switch._attr_is_on is False


@pytest.mark.asyncio
async def test_client_blocker_turn_on(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_client_data: dict,
) -> None:
    """Test blocking a client (turn on)."""
    mock_firewall_coordinator.data = {"rules": []}

    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        client_data=mock_client_data,
    )

    await switch.async_turn_on()

    mock_firewall_coordinator.async_block_client.assert_called_once_with(
        "192.168.1.100"
    )


@pytest.mark.asyncio
async def test_client_blocker_turn_off(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_client_data: dict,
) -> None:
    """Test unblocking a client (turn off)."""
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        client_data=mock_client_data,
    )

    await switch.async_turn_off()

    mock_firewall_coordinator.async_unblock_client.assert_called_once_with(
        "192.168.1.100"
    )


@pytest.mark.asyncio
async def test_client_blocker_turn_on_no_ip_raises_error(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_client_no_ip: dict,
) -> None:
    """Test blocking a client without IP raises error."""
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        client_data=mock_client_no_ip,
    )

    with pytest.raises(HomeAssistantError, match="Client IP address is not available"):
        await switch.async_turn_on()


@pytest.mark.asyncio
async def test_client_blocker_turn_off_no_ip_raises_error(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_client_no_ip: dict,
) -> None:
    """Test unblocking a client without IP raises error."""
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        client_data=mock_client_no_ip,
    )

    with pytest.raises(HomeAssistantError, match="Client IP address is not available"):
        await switch.async_turn_off()


@pytest.mark.asyncio
async def test_client_blocker_turn_on_api_error(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_client_data: dict,
) -> None:
    """Test blocking a client handles API errors."""
    mock_firewall_coordinator.async_block_client.side_effect = Exception("API Error")

    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        client_data=mock_client_data,
    )

    with pytest.raises(HomeAssistantError, match="Failed to block client"):
        await switch.async_turn_on()


def test_client_blocker_available(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_client_data: dict,
) -> None:
    """Test client blocker availability."""
    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        client_data=mock_client_data,
    )

    assert switch.available is True


def test_client_blocker_unavailable_when_no_data(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_client_data: dict,
) -> None:
    """Test client blocker unavailable when coordinator has no data."""
    mock_firewall_coordinator.data = None
    mock_firewall_coordinator.last_update_success = True

    switch = MerakiClientBlockerSwitch(
        firewall_coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        client_data=mock_client_data,
    )

    assert switch.available is False
