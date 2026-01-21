"""Tests for the Meraki VLAN DHCP switch."""

from unittest.mock import MagicMock
import dataclasses

import pytest

from custom_components.meraki_ha.const import (
    CONF_ENABLE_VLAN_MANAGEMENT,
)
from custom_components.meraki_ha.switch.setup_helpers import async_setup_switches
from custom_components.meraki_ha.switch.vlan_dhcp import MerakiVLANDHCPSwitch
from custom_components.meraki_ha.types import MerakiVlan


@pytest.fixture
def mock_coordinator_with_vlan_data(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator with VLAN data."""
    vlan1 = MerakiVlan(
        id=1,
        name="VLAN 1",
        dhcp_handling="Run a DHCP server"
    )
    mock_coordinator.data = {
        "vlans": {
            "net1": [vlan1]
        },
    }
    mock_coordinator.is_pending.return_value = False
    return mock_coordinator


@pytest.fixture
def mock_config_entry_with_vlan_management(mock_config_entry: MagicMock) -> MagicMock:
    """Fixture for a mocked ConfigEntry with VLAN management enabled."""
    mock_config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: True}
    return mock_config_entry


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiAPIClient."""
    return MagicMock()


def test_vlan_dhcp_switch_creation(
    mock_coordinator_with_vlan_data: MagicMock,
    mock_config_entry_with_vlan_management: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test that the VLAN DHCP switch is created correctly."""
    hass = MagicMock()
    entities = async_setup_switches(
        hass,
        mock_config_entry_with_vlan_management,
        mock_coordinator_with_vlan_data,
        mock_meraki_client,
    )

    assert len(entities) == 1
    switch = entities[0]

    assert isinstance(switch, MerakiVLANDHCPSwitch)
    assert switch.unique_id == "meraki_vlan_net1_1_dhcp_handling"
    assert switch.name == "DHCP"
    assert switch.is_on is True  # type: ignore[attr-defined]


def test_vlan_dhcp_switch_off_state(
    mock_coordinator_with_vlan_data: MagicMock,
    mock_config_entry_with_vlan_management: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test the off state of the VLAN DHCP switch."""
    # Modify the dataclass object
    mock_coordinator_with_vlan_data.data["vlans"]["net1"][0].dhcp_handling = (
        "Do not respond to DHCP requests"
    )

    hass = MagicMock()
    entities = async_setup_switches(
        hass,
        mock_config_entry_with_vlan_management,
        mock_coordinator_with_vlan_data,
        mock_meraki_client,
    )

    assert len(entities) == 1
    switch = entities[0]

    assert switch.is_on is False  # type: ignore[attr-defined]


def test_vlan_dhcp_switch_creation_disabled(
    mock_coordinator_with_vlan_data: MagicMock,
    mock_config_entry: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test that the VLAN DHCP switch is not created if the feature is disabled."""
    mock_config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: False}
    hass = MagicMock()
    entities = async_setup_switches(
        hass,
        mock_config_entry,
        mock_coordinator_with_vlan_data,
        mock_meraki_client,
    )
    assert len(entities) == 0
