"""Tests for the Meraki VLAN sensors."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.core.models.network import MerakiVlan
from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from custom_components.meraki_ha.sensor.network.vlan import MerakiVLANStatusSensor
from custom_components.meraki_ha.types import MerakiNetwork


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiMainCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}

    # Mock API for content filtering check (required by NetworkHandler)
    coordinator.api.appliance.get_network_appliance_content_filtering_categories = (
        MagicMock(return_value={"categories": []})
    )

    # Create a mock network using the Dataclass
    mock_network = MerakiNetwork(
        id="net1",
        name="Test Network",
        organization_id="org1",
        product_types=["appliance"],
    )

    # Create mock VLANs using MerakiVlan objects
    vlan1 = MerakiVlan(
        id=1,
        name="VLAN 1",
        subnet="192.168.1.0/24",
        appliance_ip="192.168.1.1",
        ipv6={
            "enabled": True,
            "prefix": "2001:db8:1::/64",
        },
        dhcp_handling="Run a DHCP server",
    )

    coordinator.data = {
        "networks": [mock_network],
        "vlans": {"net1": [vlan1]},
        "devices": [],
        "clients": [],
        "ssids": [],
    }

    # Mock get_network needed by BaseMerakiEntity
    coordinator.get_network.return_value = mock_network

    return coordinator


async def test_vlan_sensor_creation(mock_coordinator):
    """Test that VLAN sensors are created correctly."""
    # Run the setup
    discovery_service = DeviceDiscoveryService(
        mock_coordinator,
        mock_coordinator,
        mock_coordinator,
        mock_coordinator,
        mock_coordinator,
        mock_coordinator,
        mock_coordinator,
        mock_coordinator,
        mock_coordinator.config_entry,
        MagicMock(),
        MagicMock(),
        MagicMock(),
        MagicMock(),
    )
    await discovery_service.discover_entities()
    sensors = discovery_service.all_entities

    # Filter for VLAN sensors
    vlan_sensors = [s for s in sensors if isinstance(s, MerakiVLANStatusSensor)]

    # Expect 1 sensor for the 1 VLAN
    assert len(vlan_sensors) == 1

    sensor = vlan_sensors[0]

    # Assertions for VLAN Status Sensor
    # Unique ID format from get_vlan_entity_id
    assert sensor.unique_id == "meraki_vlan_net1_1_status"

    # Name from MerakiVLANStatusSensor
    assert sensor.name == "VLAN 1 (VLAN 1) Subnet"

    # Native value is subnet
    assert sensor.native_value == "192.168.1.0/24"

    # Attributes
    assert sensor.extra_state_attributes["vlan_id"] == 1
    assert sensor.extra_state_attributes["appliance_ip"] == "192.168.1.1"
    assert sensor.extra_state_attributes["ipv6_enabled"] is True

    # Device Info - Virtual Controller
    # Device Name should be "Site: Test Network" because resolve_device_info
    # does that and MerakiNetworkEntity (which MerakiVLANEntity inherits from)
    # uses resolve_device_info
    # AND MerakiNetworkEntity calls resolve_device_info which we modified.

    # Wait, MerakiVLANEntity uses MerakiNetworkEntity.device_info which uses
    # resolve_device_info.
    # So assertions on device_info should verify Virtual Controller pattern.

    assert sensor.device_info["identifiers"] == {(DOMAIN, "network_net1")}
    assert sensor.device_info["name"] == "Site: Test Network"
