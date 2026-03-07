"""Tests for IPSK Manager."""

from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.util import dt as dt_util

from custom_components.meraki_ha.const.api import DATA_CLIENT
from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.services.ipsk_manager import IPSKManager


@pytest.fixture
def mock_meraki_client(hass):
    """Create a mock Meraki API client."""
    client = MagicMock()
    client.wireless = MagicMock()
    client.wireless.create_identity_psk = AsyncMock(
        return_value={"id": "mock_ipsk_id", "name": "Guest User"}
    )
    client.wireless.delete_identity_psk = AsyncMock()

    hass.data[DOMAIN] = {"test_entry_id": {DATA_CLIENT: client}}
    return client


@pytest.fixture
def manager(hass):
    """Fixture for IPSKManager."""
    mgr = IPSKManager(hass)
    return mgr


@pytest.mark.asyncio
async def test_create_guest_key(hass, mock_meraki_client, manager):
    """Test creating a guest key."""
    await manager.async_setup()

    key = await manager.create_guest_key(
        config_entry_id="test_entry_id",
        network_id="N_12345",
        ssid_number="1",
        duration_minutes=60,
        name="Guest User",
    )

    assert key["identity_psk_id"] == "mock_ipsk_id"
    assert key["name"] == "Guest User"
    assert len(manager.active_keys) == 1

    mock_meraki_client.wireless.create_identity_psk.assert_called_once()
    manager.async_unload()


@pytest.mark.asyncio
async def test_remove_guest_key(hass, mock_meraki_client, manager):
    """Test removing a guest key."""
    await manager.async_setup()

    # Manually add a key to track
    key = {
        "identity_psk_id": "mock_ipsk_id",
        "network_id": "N_12345",
        "ssid_number": "1",
        "name": "Guest User",
        "expires_at": (dt_util.utcnow() + timedelta(hours=1)).isoformat(),
        "config_entry_id": "test_entry_id",
    }
    manager.active_keys.append(key)

    await manager.remove_guest_key("mock_ipsk_id")

    assert len(manager.active_keys) == 0
    mock_meraki_client.wireless.delete_identity_psk.assert_called_once_with(
        "N_12345", "1", "mock_ipsk_id"
    )
    manager.async_unload()


@pytest.mark.asyncio
async def test_remove_guest_key_failure_keeps_tracking(
    hass, mock_meraki_client, manager
):
    """Test that transient failure keeps the key in tracking."""
    await manager.async_setup()

    mock_meraki_client.wireless.delete_identity_psk.side_effect = Exception(
        "Transient Error"
    )

    # Manually add a key to track
    key = {
        "identity_psk_id": "mock_ipsk_id",
        "network_id": "N_12345",
        "ssid_number": "1",
        "name": "Guest User",
        "expires_at": (dt_util.utcnow() + timedelta(hours=1)).isoformat(),
        "config_entry_id": "test_entry_id",
    }
    manager.active_keys.append(key)

    result = await manager.remove_guest_key("mock_ipsk_id")

    assert result is False
    assert len(manager.active_keys) == 1
    manager.async_unload()


@pytest.mark.asyncio
async def test_remove_guest_key_404_removes_from_tracking(
    hass, mock_meraki_client, manager
):
    """Test that 404 error removes the key from tracking."""
    await manager.async_setup()

    mock_meraki_client.wireless.delete_identity_psk.side_effect = Exception(
        "404 Not Found"
    )

    # Manually add a key to track
    key = {
        "identity_psk_id": "mock_ipsk_id",
        "network_id": "N_12345",
        "ssid_number": "1",
        "name": "Guest User",
        "expires_at": (dt_util.utcnow() + timedelta(hours=1)).isoformat(),
        "config_entry_id": "test_entry_id",
    }
    manager.active_keys.append(key)

    result = await manager.remove_guest_key("mock_ipsk_id")

    assert result is True
    assert len(manager.active_keys) == 0
    manager.async_unload()


@pytest.mark.asyncio
async def test_reap_expired_keys(hass, mock_meraki_client, manager):
    """Test reaping expired keys."""
    await manager.async_setup()

    # Add one expired and one active key
    expired_key = {
        "identity_psk_id": "expired_id",
        "network_id": "N_12345",
        "ssid_number": "1",
        "name": "Expired Guest",
        "expires_at": (dt_util.utcnow() - timedelta(minutes=1)).isoformat(),
        "config_entry_id": "test_entry_id",
    }
    active_key = {
        "identity_psk_id": "active_id",
        "network_id": "N_12345",
        "ssid_number": "1",
        "name": "Active Guest",
        "expires_at": (dt_util.utcnow() + timedelta(minutes=60)).isoformat(),
        "config_entry_id": "test_entry_id",
    }
    manager.active_keys.extend([expired_key, active_key])

    await manager.async_check_expirations()

    assert len(manager.active_keys) == 1
    assert manager.active_keys[0]["identity_psk_id"] == "active_id"
    mock_meraki_client.wireless.delete_identity_psk.assert_called_once_with(
        "N_12345", "1", "expired_id"
    )
    manager.async_unload()
