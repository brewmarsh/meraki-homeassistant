"""Tests for switch normalization endpoints."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from meraki.exceptions import APIError

from custom_components.meraki_ha.core.api.endpoints.switch import SwitchEndpoints


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.run_sync = AsyncMock()
    return client


@pytest.fixture
def switch_endpoints(mock_client):
    """Fixture for the SwitchEndpoints."""
    return SwitchEndpoints(mock_client)


@pytest.mark.asyncio
async def test_get_organization_switch_ports_normalization(
    switch_endpoints, mock_client
):
    """Test get_organization_switch_ports normalizes portId."""
    mock_client.run_sync.return_value = [{"portId": "1", "enabled": True}]

    result = await switch_endpoints.get_organization_switch_ports("org_id")

    assert result == [{"portId": "1", "enabled": True}]
    assert mock_client.run_sync.call_count == 1


@pytest.mark.asyncio
async def test_get_organization_switch_ports_failure(switch_endpoints, mock_client):
    """Test failure gracefully returns empty list."""
    metadata = {"tags": ["test"], "operation": "test_op"}
    response = MagicMock()
    response.status_code = 400
    response.json.return_value = {"errors": ["Some API Error"]}

    # Instantiate the REAL APIError, no module patching needed
    mock_client.run_sync.side_effect = APIError(metadata, response)

    result = await switch_endpoints.get_organization_switch_ports("org_id")

    assert result == []


@pytest.mark.asyncio
async def test_get_device_switch_ports_normalization(switch_endpoints, mock_client):
    """Test get_device_switch_ports normalizes portId."""
    mock_client.run_sync.return_value = [{"portId": "1", "enabled": True}]

    result = await switch_endpoints.get_device_switch_ports("serial")

    assert result == [{"portId": "1", "enabled": True}]
    assert mock_client.run_sync.call_count == 1


@pytest.mark.asyncio
async def test_get_device_switch_ports_failure(switch_endpoints, mock_client):
    """Test failure gracefully returns empty list."""
    metadata = {"tags": ["test"], "operation": "test_op"}
    response = MagicMock()
    response.status_code = 400
    response.json.return_value = {"errors": ["Some API Error"]}

    mock_client.run_sync.side_effect = APIError(metadata, response)

    result = await switch_endpoints.get_device_switch_ports("serial")

    assert result == []


@pytest.mark.asyncio
async def test_get_switch_ports_normalization(switch_endpoints, mock_client):
    """Test get_switch_ports normalizes portId."""
    mock_client.run_sync.return_value = [{"portId": "1", "enabled": True}]

    result = await switch_endpoints.get_switch_ports(["s1"])

    # The batch switch port endpoint maps serials to their ports
    assert result == {"s1": [{"portId": "1", "enabled": True}]}
    assert mock_client.run_sync.call_count == 1


@pytest.mark.asyncio
async def test_get_switch_ports_failure(switch_endpoints, mock_client):
    """Test failure gracefully returns empty dict."""
    metadata = {"tags": ["test"], "operation": "test_op"}
    response = MagicMock()
    response.status_code = 400
    response.json.return_value = {"errors": ["Some API Error"]}

    mock_client.run_sync.side_effect = APIError(metadata, response)

    result = await switch_endpoints.get_switch_ports(["s1"])

    # The batch switch port endpoint returns an empty dict on failure
    assert result == {}
