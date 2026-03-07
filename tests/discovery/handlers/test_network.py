"""Tests for the NetworkHandler."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const.config import (
    (,
    CONF_ENABLE_CLIENT_STATUS_SENSORS,
    CONF_ENABLE_NETWORK_SENSORS,
    CONF_ENABLE_VLAN_SENSORS,
    ),
)
from custom_components.meraki_ha.core.models.network import MerakiVlan
from custom_components.meraki_ha.discovery.handlers.network import NetworkHandler
from custom_components.meraki_ha.sensor.client.status import MerakiClientStatusSensor
from custom_components.meraki_ha.sensor.network.network_clients import (
    MerakiNetworkClientsSensor,
)
from custom_components.meraki_ha.sensor.network.vlan import MerakiVLANStatusSensor
from custom_components.meraki_ha.types import MerakiNetwork

from custom_components.meraki_ha.const.integration import MOCK_CONFIG_ENTRY, MOCK_NETWORK_1= MerakiNetwork(
    id="N_1234", name="Network 1", organization_id="org1", product_types=["wireless"]
)
MOCK_NETWORK_2 = MerakiNetwork(
    id="N_5678", name="Network 2", organization_id="org1", product_types=["switch"]
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mock MerakiMainCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "networks": [MOCK_NETWORK_1, MOCK_NETWORK_2],
        "vlans": {
            "N_5678": [
                MerakiVlan(id=10, name="Staff", subnet="192.168.10.0/24"),
                MerakiVlan(id=20, name="Guest", subnet="192.168.20.0/24"),
            ]
        },
        "clients": [],  # Initialize empty; specific tests will populate this
    }
    # Mock API for content filtering check
    coordinator.api.appliance.get_network_appliance_content_filtering_categories = (
        MagicMock(return_value={"categories": []})
    )
    return coordinator


@pytest.fixture
def mock_network_control_service():
    """Fixture for a mock NetworkControlService."""
    service = MagicMock()
    service.get_network_client_count = MagicMock(return_value=5)
    return service


async def test_discover_entities_creates_network_sensors(
    mock_coordinator, mock_network_control_service
):
    """Test that discover_entities creates a client sensor for each network."""
    handler = NetworkHandler(
        mock_coordinator, MOCK_CONFIG_ENTRY, mock_network_control_service
    )

    entities = []
    async for entity in handler.discover_entities():
        entities.append(entity)

    assert len(entities) >= 2
    client_sensors = [e for e in entities if isinstance(e, MerakiNetworkClientsSensor)]
    assert len(client_sensors) == 2

    network_ids = sorted([s._network_id for s in client_sensors])
    assert network_ids == ["N_1234", "N_5678"]


async def test_discover_entities_creates_vlan_status_sensors(
    mock_coordinator, mock_network_control_service
):
    """Test that discover_entities creates MerakiVLANStatusSensor for VLANs."""
    handler = NetworkHandler(
        mock_coordinator, MOCK_CONFIG_ENTRY, mock_network_control_service
    )

    entities = []
    async for entity in handler.discover_entities():
        entities.append(entity)

    vlan_sensors = [e for e in entities if isinstance(e, MerakiVLANStatusSensor)]
    assert len(vlan_sensors) == 2

    vlan_ids = sorted([s._vlan.id for s in vlan_sensors])
    assert vlan_ids == [10, 20]

    # Safety check: Ensure old deprecated sensors are no longer present
    for e in entities:
        if "MerakiVLANIPv4EnabledSensor" in str(type(e)):
            pytest.fail("Old VLAN sensor class found!")


async def test_discover_entities_creates_client_status_sensors_when_enabled(
    mock_coordinator, mock_network_control_service
):
    """Test that discover_entities creates client status sensors.

    Uses full data verification.
    """
    # 1. Setup Mock Data
    mock_coordinator.data["clients"] = [
        {
            "mac": "00:11:22:33:44:55",
            "networkId": "N_1234",
            "status": "Online",
            "description": "Client 1",
            "ip": "10.0.0.1",
        },
        {
            "mac": "AA:BB:CC:DD:EE:FF",
            "networkId": "N_5678",
            "status": "Offline",
            "description": "Client 2",
        },
        {
            "mac": "11:22:33:44:55:66",
            "networkId": "N_OTHER",  # Should be ignored (network not in
            # mock_coordinator.data["networks"])
            "status": "Online",
        },
    ]

    # 2. Configure Options
    config_entry = MagicMock()
    config_entry.options = {
        CONF_ENABLE_CLIENT_STATUS_SENSORS: True,
        CONF_ENABLE_NETWORK_SENSORS: True,
        CONF_ENABLE_VLAN_SENSORS: False,
    }

    handler = NetworkHandler(
        mock_coordinator, config_entry, mock_network_control_service
    )

    # 3. Discovery
    entities = []
    async for entity in handler.discover_entities():
        entities.append(entity)

    client_status_sensors = [
        e for e in entities if isinstance(e, MerakiClientStatusSensor)
    ]

    # 4. Assertions
    # We expect 2 sensors (Client 1 and Client 2). Client 3 (N_OTHER) is skipped.
    assert len(client_status_sensors) == 2

    # Verify specific sensor data (ensures deep attribute mapping works)
    sensor1 = next(
        s for s in client_status_sensors if s._client_mac == "00:11:22:33:44:55"
    )
    assert sensor1.native_value == "online"
    assert sensor1.extra_state_attributes["ip_address"] == "10.0.0.1"

    sensor2 = next(
        s for s in client_status_sensors if s._client_mac == "AA:BB:CC:DD:EE:FF"
    )
    assert sensor2.native_value == "offline"
