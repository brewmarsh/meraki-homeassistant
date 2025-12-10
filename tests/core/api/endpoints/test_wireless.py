"""Tests for the Wireless Endpoints."""

from unittest.mock import AsyncMock, MagicMock
import pytest
from custom_components.meraki_ha.core.api.endpoints.wireless import WirelessEndpoints

@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.dashboard = MagicMock()
    client.run_sync = AsyncMock()
    return client

@pytest.fixture
def wireless(mock_client):
    """Fixture for the WirelessEndpoints."""
    return WirelessEndpoints(mock_client)

async def test_create_identity_psk(wireless, mock_client):
    """Test create_identity_psk."""
    mock_client.run_sync.return_value = {"id": "test_id"}

    result = await wireless.create_identity_psk(
        network_id="net1",
        number="0",
        name="test",
        group_policy_id="policy1",
        passphrase="pass",
    )

    assert result == {"id": "test_id"}
    mock_client.run_sync.assert_called_once()
    args, kwargs = mock_client.run_sync.call_args
    assert kwargs["networkId"] == "net1"
    assert kwargs["number"] == "0"
    assert kwargs["name"] == "test"
    assert kwargs["groupPolicyId"] == "policy1"
    assert kwargs["passphrase"] == "pass"

async def test_delete_identity_psk(wireless, mock_client):
    """Test delete_identity_psk."""
    mock_client.run_sync.return_value = None

    await wireless.delete_identity_psk(
        network_id="net1",
        number="0",
        identity_psk_id="psk1",
    )

    mock_client.run_sync.assert_called_once()
    args, kwargs = mock_client.run_sync.call_args
    assert kwargs["networkId"] == "net1"
    assert kwargs["number"] == "0"
    assert kwargs["identityPskId"] == "psk1"
