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

    async def mock_run_with_cache(key, func, ttl=None):
        return await func()

    client.run_with_cache = AsyncMock(side_effect=mock_run_with_cache)

    return client


@pytest.fixture
def switch_endpoints(mock_client):
    """Fixture for the SwitchEndpoints."""
    return SwitchEndpoints(mock_client)


@pytest.mark.asyncio
async def test_get_device_switch_ports_statuses_normalization(
    switch_endpoints, mock_client
):
    """Test get_device_switch_ports_statuses normalizes portId."""
    mock_client.run_sync.return_value = [{"portId": "1", "enabled": True}]

    result = await switch_endpoints.get_device_switch_ports_statuses("serial")

    assert result == [{"portId": "1", "enabled": True}]
    assert mock_client.run_sync.call_count == 1


@pytest.mark.asyncio
async def test_get_device_switch_ports_statuses_failure(switch_endpoints, mock_client):
    """Test failure raises MerakiConnectionError."""
    metadata = {"tags": ["test"], "operation": "test_op"}
    response = MagicMock()
    response.status_code = 400
    response.json.return_value = {"errors": ["Some API Error"]}

    mock_client.run_sync.side_effect = APIError(metadata, response)

    from custom_components.meraki_ha.core.errors import MerakiConnectionError

    with pytest.raises(MerakiConnectionError):
        await switch_endpoints.get_device_switch_ports_statuses("serial")


@pytest.mark.asyncio
async def test_get_switch_ports_normalization(switch_endpoints, mock_client):
    """Test get_switch_ports normalizes portId."""
    mock_client.run_sync.return_value = [{"portId": "1", "enabled": True}]

    result = await switch_endpoints.get_switch_ports("s1")

    assert result == [{"portId": "1", "enabled": True}]
    assert mock_client.run_sync.call_count == 1


@pytest.mark.asyncio
async def test_get_switch_ports_failure(switch_endpoints, mock_client):
    """Test failure raises MerakiConnectionError."""
    metadata = {"tags": ["test"], "operation": "test_op"}
    response = MagicMock()
    response.status_code = 400
    response.json.return_value = {"errors": ["Some API Error"]}

    mock_client.run_sync.side_effect = APIError(metadata, response)

    from custom_components.meraki_ha.core.errors import MerakiConnectionError

    with pytest.raises(MerakiConnectionError):
        await switch_endpoints.get_switch_ports("s1")
