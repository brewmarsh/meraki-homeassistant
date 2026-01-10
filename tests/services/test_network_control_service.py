"""Tests for the NetworkControlService."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.services.network_control_service import (
    NetworkControlService,
)


@pytest.fixture
def mock_api_client() -> MagicMock:
    """Fixture for a mocked MerakiAPIClient."""
    return MagicMock()


@pytest.fixture
def mock_coordinator_with_clients(mock_coordinator: MagicMock) -> MagicMock:
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataUpdateCoordinator with client data."""
=======
    """Fixture for a mocked MerakiDataCoordinator with client data."""
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
    mock_coordinator.data = {
        "clients": [
            {"networkId": "N_1234", "mac": "00:11:22:33:44:55"},
            {"networkId": "N_1234", "mac": "00:11:22:33:44:66"},
            {"networkId": "N_5678", "mac": "00:11:22:33:44:77"},
        ]
    }
    return mock_coordinator


def test_get_network_client_count(
    mock_api_client: MagicMock, mock_coordinator_with_clients: MagicMock
) -> None:
    """Test that get_network_client_count returns the correct count."""
    service = NetworkControlService(mock_api_client, mock_coordinator_with_clients)

    # Test with a network that has clients
    count = service.get_network_client_count("N_1234")
    assert count == 2

    # Test with a network that has one client
    count = service.get_network_client_count("N_5678")
    assert count == 1

    # Test with a network that has no clients
    count = service.get_network_client_count("N_9999")
    assert count == 0


def test_get_network_client_count_no_clients_data(
    mock_api_client: MagicMock,
) -> None:
    """Test get_network_client_count when there is no client data."""
    coordinator = MagicMock()
    coordinator.data = {}
    service = NetworkControlService(mock_api_client, coordinator)
    count = service.get_network_client_count("N_1234")
    assert count == 0
