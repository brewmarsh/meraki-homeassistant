"""Tests for the NetworkHandler."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.discovery.handlers.network import NetworkHandler
from custom_components.meraki_ha.sensor.network.network_clients import (
    MerakiNetworkClientsSensor,
)
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
    coordinator.data = {"networks": [MOCK_NETWORK_1, MOCK_NETWORK_2]}
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

    entities = await handler.discover_entities()

    # With recent changes, additional network entities (like TrafficShapingSensor and ContentFilteringSensor)
    # may also be discovered if enabled. For this test, we verify that at least the client sensors are present.
    assert len(entities) >= 2

    client_sensors = [e for e in entities if isinstance(e, MerakiNetworkClientsSensor)]
    assert len(client_sensors) == 2

    network_ids = sorted([s._network_id for s in client_sensors])
    assert network_ids == ["N_1234", "N_5678"]
