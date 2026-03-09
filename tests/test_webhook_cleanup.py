"""Tests for Meraki webhook registration idempotency and cleanup."""

from unittest.mock import AsyncMock, patch
import pytest
from custom_components.meraki_ha.core.api.endpoints.network import NetworkEndpoints

@pytest.fixture
def mock_api_client():
    """Mock the Meraki API client protocol."""
    client = AsyncMock()
    client.dashboard = AsyncMock()
    client.organization = AsyncMock()
    # Mock run_sync to just return the result of calling the func if it's not a mock
    async def side_effect(func, *args, **kwargs):
        if isinstance(func, AsyncMock):
            return await func(*args, **kwargs)
        return func(*args, **kwargs)
    client.run_sync.side_effect = side_effect
    return client

@pytest.fixture
def network_endpoints(mock_api_client):
    """Create NetworkEndpoints with a mock client."""
    return NetworkEndpoints(mock_api_client)

@pytest.mark.asyncio
async def test_register_webhook_exact_match(network_endpoints, mock_api_client):
    """Test that an exact match reuses the existing webhook and skips creation."""
    network_id = "n123"
    webhook_url = "https://example.com/webhook"
    config_entry_id = "entry123"
    webhook_name = f"Home Assistant Webhook - {config_entry_id}"

    mock_api_client.organization.get_organization_networks.return_value = [{"id": network_id}]

    # Existing webhooks include an exact match
    existing_webhooks = [
        {"id": "wh1", "name": webhook_name, "url": webhook_url}
    ]

    # Mock the direct API call used in the refactored code
    mock_api_client.dashboard.networks.getNetworkWebhooksHttpServers = AsyncMock(return_value=existing_webhooks)

    webhook_ids = await network_endpoints.register_webhook(webhook_url, "secret", config_entry_id)

    assert webhook_ids == ["wh1"]
    # createNetworkWebhooksHttpServer should NOT be called
    assert mock_api_client.dashboard.networks.createNetworkWebhooksHttpServer.call_count == 0

@pytest.mark.asyncio
async def test_register_webhook_cleanup_orphans(network_endpoints, mock_api_client):
    """Test that orphaned webhooks (same name, diff URL OR diff name, same URL) are deleted."""
    network_id = "n123"
    webhook_url = "https://example.com/webhook"
    config_entry_id = "entry123"
    webhook_name = f"Home Assistant Webhook - {config_entry_id}"

    mock_api_client.organization.get_organization_networks.return_value = [{"id": network_id}]

    # Existing webhooks include orphans
    existing_webhooks = [
        {"id": "wh_old_url", "name": webhook_name, "url": "https://old.com/webhook"},
        {"id": "wh_other_name", "name": "Other HA", "url": webhook_url},
        {"id": "wh_unrelated", "name": "Unrelated", "url": "https://unrelated.com"}
    ]

    mock_api_client.dashboard.networks.getNetworkWebhooksHttpServers = AsyncMock(return_value=existing_webhooks)
    mock_api_client.dashboard.networks.createNetworkWebhooksHttpServer = AsyncMock(return_value={"id": "wh_new"})

    with patch.object(network_endpoints, "delete_webhook", new_callable=AsyncMock) as mock_delete:
        webhook_ids = await network_endpoints.register_webhook(webhook_url, "secret", config_entry_id)

        # wh_old_url and wh_other_name should be deleted
        assert mock_delete.call_count == 2
        deleted_ids = [call.args[1] for call in mock_delete.call_args_list]
        assert "wh_old_url" in deleted_ids
        assert "wh_other_name" in deleted_ids
        assert "wh_unrelated" not in deleted_ids

    assert webhook_ids == ["wh_new"]
    # Should call create once
    mock_api_client.dashboard.networks.createNetworkWebhooksHttpServer.assert_called_once()

@pytest.mark.asyncio
async def test_register_webhook_multiple_networks(network_endpoints, mock_api_client):
    """Test registration across multiple networks."""
    networks = [{"id": "n1"}, {"id": "n2"}]
    webhook_url = "https://example.com/webhook"
    config_entry_id = "entry123"

    mock_api_client.organization.get_organization_networks.return_value = networks
    mock_api_client.dashboard.networks.getNetworkWebhooksHttpServers = AsyncMock(return_value=[])
    mock_api_client.dashboard.networks.createNetworkWebhooksHttpServer = AsyncMock()
    mock_api_client.dashboard.networks.createNetworkWebhooksHttpServer.side_effect = [{"id": "wh_n1"}, {"id": "wh_n2"}]

    webhook_ids = await network_endpoints.register_webhook(webhook_url, "secret", config_entry_id)

    assert webhook_ids == ["wh_n1", "wh_n2"]
    assert mock_api_client.dashboard.networks.createNetworkWebhooksHttpServer.call_count == 2
