"""Tests for the NetworkHandler."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.discovery.handlers.network import NetworkHandler
from custom_components.meraki_ha.sensor.network.network_clients import (
    MerakiNetworkClientsSensor,
)
from custom_components.meraki_ha.sensor.network.vlan import MerakiVLANStatusSensor
from custom_components.meraki_ha.types import MerakiNetwork

from ...const import MOCK_CONFIG_ENTRY

MOCK_NETWORK_1 = MerakiNetwork(
    id="N_1234", name="Network 1", organization_id="org1", product_types=["wireless"]
)
MOCK_NETWORK_2 = MerakiNetwork(
    id="N_5678", name="Network 2", organization_id="org1", product_types=["switch"]
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mock MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "networks": [MOCK_NETWORK_1, MOCK_NETWORK_2],
        "vlans": {
            "N_5678": [
                {"id": 10, "name": "Staff", "subnet": "192.168.10.0/24"},
                {"id": 20, "name": "Guest", "subnet": "192.168.20.0/24"},
            ]
        }
    }
    # Mock API for content filtering check
    coordinator.api.appliance.get_network_appliance_content_filtering_categories = MagicMock(
        return_value={"categories": []}
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

    # With recent changes, additional network entities (like TrafficShapingSensor
    # and ContentFilteringSensor) may also be discovered if enabled. For this test,
    # we verify that at least the client sensors are present.
    assert len(entities) >= 2

    client_sensors = [e for e in entities if isinstance(e, MerakiNetworkClientsSensor)]
    assert len(client_sensors) == 2

    network_ids = sorted([s._network_id for s in client_sensors])
    assert network_ids == ["N_1234", "N_5678"]


async def test_discover_entities_creates_vlan_status_sensors(
    mock_coordinator, mock_network_control_service
):
    """Test that discover_entities creates only MerakiVLANStatusSensor for VLANs."""
    handler = NetworkHandler(
        mock_coordinator, MOCK_CONFIG_ENTRY, mock_network_control_service
    )

    entities = []
    async for entity in handler.discover_entities():
        entities.append(entity)

    vlan_sensors = [e for e in entities if isinstance(e, MerakiVLANStatusSensor)]

    # We expect 2 VLAN sensors (one for each VLAN in N_5678)
    # Plus VlansListSensor which is also created

    assert len(vlan_sensors) == 2

    vlan_ids = sorted([s._vlan["id"] for s in vlan_sensors])
    assert vlan_ids == [10, 20]

    # Verify no old sensors are created
    # We can check by class name or just rely on the fact that only MerakiVLANStatusSensor is imported/yielded
    # But just to be sure:
    for e in entities:
        if "MerakiVLANIPv4EnabledSensor" in str(type(e)):
            pytest.fail("Old VLAN sensor class found!")


async def test_discover_entities_creates_client_status_sensors_if_enabled(
    mock_coordinator, mock_network_control_service
):
    """Test that discover_entities creates client status sensors if enabled."""
    from custom_components.meraki_ha.const_conf import (
        CONF_ENABLE_CLIENT_STATUS_SENSORS,
        CONF_ENABLE_NETWORK_SENSORS,
        CONF_ENABLE_TRAFFIC_SHAPING,
        CONF_ENABLE_VLAN_SENSORS,
        CONF_ENABLE_VPN_MANAGEMENT,
    )
    from custom_components.meraki_ha.sensor.client.status import (
        MerakiClientStatusSensor,
    )

    # Mock config entry with client status sensors enabled
    mock_config_entry = MagicMock()
    mock_config_entry.options = {
        CONF_ENABLE_CLIENT_STATUS_SENSORS: True,
        CONF_ENABLE_NETWORK_SENSORS: True,
        CONF_ENABLE_VPN_MANAGEMENT: False,
        CONF_ENABLE_TRAFFIC_SHAPING: False,
        CONF_ENABLE_VLAN_SENSORS: False,
    }

    # Add clients to coordinator data
    mock_coordinator.data["clients"] = [
        # Network 1 Client
        {
            "mac": "00:11:22:33:44:55",
            "networkId": "N_1234",
            "status": "Online",
            "description": "Client 1",
            "ip": "10.0.0.1",
        },
        # Network 2 Client
        {
            "mac": "AA:BB:CC:DD:EE:FF",
            "networkId": "N_5678",
            "status": "Offline",
            "description": "Client 2",
        },
        # Client not in known network (should be skipped)
        {
            "mac": "11:22:33:44:55:66",
            "networkId": "N_9999",
            "status": "Online",
        },
    ]

    handler = NetworkHandler(
        mock_coordinator, mock_config_entry, mock_network_control_service
    )

    entities = []
    async for entity in handler.discover_entities():
        entities.append(entity)

    # Filter for client status sensors
    client_sensors = [e for e in entities if isinstance(e, MerakiClientStatusSensor)]

    # Should find 2 clients (one for N_1234, one for N_5678)
    assert len(client_sensors) == 2

    # Verify attributes
    sensor1 = next(s for s in client_sensors if s._client_mac == "00:11:22:33:44:55")
    assert sensor1.native_value == "online"
    assert sensor1.extra_state_attributes["ip_address"] == "10.0.0.1"

    sensor2 = next(s for s in client_sensors if s._client_mac == "AA:BB:CC:DD:EE:FF")
    assert sensor2.native_value == "offline"
