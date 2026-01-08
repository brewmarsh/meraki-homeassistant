"""Tests for the NetworkHandler."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.discovery.handlers.network import NetworkHandler
from custom_components.meraki_ha.sensor.network.meraki_network_info import (
    MerakiNetworkInfoSensor,
)
from custom_components.meraki_ha.sensor.network.network_clients import (
    MerakiNetworkClientsSensor,
)
from custom_components.meraki_ha.sensor.network.network_identity import (
    MerakiNetworkIdentitySensor,
)

MOCK_NETWORK_1 = {"id": "N_1234", "name": "Network 1", "productTypes": ["wireless"]}
MOCK_NETWORK_2 = {"id": "N_5678", "name": "Network 2", "productTypes": ["switch"]}


@pytest.fixture
def mock_coordinator():
    """Fixture for a mock MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {"networks": [MOCK_NETWORK_1, MOCK_NETWORK_2]}
    return coordinator


@pytest.fixture
def mock_network_control_service():
    """Fixture for a mock NetworkControlService."""
    service = MagicMock()
    service.get_network_client_count = MagicMock(return_value=5)
    return service


@pytest.mark.asyncio
async def test_discover_entities_creates_network_sensors(
    mock_coordinator, mock_network_control_service
):
    """Test that discover_entities creates sensors for each network."""
    # Configure mock config entry to enable network sensors
    config_entry = MagicMock()
    config_entry.options = {
        "enable_network_sensors": True,
        "enable_vlan_sensors": False,
    }

    handler = NetworkHandler(
        mock_coordinator, config_entry, mock_network_control_service
    )

    entities = await handler.discover_entities()

    # Network handler creates 3 sensors per network: clients, identity, info
    # 2 networks * 3 sensors = 6 entities
    assert len(entities) == 6

    # Check entity types
    client_sensors = [e for e in entities if isinstance(e, MerakiNetworkClientsSensor)]
    identity_sensors = [
        e for e in entities if isinstance(e, MerakiNetworkIdentitySensor)
    ]
    info_sensors = [e for e in entities if isinstance(e, MerakiNetworkInfoSensor)]

    assert len(client_sensors) == 2
    assert len(identity_sensors) == 2
    assert len(info_sensors) == 2

    # Verify network IDs
    assert client_sensors[0]._network_id == "N_1234"
    assert client_sensors[1]._network_id == "N_5678"
