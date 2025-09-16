"""Tests for the Meraki VLAN DHCP switch."""

import pytest
from unittest.mock import MagicMock, AsyncMock

from custom_components.meraki_ha.switch.setup_helpers import async_setup_switches
from custom_components.meraki_ha.const import (
    CONF_ENABLE_VLAN_MANAGEMENT,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {
        "device_name_format": "omit",
        CONF_ENABLE_VLAN_MANAGEMENT: True,
    }
    coordinator.data = {
        "networks": [{"id": "net1", "name": "Test Network"}],
        "vlans": {
            "net1": [
                {
                    "id": 1,
                    "name": "VLAN 1",
                    "subnet": "192.168.1.0/24",
                    "applianceIp": "192.168.1.1",
                    "dhcpHandling": "Run a DHCP server",
                },
            ]
        },
    }
    coordinator.is_pending.return_value = False
    coordinator.api = MagicMock()
    coordinator.api.appliance.update_network_vlan = AsyncMock()
    return coordinator


def test_vlan_dhcp_switch_creation(mock_coordinator):
    """Test that the VLAN DHCP switch is created correctly."""
    hass = MagicMock()

    # Run the setup
    switches = async_setup_switches(
        hass, mock_coordinator.config_entry, mock_coordinator
    )

    # Find the specific switch
    vlan_dhcp_switch = next(s for s in switches if "DHCP" in s.name)

    # Assertions for VLAN DHCP Switch
    assert vlan_dhcp_switch.unique_id == "meraki_vlan_net1_1_dhcp_handling"
    assert vlan_dhcp_switch.name == "VLAN 1 DHCP"
    assert vlan_dhcp_switch.is_on is True


@pytest.mark.asyncio
async def test_vlan_dhcp_switch_turn_off(mock_coordinator):
    """Test turning off the VLAN DHCP switch."""
    hass = MagicMock()
    switches = async_setup_switches(
        hass, mock_coordinator.config_entry, mock_coordinator
    )
    vlan_dhcp_switch = next(s for s in switches if "DHCP" in s.name)
    vlan_dhcp_switch.hass = hass

    await vlan_dhcp_switch.async_turn_off()

    mock_coordinator.api.appliance.update_network_vlan.assert_called_once_with(
        network_id="net1",
        vlan_id=1,
        dhcpHandling="Do not respond to DHCP requests",
    )


@pytest.mark.asyncio
async def test_vlan_dhcp_switch_turn_on(mock_coordinator):
    """Test turning on the VLAN DHCP switch."""
    hass = MagicMock()
    # Set initial state to off
    mock_coordinator.data["vlans"]["net1"][0]["dhcpHandling"] = "Do not respond to DHCP requests"
    switches = async_setup_switches(
        hass, mock_coordinator.config_entry, mock_coordinator
    )
    vlan_dhcp_switch = next(s for s in switches if "DHCP" in s.name)
    vlan_dhcp_switch.hass = hass

    await vlan_dhcp_switch.async_turn_on()

    mock_coordinator.api.appliance.update_network_vlan.assert_called_once_with(
        network_id="net1",
        vlan_id=1,
        dhcpHandling="Run a DHCP server",
    )
