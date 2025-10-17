"""Tests for the Meraki VLAN DHCP switch."""
from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const import (
    CONF_ENABLE_VLAN_MANAGEMENT,
)
from custom_components.meraki_ha.switch.setup_helpers import async_setup_switches
from custom_components.meraki_ha.switch.vlan_dhcp import MerakiVLANDHCPSwitch


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "vlans": {
            "net1": [
                {
                    "id": 1,
                    "name": "VLAN 1",
                    "dhcpHandling": "Run a DHCP server",
                },
            ]
        },
    }
    coordinator.is_pending.return_value = False
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: True}
    return entry


@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked MerakiAPIClient."""
    return MagicMock()


def test_vlan_dhcp_switch_creation(
    mock_coordinator, mock_config_entry, mock_meraki_client
):
    """Test that the VLAN DHCP switch is created correctly."""
    hass = MagicMock()
    entities = async_setup_switches(
        hass, mock_config_entry, mock_coordinator, mock_meraki_client
    )

    assert len(entities) == 1
    switch = entities[0]

    assert isinstance(switch, MerakiVLANDHCPSwitch)
    assert switch.unique_id == "meraki_vlan_net1_1_dhcp_handling"
    assert switch.name == "DHCP"
    assert switch.is_on is True


def test_vlan_dhcp_switch_off_state(
    mock_coordinator, mock_config_entry, mock_meraki_client
):
    """Test the off state of the VLAN DHCP switch."""
    mock_coordinator.data["vlans"]["net1"][0][
        "dhcpHandling"
    ] = "Do not respond to DHCP requests"

    hass = MagicMock()
    entities = async_setup_switches(
        hass, mock_config_entry, mock_coordinator, mock_meraki_client
    )

    assert len(entities) == 1
    switch = entities[0]

    assert switch.is_on is False


def test_vlan_dhcp_switch_creation_disabled(
    mock_coordinator, mock_config_entry, mock_meraki_client
):
    """Test that the VLAN DHCP switch is not created if the feature is disabled."""
    mock_config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: False}
    hass = MagicMock()
    entities = async_setup_switches(
        hass, mock_config_entry, mock_coordinator, mock_meraki_client
    )
    assert len(entities) == 0
