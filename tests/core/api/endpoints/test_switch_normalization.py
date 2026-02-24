"""Tests for Switch Port normalization."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.api.endpoints.organization import (
    OrganizationEndpoints,
)
from custom_components.meraki_ha.core.api.endpoints.switch import SwitchEndpoints


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.dashboard = MagicMock()
    client.run_sync = AsyncMock()
    client.organization_id = "org123"
    return client


@pytest.fixture
def organization_endpoints(mock_client):
    """Fixture for OrganizationEndpoints."""
    return OrganizationEndpoints(mock_client)


@pytest.fixture
def switch_endpoints(mock_client):
    """Fixture for SwitchEndpoints."""
    return SwitchEndpoints(mock_client)


@pytest.mark.asyncio
async def test_get_organization_switch_ports_statuses_normalization(
    organization_endpoints, mock_client
):
    """Test that {} is normalized to [] for organization switch ports statuses."""
    # Mock API returning empty dict
    mock_client.run_sync.return_value = {}

    result = await organization_endpoints.get_organization_switch_ports_statuses()

    assert result == []
    mock_client.run_sync.assert_called_once()


@pytest.mark.asyncio
async def test_get_device_switch_ports_statuses_normalization(
    switch_endpoints, mock_client
):
    """Test that {} is normalized to [] for device switch ports statuses."""
    # Mock API returning empty dict
    mock_client.run_sync.return_value = {}

    result = await switch_endpoints.get_device_switch_ports_statuses("serial123")

    assert result == []
    mock_client.run_sync.assert_called_once()


@pytest.mark.asyncio
async def test_get_switch_ports_normalization(switch_endpoints, mock_client):
    """Test that {} is normalized to [] for get_switch_ports."""
    # Mock API returning empty dict
    mock_client.run_sync.return_value = {}

    result = await switch_endpoints.get_switch_ports("serial123")

    assert result == []
    mock_client.run_sync.assert_called_once()
