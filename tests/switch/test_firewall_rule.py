"""Tests for MerakiFirewallRuleSwitch."""

from typing import cast
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.switch.firewall_rule import MerakiFirewallRuleSwitch
from custom_components.meraki_ha.types import MerakiFirewallRule
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_firewall_rule() -> MerakiFirewallRule:
    """Create a mock firewall rule."""
    return cast(
        MerakiFirewallRule,
        {
            "comment": "Allow HTTP",
            "policy": "allow",
            "protocol": "tcp",
            "destPort": "80",
            "destCidr": "any",
            "srcCidr": "any",
        },
    )


@pytest.fixture
def mock_firewall_coordinator(mock_coordinator: MagicMock) -> MagicMock:
    """Create a mock coordinator with firewall data."""
    mock_coordinator.data = {
        "l3_firewall_rules": {
            MOCK_NETWORK["id"]: {
                "rules": [
                    {"comment": "Allow HTTP", "policy": "allow"},
                    {"comment": "Block SSH", "policy": "deny"},
                ]
            }
        }
    }
    mock_coordinator.is_pending = MagicMock(return_value=False)
    mock_coordinator.register_pending_update = MagicMock()
    mock_coordinator.api = MagicMock()
    mock_coordinator.api.appliance = MagicMock()
    mock_coordinator.api.appliance.update_l3_firewall_rules = AsyncMock()
    return mock_coordinator


def test_firewall_rule_switch_initialization(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_firewall_rule: MerakiFirewallRule,
) -> None:
    """Test firewall rule switch initialization."""
    switch = MerakiFirewallRuleSwitch(
        coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        network_id=MOCK_NETWORK["id"],
        rule=mock_firewall_rule,
        rule_index=0,
    )

    assert switch._attr_name == "Allow HTTP"
    assert switch._attr_is_on is True  # policy is "allow"


def test_firewall_rule_switch_deny_policy(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test firewall rule switch with deny policy."""
    deny_rule = cast(
        MerakiFirewallRule,
        {
            "comment": "Block SSH",
            "policy": "deny",
            "protocol": "tcp",
            "destPort": "22",
        },
    )

    switch = MerakiFirewallRuleSwitch(
        coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        network_id=MOCK_NETWORK["id"],
        rule=deny_rule,
        rule_index=1,
    )

    assert switch._attr_is_on is False  # policy is "deny"


def test_firewall_rule_switch_no_comment(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test firewall rule switch without comment uses default name."""
    rule_no_comment = cast(
        MerakiFirewallRule,
        {
            "policy": "allow",
            "protocol": "tcp",
            "destPort": "443",
        },
    )

    switch = MerakiFirewallRuleSwitch(
        coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        network_id=MOCK_NETWORK["id"],
        rule=rule_no_comment,
        rule_index=2,
    )

    assert switch._attr_name == "Rule 3"  # 0-indexed, so rule_index 2 = Rule 3


def test_firewall_rule_switch_requires_network_id(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_firewall_rule: MerakiFirewallRule,
) -> None:
    """Test firewall rule switch raises error without network ID."""
    with pytest.raises(ValueError, match="Network ID cannot be None"):
        MerakiFirewallRuleSwitch(
            coordinator=mock_firewall_coordinator,
            config_entry=mock_config_entry,
            network_id=None,  # type: ignore[arg-type]
            rule=mock_firewall_rule,
            rule_index=0,
        )


@pytest.mark.asyncio
async def test_firewall_rule_switch_turn_on(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test turning on the firewall rule switch."""
    deny_rule = cast(
        MerakiFirewallRule,
        {"comment": "Block Traffic", "policy": "deny"},
    )

    switch = MerakiFirewallRuleSwitch(
        coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        network_id=MOCK_NETWORK["id"],
        rule=deny_rule,
        rule_index=0,
    )

    # Mock async_write_ha_state
    object.__setattr__(switch, "async_write_ha_state", MagicMock())

    await switch.async_turn_on()

    assert switch._attr_is_on is True
    mock_firewall_coordinator.register_pending_update.assert_called()


@pytest.mark.asyncio
async def test_firewall_rule_switch_turn_off(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_firewall_rule: MerakiFirewallRule,
) -> None:
    """Test turning off the firewall rule switch."""
    switch = MerakiFirewallRuleSwitch(
        coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        network_id=MOCK_NETWORK["id"],
        rule=mock_firewall_rule,
        rule_index=0,
    )

    # Mock async_write_ha_state
    object.__setattr__(switch, "async_write_ha_state", MagicMock())

    await switch.async_turn_off()

    assert switch._attr_is_on is False
    mock_firewall_coordinator.register_pending_update.assert_called()


def test_firewall_rule_switch_pending_update_skips_state_update(
    mock_firewall_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_firewall_rule: MerakiFirewallRule,
) -> None:
    """Test that pending update prevents state update."""
    mock_firewall_coordinator.is_pending = MagicMock(return_value=True)

    _ = MerakiFirewallRuleSwitch(
        coordinator=mock_firewall_coordinator,
        config_entry=mock_config_entry,
        network_id=MOCK_NETWORK["id"],
        rule=mock_firewall_rule,
        rule_index=0,
    )

    # State should not be updated when pending
    # The _update_internal_state should return early
    mock_firewall_coordinator.is_pending.assert_called()
