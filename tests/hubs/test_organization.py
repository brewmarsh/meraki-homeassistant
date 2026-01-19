"""Tests for the OrganizationHub."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.hubs.organization import OrganizationHub
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_coordinator_with_network(mock_coordinator: MagicMock) -> MagicMock:
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataUpdateCoordinator with a network."""
=======
    """Fixture for a mocked MerakiDataCoordinator with a network."""
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    mock_coordinator.data = {"networks": [MOCK_NETWORK]}
    return mock_coordinator


def test_organization_hub_init(mock_coordinator_with_network: MagicMock) -> None:
    """Test the initialization of the OrganizationHub."""
    hub = OrganizationHub(mock_coordinator_with_network)
    assert hub._coordinator is mock_coordinator_with_network


def test_organization_id_property(mock_coordinator_with_network: MagicMock) -> None:
    """Test the organization_id property."""
    hub = OrganizationHub(mock_coordinator_with_network)
    assert hub.organization_id == MOCK_NETWORK["organizationId"]


def test_organization_id_property_no_data(
    mock_coordinator_with_network: MagicMock,
) -> None:
    """Test the organization_id property when there is no data."""
    mock_coordinator_with_network.data = {}
    hub = OrganizationHub(mock_coordinator_with_network)
    assert hub.organization_id is None


@pytest.mark.asyncio
async def test_async_update_data(mock_coordinator_with_network: MagicMock) -> None:
    """Test the async_update_data method."""
    hub = OrganizationHub(mock_coordinator_with_network)
    assert hub.data == {}
    await hub.async_update_data()
    assert hub.data is mock_coordinator_with_network.data
