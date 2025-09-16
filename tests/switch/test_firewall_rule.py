"""Tests for the Meraki firewall rule switch."""

import pytest
from unittest.mock import MagicMock, AsyncMock

from custom_components.meraki_ha.switch.setup_helpers import async_setup_switches
from custom_components.meraki_ha.const import (
    CONF_ENABLE_FIREWALL_RULES,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {
        "device_name_format": "omit",
        CONF_ENABLE_FIREWALL_RULES: True,
    }
    coordinator.data = {
        "networks": [{"id": "net1", "name": "Test Network"}],
        "l3_firewall_rules": {
            "net1": {
                "rules": [
                    {
                        "comment": "Allow all",
                        "policy": "allow",
                        "protocol": "any",
                        "destPort": "any",
                        "destCidr": "any",
                        "srcPort": "any",
                        "srcCidr": "any",
                        "syslogEnabled": False,
                    }
                ]
            }
        },
    }
    coordinator.is_pending.return_value = False
    coordinator.api = MagicMock()
    coordinator.api.appliance.update_l3_firewall_rules = AsyncMock()
    return coordinator


def test_firewall_rule_switch_creation(mock_coordinator):
    """Test that the firewall rule switch is created correctly."""
    hass = MagicMock()

    # Run the setup
    switches = async_setup_switches(
        hass, mock_coordinator.config_entry, mock_coordinator
    )

    # Find the specific switch
    firewall_rule_switch = next(s for s in switches if "Allow all" in s.name)

    # Assertions for Firewall Rule Switch
    assert (
        firewall_rule_switch.unique_id == "meraki_firewall_rule_net1_0"
    )
    assert firewall_rule_switch.name == "Allow all"
    assert firewall_rule_switch.is_on is True


@pytest.mark.asyncio
async def test_firewall_rule_switch_turn_off(mock_coordinator):
    """Test turning off the firewall rule switch."""
    hass = MagicMock()
    switches = async_setup_switches(
        hass, mock_coordinator.config_entry, mock_coordinator
    )
    firewall_rule_switch = next(s for s in switches if "Allow all" in s.name)
    firewall_rule_switch.hass = hass

    await firewall_rule_switch.async_turn_off()

    mock_coordinator.api.appliance.update_l3_firewall_rules.assert_called_once_with(
        network_id="net1",
        rules=[
            {
                "comment": "Allow all",
                "policy": "deny",
                "protocol": "any",
                "destPort": "any",
                "destCidr": "any",
                "srcPort": "any",
                "srcCidr": "any",
                "syslogEnabled": False,
            }
        ],
    )


@pytest.mark.asyncio
async def test_firewall_rule_switch_turn_on(mock_coordinator):
    """Test turning on the firewall rule switch."""
    hass = MagicMock()
    # Set initial state to off
    mock_coordinator.data["l3_firewall_rules"]["net1"]["rules"][0][
        "policy"
    ] = "deny"
    switches = async_setup_switches(
        hass, mock_coordinator.config_entry, mock_coordinator
    )
    firewall_rule_switch = next(s for s in switches if "Allow all" in s.name)
    firewall_rule_switch.hass = hass

    await firewall_rule_switch.async_turn_on()

    mock_coordinator.api.appliance.update_l3_firewall_rules.assert_called_once_with(
        network_id="net1",
        rules=[
            {
                "comment": "Allow all",
                "policy": "allow",
                "protocol": "any",
                "destPort": "any",
                "destCidr": "any",
                "srcPort": "any",
                "srcCidr": "any",
                "syslogEnabled": False,
            }
        ],
    )
