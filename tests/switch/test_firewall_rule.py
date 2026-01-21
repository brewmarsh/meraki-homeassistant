"""Tests for the Meraki Firewall Rule switch."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const import (
    CONF_ENABLE_FIREWALL_RULES,
)
from custom_components.meraki_ha.switch.firewall_rule import MerakiFirewallRuleSwitch
from custom_components.meraki_ha.switch.setup_helpers import async_setup_switches
from custom_components.meraki_ha.types import MerakiFirewallRule


@pytest.fixture
def mock_coordinator_with_firewall_data(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator with Firewall data."""
    rule1 = MerakiFirewallRule(
        comment="Block Bad Site",
        policy="deny",
        protocol="tcp",
        dest_port="80",
        dest_cidr="1.2.3.4/32",
        src_port="any",
        src_cidr="any",
        syslog_enabled=False,
    )
    rule2 = MerakiFirewallRule(
        comment="Allow Good Site",
        policy="allow",
        protocol="tcp",
        dest_port="443",
        dest_cidr="5.6.7.8/32",
        src_port="any",
        src_cidr="any",
        syslog_enabled=True,
    )
    mock_coordinator.data = {
        "l3_firewall_rules": {"net1": [rule1, rule2]},
    }
    mock_coordinator.is_pending.return_value = False
    return mock_coordinator


@pytest.fixture
def mock_config_entry_with_firewall_rules(mock_config_entry: MagicMock) -> MagicMock:
    """Fixture for a mocked ConfigEntry with Firewall rules enabled."""
    mock_config_entry.options = {CONF_ENABLE_FIREWALL_RULES: True}
    return mock_config_entry


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiAPIClient."""
    return MagicMock()


def test_firewall_rule_switch_creation(
    mock_coordinator_with_firewall_data: MagicMock,
    mock_config_entry_with_firewall_rules: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test that the firewall rule switches are created correctly."""
    hass = MagicMock()
    entities = async_setup_switches(
        hass,
        mock_config_entry_with_firewall_rules,
        mock_coordinator_with_firewall_data,
        mock_meraki_client,
    )

    assert len(entities) == 2
    switch1 = entities[0]
    switch2 = entities[1]

    assert isinstance(switch1, MerakiFirewallRuleSwitch)
    assert switch1.unique_id == "meraki_firewall_rule_net1_0"
    assert switch1.name == "Block Bad Site"
    assert switch1.is_on is False  # policy is deny

    assert isinstance(switch2, MerakiFirewallRuleSwitch)
    assert switch2.unique_id == "meraki_firewall_rule_net1_1"
    assert switch2.name == "Allow Good Site"
    assert switch2.is_on is True  # policy is allow


def test_firewall_rule_switch_creation_disabled(
    mock_coordinator_with_firewall_data: MagicMock,
    mock_config_entry: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Firewall rule switches are not created when the feature is disabled."""
    mock_config_entry.options = {CONF_ENABLE_FIREWALL_RULES: False}
    hass = MagicMock()
    entities = async_setup_switches(
        hass,
        mock_config_entry,
        mock_coordinator_with_firewall_data,
        mock_meraki_client,
    )
    assert len(entities) == 0
