"""Tests for the Wireless Endpoints."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.api.endpoints.wireless import WirelessEndpoints


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.dashboard = MagicMock()
    client.dashboard.wireless.createNetworkWirelessSsidIdentityPsk = AsyncMock()
    client.dashboard.wireless.deleteNetworkWirelessSsidIdentityPsk = AsyncMock()
    return client


@pytest.fixture
def wireless(mock_client):
    """Fixture for the WirelessEndpoints."""
    return WirelessEndpoints(mock_client)


async def test_create_identity_psk(wireless, mock_client):
    """Test create_identity_psk."""
    mock_client.dashboard.wireless.createNetworkWirelessSsidIdentityPsk = AsyncMock(
        return_value={"id": "test_id"}
    )

    result = await wireless.create_identity_psk(
        network_id="net1",
        number="0",
        name="test",
        group_policy_id="123",
        passphrase="pass",
    )

    assert result == {"id": "test_id"}
    mock_client.dashboard.wireless.createNetworkWirelessSsidIdentityPsk.assert_called_once_with(
        networkId="net1",
        number="0",
        name="test",
        groupPolicyId="123",
        passphrase="pass",
    )


async def test_create_identity_psk_no_group_policy(wireless, mock_client):
    """Test create_identity_psk without group policy."""
    mock_client.dashboard.wireless.createNetworkWirelessSsidIdentityPsk = AsyncMock(
        return_value={"id": "test_id"}
    )

    result = await wireless.create_identity_psk(
        network_id="net1",
        number="0",
        name="test",
        group_policy_id=None,
        passphrase="pass",
    )

    assert result == {"id": "test_id"}
    mock_client.dashboard.wireless.createNetworkWirelessSsidIdentityPsk.assert_called_once_with(
        networkId="net1",
        number="0",
        name="test",
        passphrase="pass",
    )


async def test_delete_identity_psk(wireless, mock_client):
    """Test delete_identity_psk."""
    mock_client.dashboard.wireless.deleteNetworkWirelessSsidIdentityPsk = AsyncMock(
        return_value=None
    )

    await wireless.delete_identity_psk(
        network_id="net1",
        number="0",
        identity_psk_id="psk1",
    )

    mock_client.dashboard.wireless.deleteNetworkWirelessSsidIdentityPsk.assert_called_once_with(
        networkId="net1", number="0", identityPskId="psk1"
    )
