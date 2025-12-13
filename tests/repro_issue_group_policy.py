"""Reproduction script for group policy issue."""

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

async def test_create_identity_psk_correct_behavior(wireless, mock_client):
    """Test create_identity_psk sends correct arguments."""
    mock_client.run_sync.return_value = {"id": "test_id"}

    # Case 1: group_policy_id is None
    await wireless.create_identity_psk(
        network_id="net1",
        number="0",
        name="test",
        group_policy_id=None,
        passphrase="pass",
    )

    args, kwargs = mock_client.run_sync.call_args
    # It should NOT contain groupPolicyId
    assert "groupPolicyId" not in kwargs, "groupPolicyId should not be sent when None"

    # Reset mock
    mock_client.run_sync.reset_mock()

    # Case 2: group_policy_id is "Normal" (string)
    await wireless.create_identity_psk(
        network_id="net1",
        number="0",
        name="test",
        group_policy_id="Normal",
        passphrase="pass",
    )

    args, kwargs = mock_client.run_sync.call_args
    # It should NOT contain groupPolicyId
    assert "groupPolicyId" not in kwargs, "groupPolicyId should not be sent when 'Normal'"

    # Reset mock
    mock_client.run_sync.reset_mock()

    # Case 3: group_policy_id is a valid ID "123"
    await wireless.create_identity_psk(
        network_id="net1",
        number="0",
        name="test",
        group_policy_id="123",
        passphrase="pass",
    )

    args, kwargs = mock_client.run_sync.call_args
    # It SHOULD contain groupPolicyId
    assert "groupPolicyId" in kwargs
    assert kwargs["groupPolicyId"] == "123"
