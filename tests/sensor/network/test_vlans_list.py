"""Tests for the Meraki VLANs list sensor."""

from unittest.mock import MagicMock

import pytest
from homeassistant.const import EntityCategory

from custom_components.meraki_ha.const import CONF_ENABLE_VLAN_MANAGEMENT
from custom_components.meraki_ha.sensor.setup_helpers import async_setup_sensors
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
        id="1",
        name="VLAN 1",
        subnet="192.168.1.0/24",
        appliance_ip="192.168.1.1",
    )
    vlan2 = MerakiVlan(
        id="2",
        name="VLAN 2",
        subnet="192.168.2.0/24",
        appliance_ip="192.168.2.1",
    )

    coordinator.data = {
        "networks": [mock_network],
        "vlans": {"net1": [vlan1, vlan2]},
        "devices": [],
        "clients": [],
        "ssids": [],
    }
    return coordinator


def test_vlans_list_sensor_creation_enabled(mock_coordinator):
    """Test that VLANs list sensor is created when enabled."""
    hass = MagicMock()

    # Enable the option
    mock_coordinator.config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: True}

    # Run the setup
    sensors = async_setup_sensors(hass, mock_coordinator.config_entry, mock_coordinator)

    # Filter for VlansListSensor
    vl_sensors = [s for s in sensors if s.__class__.__name__ == "VlansListSensor"]
    assert len(vl_sensors) == 1

    sensor = vl_sensors[0]
    assert sensor.unique_id == "net1_vlans"
    assert sensor.name == "VLANs"
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC

    # Mock hass for the sensor
    sensor.hass = hass

    # Mock async_write_ha_state
    sensor.async_write_ha_state = MagicMock()

    # Simulate update
    sensor._handle_coordinator_update()
    assert sensor.native_value == 2
    assert len(sensor.extra_state_attributes["vlans"]) == 2
