"""Tests for the Meraki VLANs List sensor."""

from unittest.mock import MagicMock

import pytest
from homeassistant.const import EntityCategory

from custom_components.meraki_ha.sensor.network.vlans_list import VlansListSensor
from custom_components.meraki_ha.types import MerakiNetwork, MerakiVlan


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}

    # Create a mock network
    mock_network = MerakiNetwork(
        id="net1",
        name="Test Network",
        organization_id="org1",
        product_types=["appliance"],
    )

    # Create mock VLANs
    vlan1 = MerakiVlan(
        id=10, name="Guest", subnet="192.168.10.0/24", appliance_ip="192.168.10.1"
    )
    vlan2 = MerakiVlan(
        id=20, name="Staff", subnet="192.168.20.0/24", appliance_ip="192.168.20.1"
    )

    coordinator.data = {
        "networks": [mock_network],
        "vlans": {"net1": [vlan1, vlan2]},
        "devices": [],
        "clients": [],
        "ssids": [],
    }
    return coordinator

def test_vlans_list_sensor(mock_coordinator):
    """Test VLANs List sensor creation and state."""
    hass = MagicMock()

    network_data = mock_coordinator.data["networks"][0]

    sensor = VlansListSensor(
        mock_coordinator,
        mock_coordinator.config_entry,
        network_data
    )

    assert sensor.unique_id == "net1_vlans"
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.name == "VLANs"

    # Mock hass/async_write_ha_state
    sensor.hass = hass
    sensor.async_write_ha_state = MagicMock()

    sensor._handle_coordinator_update()

    assert sensor.native_value == 2
    assert sensor.extra_state_attributes["vlans"] == ["Guest", "Staff"]
