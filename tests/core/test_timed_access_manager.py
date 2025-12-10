"""Tests for the TimedAccessManager."""

from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.util import dt as dt_util

from custom_components.meraki_ha.const import DATA_CLIENT, DOMAIN
from custom_components.meraki_ha.core.timed_access_manager import (
    TimedAccessKey,
    TimedAccessManager,
)


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client.wireless.create_identity_psk = AsyncMock()
    client.wireless.delete_identity_psk = AsyncMock()
    return client

@pytest.fixture
def manager(hass):
    """Fixture for the TimedAccessManager."""
    return TimedAccessManager(hass)

@pytest.fixture
def mock_store(manager):
    """Mock the storage."""
    with patch.object(manager, "_store") as mock:
        mock.async_load = AsyncMock(return_value=None)
        mock.async_save = AsyncMock()
        yield mock

async def test_load_keys(hass, manager, mock_store):
    """Test loading keys from storage."""
    now = dt_util.utcnow()
    expires_at = now + timedelta(hours=1)

    mock_data = [{
        "identity_psk_id": "psk1",
        "network_id": "net1",
        "ssid_number": "0",
        "name": "Test Key",
        "passphrase": "secret",
        "expires_at": expires_at.isoformat(),
        "config_entry_id": "entry1",
    }]
    mock_store.async_load.return_value = mock_data

    await manager.async_setup()

    assert len(manager._keys) == 1
    assert manager._keys[0].identity_psk_id == "psk1"
    # Should have scheduled removal
    assert "psk1" in manager._scheduled_removals

async def test_load_expired_keys(hass, manager, mock_store, mock_client):
    """Test loading keys that have expired."""
    now = dt_util.utcnow()
    expires_at = now - timedelta(hours=1)

    mock_data = [{
        "identity_psk_id": "psk1",
        "network_id": "net1",
        "ssid_number": "0",
        "name": "Test Key",
        "passphrase": "secret",
        "expires_at": expires_at.isoformat(),
        "config_entry_id": "entry1",
    }]
    mock_store.async_load.return_value = mock_data

    hass.data[DOMAIN] = {
        "entry1": {
            DATA_CLIENT: mock_client
        }
    }

    with patch.object(manager, "delete_key", new_callable=AsyncMock) as mock_delete:
        await manager.async_setup()
        await hass.async_block_till_done()

        # Should call delete_key immediately
        mock_delete.assert_called_once()
        args = mock_delete.call_args[0]
        assert args[0] == "psk1"

async def test_create_key(hass, manager, mock_store, mock_client):
    """Test creating a new key."""
    hass.data[DOMAIN] = {
        "entry1": {
            DATA_CLIENT: mock_client
        }
    }

    mock_client.wireless.create_identity_psk.return_value = {"id": "new_psk_id"}

    key = await manager.create_key(
        config_entry_id="entry1",
        network_id="net1",
        ssid_number="0",
        duration_minutes=60,
        name="Guest",
    )

    assert key.identity_psk_id == "new_psk_id"
    assert key.name == "Guest"
    assert len(manager._keys) == 1
    assert "new_psk_id" in manager._scheduled_removals

    mock_client.wireless.create_identity_psk.assert_called_once_with(
        "net1", "0", "Guest", None, key.passphrase
    )
    mock_store.async_save.assert_called_once()

async def test_delete_key(hass, manager, mock_store, mock_client):
    """Test deleting a key."""
    hass.data[DOMAIN] = {
        "entry1": {
            DATA_CLIENT: mock_client
        }
    }

    now = dt_util.utcnow()
    key = TimedAccessKey(
        identity_psk_id="psk1",
        network_id="net1",
        ssid_number="0",
        name="Test",
        passphrase="pass",
        expires_at=now.isoformat(),
        config_entry_id="entry1",
    )
    manager._keys.append(key)

    # Mock a timer
    manager._scheduled_removals["psk1"] = MagicMock()

    await manager.delete_key("psk1")

    assert len(manager._keys) == 0
    assert "psk1" not in manager._scheduled_removals
    mock_client.wireless.delete_identity_psk.assert_called_once_with(
        "net1", "0", "psk1"
    )
    mock_store.async_save.assert_called()
