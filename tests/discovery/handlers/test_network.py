"""Tests for the NetworkHandler."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.discovery.handlers.network import NetworkHandler
from custom_components.meraki_ha.sensor.network.network_clients import (
    MerakiNetworkClientsSensor,
)

from ...const import MOCK_CONFIG_ENTRY

MOCK_NETWORK_1 = {"id": "N_1234", "name": "Network 1"}
MOCK_NETWORK_2 = {"id": "N_5678", "name": "Network 2"}


@pytest.fixture
def mock_coordinator():
<<<<<<< HEAD
<<<<<<< HEAD
    """Fixture for a mock MerakiDataUpdateCoordinator."""
=======
<<<<<<< HEAD
    """Fixture for a mock MerakiDataUpdateCoordinator."""
=======
    """Fixture for a mock MerakiDataCoordinator."""
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    """Fixture for a mock MerakiDataCoordinator."""
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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

    assert len(entities) == 2
    assert isinstance(entities[0], MerakiNetworkClientsSensor)
    assert isinstance(entities[1], MerakiNetworkClientsSensor)
    assert entities[0]._network_id == "N_1234"
    assert entities[1]._network_id == "N_5678"
