"""Tests for the Meraki VLAN DHCP switch."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const.config import CONF_ENABLE_VLAN_MANAGEMENT
from custom_components.meraki_ha.core.models.network import MerakiVlan
from custom_components.meraki_ha.switch.setup_helpers import async_setup_switches
from custom_components.meraki_ha.switch.vlan_dhcp import MerakiVLANDHCPSwitch
from custom_components.meraki_ha.types import MerakiNetwork


@pytest.fixture
def mock_coordinator_with_vlan_data(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiMainCoordinator with VLAN data."""
    vlan1 = MerakiVlan(
        id="1",
        name="VLAN 1",
        subnet="192.168.1.0/24",
        appliance_ip="192.168.1.1",
        dhcp_handling="Run a DHCP server",
    )
    network = MerakiNetwork(id="net1", name="Network 1")
    mock_coordinator.data = {
        "vlans": {"net1": [vlan1]},
        "networks": [network],
    }
    mock_coordinator.is_pending.return_value = False

    def get_network(network_id):
        if network_id == "net1":
            return network
        return None

    mock_coordinator.get_network = MagicMock(side_effect=get_network)
    return mock_coordinator


@pytest.fixture
def mock_config_entry_with_vlan_management(mock_config_entry: MagicMock) -> MagicMock:
    """Fixture for a mocked ConfigEntry with VLAN management enabled."""
    mock_config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: True}
    return mock_config_entry


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiApiClientProtocol."""
    return MagicMock()


def test_vlan_dhcp_switch_creation(
    mock_coordinator_with_vlan_data: MagicMock,
    mock_config_entry_with_vlan_management: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test that the VLAN DHCP switch is created correctly."""
    hass = MagicMock()
    entities: list = []
    def mock_add_entities(new_entities, update_before_add=False):
        entities.extend(new_entities)

    async_setup_switches(
        hass,
        mock_config_entry_with_vlan_management,
        mock_coordinator_with_vlan_data,
        mock_meraki_client,
        mock_add_entities,
    )

    assert len(entities) == 1
    switch = entities[0]

    assert isinstance(switch, MerakiVLANDHCPSwitch)
    assert switch.unique_id == "meraki_vlan_net1_1_dhcp_handling"

    # RESOLVED: Asserting the descriptive name from beta
    assert switch.name == "VLAN 1 (VLAN 1) DHCP"
    assert switch.is_on is True

    # Check extra_state_attributes (Retained from feat branch)
    attrs = switch.extra_state_attributes
    assert attrs["vlan_id"] == "1"
    assert attrs["vlan_name"] == "VLAN 1"
    assert attrs["subnet"] == "192.168.1.0/24"
    assert attrs["gateway"] == "192.168.1.1"


def test_vlan_dhcp_switch_attributes(
    mock_coordinator: MagicMock,
    mock_config_entry_with_vlan_management: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test the extra state attributes of the VLAN DHCP switch."""
    vlan = MerakiVlan(
        id="20",
        name="Guest",
        subnet="192.168.20.0/24",
        appliance_ip="192.168.20.1",
        dhcp_handling="Run a DHCP server",
    )
    network = MerakiNetwork(id="net1", name="Network 1")
    mock_coordinator.data = {
        "vlans": {"net1": [vlan]},
        "networks": [network],
    }

    def get_network(network_id):
        if network_id == "net1":
            return network
        return None

    mock_coordinator.get_network = MagicMock(side_effect=get_network)
    mock_coordinator.is_pending.return_value = False

    hass = MagicMock()
    entities: list = []
    def mock_add_entities(new_entities, update_before_add=False):
        entities.extend(new_entities)

    async_setup_switches(
        hass,
        mock_config_entry_with_vlan_management,
        mock_coordinator,
        mock_meraki_client,
        mock_add_entities,
    )

    assert len(entities) == 1
    switch = entities[0]

    assert switch.name == "Guest (VLAN 20) DHCP"
    attrs = switch.extra_state_attributes
    assert attrs["subnet"] == "192.168.20.0/24"
    assert attrs["gateway"] == "192.168.20.1"


def test_vlan_dhcp_switch_off_state(
    mock_coordinator_with_vlan_data: MagicMock,
    mock_config_entry_with_vlan_management: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test the off state of the VLAN DHCP switch."""
    # Modify the object state to reflect DHCP disabled
    mock_coordinator_with_vlan_data.data["vlans"]["net1"][
        0
    ].dhcp_handling = "Do not respond to DHCP requests"

    hass = MagicMock()
    entities: list = []
    def mock_add_entities(new_entities, update_before_add=False):
        entities.extend(new_entities)

    async_setup_switches(
        hass,
        mock_config_entry_with_vlan_management,
        mock_coordinator_with_vlan_data,
        mock_meraki_client,
        mock_add_entities,
    )

    assert len(entities) == 1
    switch = entities[0]

    assert switch.is_on is False


def test_vlan_dhcp_switch_creation_disabled(
    mock_coordinator_with_vlan_data: MagicMock,
    mock_config_entry: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test that the VLAN DHCP switch is not created if the feature is disabled."""
    mock_config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: False}
    hass = MagicMock()
    entities: list = []
    def mock_add_entities(new_entities, update_before_add=False):
        entities.extend(new_entities)

    async_setup_switches(
        hass,
        mock_config_entry,
        mock_coordinator_with_vlan_data,
        mock_meraki_client,
        mock_add_entities,
    )
    assert len(entities) == 0
