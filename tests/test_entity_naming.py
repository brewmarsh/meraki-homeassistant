"""Test entity naming conventions for Meraki HA."""
from unittest.mock import MagicMock

from custom_components.meraki_ha.camera import MerakiCamera
from custom_components.meraki_ha.sensor.network.network_clients import (
    MerakiNetworkClientsSensor,
)
from custom_components.meraki_ha.sensor.network.vlan import MerakiVLANIDSensor
from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork


async def test_camera_naming(hass, mock_coordinator, mock_config_entry):
    """Test that the camera entity name is set correctly."""
    # GIVEN a mock Meraki device for a camera
    camera_device = MerakiDevice(
        serial="Q234-ABCD-5678",
        name="Front Door",
        model="MV12",
        lan_ip="1.2.3.4",
        status="online",
        network_id="N_12345",
    )

    # GIVEN a mock camera service
    mock_camera_service = MagicMock()

    # WHEN the MerakiCamera entity is created
    camera_entity = MerakiCamera(
        coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        device=camera_device,
        camera_service=mock_camera_service,
    )

    # THEN the entity name should match the device name
    assert camera_entity.name == "Front Door"


async def test_vlan_naming(hass, mock_coordinator, mock_config_entry):
    """Test that the VLAN entity name is set correctly."""
    # GIVEN a mock network
    mock_network = MerakiNetwork(id="N_12345", name="Main Office")
    mock_coordinator.data = {"networks": [mock_network]}

    # GIVEN mock VLAN data
    vlan_data = {"id": 10, "name": "Guest"}

    # WHEN the MerakiVLAN entity is created
    vlan_entity = MerakiVLANIDSensor(
        coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        network_id="N_12345",
        vlan=vlan_data,
    )

    # THEN the device name should be formatted correctly
    assert vlan_entity.device_info["name"] == "Main Office VLAN 10 Guest"


async def test_network_entity_naming(hass, mock_coordinator, mock_config_entry):
    """Test that the network entity name is set correctly."""
    # GIVEN a mock network
    mock_network = MerakiNetwork(id="N_12345", name="Main Office")

    # GIVEN a mock network control service
    mock_network_control_service = MagicMock()

    # WHEN the MerakiNetworkClientsSensor entity is created
    network_entity = MerakiNetworkClientsSensor(
        coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        network_data=mock_network,
        network_control_service=mock_network_control_service,
    )

    # THEN the entity name should start with the network name
    assert network_entity.name == "Main Office Clients"
