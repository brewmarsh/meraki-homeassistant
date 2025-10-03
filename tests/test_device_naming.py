"""Tests for consistent device name formatting across various entity types."""

import pytest
from unittest.mock import MagicMock

# Import the sensor classes to be tested
from custom_components.meraki_ha.sensor.org.org_clients import (
    MerakiOrganizationSSIDClientsSensor,
)
from custom_components.meraki_ha.sensor.network.network_clients import (
    MerakiNetworkClientsSensor,
)
from custom_components.meraki_ha.sensor.network.vlan import MerakiVLANIDSensor


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = {
        "networks": [
            {
                "id": "net1",
                "name": "Test Network",
                "productTypes": ["appliance", "switch", "wireless"],
            },
        ],
        "vlans": {
            "net1": [
                {"id": 1, "name": "Test VLAN", "enabled": True},
            ]
        },
    }
    return coordinator


def test_org_device_naming(mock_coordinator):
    """Test name formatting for an organization-level device."""
    org_id = "org1"
    org_name = "Test Organization"

    sensor = MerakiOrganizationSSIDClientsSensor(mock_coordinator, org_id, org_name)
    assert sensor.device_info["name"] == "[Organization] Test Organization"


def test_network_device_naming(mock_coordinator):
    """Test name formatting for a network-level device."""
    network_id = "net1"
    network_name = "Test Network"

    network_data = {
        "id": network_id,
        "name": network_name,
        "productTypes": ["wireless"],
    }

    sensor = MerakiNetworkClientsSensor(
        mock_coordinator,
        mock_coordinator.config_entry,
        network_data,
        MagicMock(),
    )
    assert sensor.device_info["name"] == "[Network] Test Network"


def test_vlan_device_naming(mock_coordinator):
    """Test name formatting for a VLAN-level device."""
    network_id = "net1"
    vlan_data = mock_coordinator.data["vlans"]["net1"][0]

    sensor = MerakiVLANIDSensor(
        mock_coordinator, mock_coordinator.config_entry, network_id, vlan_data
    )
    assert sensor.device_info["name"] == "Test VLAN"
