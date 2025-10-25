"""Tests for the OrganizationHub."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.hubs.organization import OrganizationHub
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {"networks": [MOCK_NETWORK]}
    return coordinator


def test_organization_hub_init(mock_coordinator):
    """Test the initialization of the OrganizationHub."""
    hub = OrganizationHub(mock_coordinator)
    assert hub._coordinator is mock_coordinator


def test_organization_id_property(mock_coordinator):
    """Test the organization_id property."""
    hub = OrganizationHub(mock_coordinator)
    assert hub.organization_id == MOCK_NETWORK["organizationId"]


def test_organization_id_property_no_data(mock_coordinator):
    """Test the organization_id property when there is no data."""
    mock_coordinator.data = {}
    hub = OrganizationHub(mock_coordinator)
    assert hub.organization_id is None


@pytest.mark.asyncio
async def test_async_update_data(mock_coordinator):
    """Test the async_update_data method."""
    hub = OrganizationHub(mock_coordinator)
    assert hub.data == {}
    await hub.async_update_data()
    assert hub.data is mock_coordinator.data
