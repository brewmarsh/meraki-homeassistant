"""Tests for the TimedAccessManager."""

from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.util import dt as dt_util

from custom_components.meraki_ha.core.timed_access_manager import TimedAccessManager


@pytest.fixture
def mock_api_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.wireless = MagicMock()
    client.wireless.create_network_wireless_ssid_identity_psk = AsyncMock(
        return_value={"id": "new_psk_id", "name": "Test Key"}
    )
    return client


@pytest.fixture
def manager(mock_api_client):
    """Fixture for the TimedAccessManager."""
    return TimedAccessManager(mock_api_client)


async def test_create_timed_access_key(manager, mock_api_client):
    """Test creating a new timed access key."""
    result = await manager.create_timed_access_key(
        network_id="net1",
        ssid_number="0",
        name="Guest Key",
        passphrase="secretpassword",
        duration_hours=24,
    )

    assert result["id"] == "new_psk_id"
    mock_api_client.wireless.create_network_wireless_ssid_identity_psk.assert_called_once()
    call_kwargs = (
        mock_api_client.wireless.create_network_wireless_ssid_identity_psk.call_args
    )
    assert call_kwargs.kwargs["network_id"] == "net1"
    assert call_kwargs.kwargs["number"] == "0"
    assert call_kwargs.kwargs["name"] == "Guest Key"
    assert call_kwargs.kwargs["passphrase"] == "secretpassword"
    assert call_kwargs.kwargs["group_policy_id"] == "Normal"
    assert "expiresAt" in call_kwargs.kwargs


async def test_create_timed_access_key_with_group_policy(manager, mock_api_client):
    """Test creating a timed access key with custom group policy."""
    result = await manager.create_timed_access_key(
        network_id="net1",
        ssid_number="1",
        name="VIP Key",
        passphrase="vippassword",
        duration_hours=48,
        group_policy_id="101",
    )

    call_kwargs = (
        mock_api_client.wireless.create_network_wireless_ssid_identity_psk.call_args
    )
    assert call_kwargs.kwargs["group_policy_id"] == "101"


async def test_create_timed_access_key_expiration_time(manager, mock_api_client):
    """Test that expiration time is calculated correctly."""
    with patch.object(dt_util, "utcnow") as mock_now:
        fixed_time = dt_util.parse_datetime("2025-01-05T12:00:00+00:00")
        mock_now.return_value = fixed_time

        await manager.create_timed_access_key(
            network_id="net1",
            ssid_number="0",
            name="Test Key",
            passphrase="password",
            duration_hours=2,
        )

        call_kwargs = (
            mock_api_client.wireless.create_network_wireless_ssid_identity_psk.call_args
        )
        # Should expire 2 hours from now
        expected_expiry = (fixed_time + timedelta(hours=2)).isoformat()
        assert call_kwargs.kwargs["expiresAt"] == expected_expiry
