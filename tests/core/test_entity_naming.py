"""Tests for entity naming."""

from unittest.mock import MagicMock
import pytest
from custom_components.meraki_ha.core.entities.meraki_vlan_entity import MerakiVLANEntity
from custom_components.meraki_ha.types import MerakiNetwork

@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {}
    return coordinator

def test_vlan_naming(mock_coordinator):
    """Test the naming of a VLAN entity."""
    config_entry = MagicMock()
    config_entry.options = {}
    config_entry.domain = "meraki_ha"

    network = MerakiNetwork(
        id="N_12345",
        name="Site A",
        organization_id="123",
        product_types=["appliance"],
        time_zone="America/Los_Angeles",
    )
    mock_coordinator.get_network.return_value = network

    vlan = {
        "id": 10,
        "name": "VoIP",
        "applianceIp": "192.168.10.1",
        "subnet": "192.168.10.0/24",
        "ipv6": None,
    }

    entity = MerakiVLANEntity(mock_coordinator, config_entry, "N_12345", vlan)

    # Device name remains the standardized Meraki format
    assert entity.device_info["name"] == "[VLAN 10] VoIP"
    # RESOLVED: Setting name to None ensures the entity inherits the Device Name exactly
    assert entity.name is None


def test_camera_naming(mock_coordinator):
    """Test the naming of a Camera entity."""
    from custom_components.meraki_ha.camera import MerakiRTSPStreamCamera
    from custom_components.meraki_ha.types import MerakiDevice

    config_entry = MagicMock()
    config_entry.options = {}
    mock_coordinator.config_entry = config_entry

    device = MerakiDevice(
        serial="Q2XX-YYYY-YYYY",
        name="Front Door",
        model="MV22",
        mac="00:11:22:33:44:56",
        status="online",
        product_type="camera",
    )
    mock_coordinator.get_device.return_value = device
    camera_service = MagicMock()

    entity = MerakiRTSPStreamCamera(
        mock_coordinator, device, camera_service, config_entry
    )

    assert entity.has_entity_name is True
    # The entity inherits the device name "Front Door" because name is None
    assert entity.name is None
    assert entity.device_info["name"] == "[Camera] Front Door"


def test_network_status_naming(mock_coordinator):
    """Test the naming of a Network Status entity."""
    from custom_components.meraki_ha.binary_sensor.network import MerakiNetworkStatus
    from custom_components.meraki_ha.types import MerakiNetwork

    network = MerakiNetwork(
        id="N_67890",
        name="Warehouse",
        organization_id="456",
        product_types=["switch"],
        time_zone="America/New_York",
    )
    mock_coordinator.get_network.return_value = network

    entity = MerakiNetworkStatus(mock_coordinator, network)
    entity.hass = MagicMock()
    entity.coordinator = mock_coordinator

    # Supplemental entities keep a descriptive name
    assert entity.name == "Uplink status"
    assert entity.device_info["name"] == "[Network] Warehouse"