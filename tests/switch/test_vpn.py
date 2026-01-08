"""Tests for MerakiVPNSwitch."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.switch.vpn import MerakiVPNSwitch
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_vpn_coordinator(mock_coordinator: MagicMock) -> MagicMock:
    """Create a mock coordinator with VPN data."""
    mock_coordinator.data = {
        "vpn_status": {
            MOCK_NETWORK["id"]: {
                "mode": "hub",
                "subnets": [{"localSubnet": "192.168.1.0/24"}],
            }
        }
    }
    mock_coordinator.is_pending = MagicMock(return_value=False)
    mock_coordinator.register_pending_update = MagicMock()
    mock_coordinator.api = MagicMock()
    mock_coordinator.api.appliance = MagicMock()
    mock_coordinator.api.appliance.update_vpn_status = AsyncMock()
    return mock_coordinator


def test_vpn_switch_initialization(
    mock_vpn_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test VPN switch initialization."""
    switch = MerakiVPNSwitch(
        coordinator=mock_vpn_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
    )

    assert switch._attr_name == "Site-to-Site VPN"
    assert switch._attr_unique_id == f"vpn_{MOCK_NETWORK['id']}"
    assert switch._attr_has_entity_name is True


def test_vpn_switch_enabled_state(
    mock_vpn_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test VPN switch shows on when mode is not disabled."""
    switch = MerakiVPNSwitch(
        coordinator=mock_vpn_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
    )

    assert switch._attr_is_on is True


def test_vpn_switch_disabled_state(
    mock_vpn_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test VPN switch shows off when mode is disabled."""
    mock_vpn_coordinator.data = {
        "vpn_status": {MOCK_NETWORK["id"]: {"mode": "disabled"}}
    }

    switch = MerakiVPNSwitch(
        coordinator=mock_vpn_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
    )

    assert switch._attr_is_on is False


@pytest.mark.asyncio
async def test_vpn_switch_turn_on(
    mock_vpn_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test turning on the VPN switch."""
    mock_vpn_coordinator.data = {
        "vpn_status": {MOCK_NETWORK["id"]: {"mode": "disabled"}}
    }

    switch = MerakiVPNSwitch(
        coordinator=mock_vpn_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
    )

    # Mock async_write_ha_state
    switch.async_write_ha_state = MagicMock()

    await switch.async_turn_on()

    assert switch._attr_is_on is True
    mock_vpn_coordinator.register_pending_update.assert_called()
    mock_vpn_coordinator.api.appliance.update_vpn_status.assert_called_once_with(
        network_id=MOCK_NETWORK["id"],
        mode="hub",
    )


@pytest.mark.asyncio
async def test_vpn_switch_turn_off(
    mock_vpn_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test turning off the VPN switch."""
    switch = MerakiVPNSwitch(
        coordinator=mock_vpn_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
    )

    # Mock async_write_ha_state
    switch.async_write_ha_state = MagicMock()

    await switch.async_turn_off()

    assert switch._attr_is_on is False
    mock_vpn_coordinator.register_pending_update.assert_called()
    mock_vpn_coordinator.api.appliance.update_vpn_status.assert_called_once_with(
        network_id=MOCK_NETWORK["id"],
        mode="disabled",
    )


def test_vpn_switch_handle_coordinator_update(
    mock_vpn_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test VPN switch handles coordinator updates."""
    switch = MerakiVPNSwitch(
        coordinator=mock_vpn_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
    )

    # Mock async_write_ha_state
    switch.async_write_ha_state = MagicMock()

    # Initial state is on (mode=hub)
    assert switch._attr_is_on is True

    # Update coordinator data to disabled
    mock_vpn_coordinator.data = {
        "vpn_status": {MOCK_NETWORK["id"]: {"mode": "disabled"}}
    }

    # Trigger update
    switch._handle_coordinator_update()

    assert switch._attr_is_on is False
    switch.async_write_ha_state.assert_called()


def test_vpn_switch_pending_update_skips_state_update(
    mock_vpn_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test that pending update prevents state update."""
    mock_vpn_coordinator.is_pending = MagicMock(return_value=True)

    _ = MerakiVPNSwitch(
        coordinator=mock_vpn_coordinator,
        config_entry=mock_config_entry,
        network=MOCK_NETWORK,
    )

    # is_pending should have been called
    mock_vpn_coordinator.is_pending.assert_called()
