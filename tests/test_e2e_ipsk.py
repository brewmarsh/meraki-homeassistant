"""End-to-end integration tests for IPSK functionality."""

import logging
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.const.integration import DATA_CLIENT, DOMAIN
from custom_components.meraki_ha.core.api import (
    MerakiApiClientProtocol,
)
from custom_components.meraki_ha.services.ipsk_manager import IPSKManager

_LOGGER = logging.getLogger(__name__)


@pytest.fixture
def mock_meraki_client(hass):
    """Create a mock Meraki API client."""
    client = MagicMock(spec=MerakiApiClientProtocol)
    client._disabled_features = set()
    client.wireless = MagicMock()
    client.wireless.create_identity_psk = AsyncMock(
        return_value={
            "id": "mock_ipsk_id",
            "name": "Guest User",
            "passphrase": "secretpassphrase",
        }
    )
    client.wireless.delete_identity_psk = AsyncMock()
    return client


@pytest.fixture
def mock_hass_config(hass, mock_meraki_client):
    """Set up hass data with mock client."""
    hass.data[DOMAIN] = {"test_entry_id": {DATA_CLIENT: mock_meraki_client}}
    return hass


@pytest.fixture
def manager(hass):
    """Fixture for IPSKManager with cleanup."""
    mgr = IPSKManager(hass)
    yield mgr
    mgr.async_unload()


@pytest.mark.asyncio
async def test_e2e_create_and_expire_ipsk(
    hass, mock_hass_config, mock_meraki_client, manager
):
    """
    Test the full lifecycle of an IPSK creation and expiration logic.

    This simulates the higher-level flow from the IPSKManager down to the API
    client, verifying that the correct parameters (including groupPolicyId) are passed.
    """
    await manager.async_setup()
    try:
        # 1. Create a Key
        # Verify that calling create_guest_key propagates to the client correctly
        key = await manager.create_guest_key(
            config_entry_id="test_entry_id",
            network_id="N_12345",
            ssid_number="1",
            duration_minutes=60,
            name="Guest User",
            group_policy_id="101",
        )

        # Assertions on the returned key object
        assert key["identity_psk_id"] == "mock_ipsk_id"
        assert key["name"] == "Guest User"
        assert key["network_id"] == "N_12345"
        assert key["passphrase"] == "secretpassphrase"

        # Assert that the API client was called with the correct arguments
        mock_meraki_client.wireless.create_identity_psk.assert_called_once_with(
            "N_12345", "1", "Guest User", "101", None
        )

        # 2. Verify deletion logic
        await manager.remove_guest_key(key["identity_psk_id"])

        mock_meraki_client.wireless.delete_identity_psk.assert_called_once_with(
            "N_12345", "1", "mock_ipsk_id"
        )
    finally:
        manager.async_unload()


@pytest.mark.asyncio
async def test_e2e_ipsk_flow_real_endpoints(hass, mock_meraki_client, manager):
    """Simplified integration test verifying parameter passing."""
    # Setup Hass data
    hass.data[DOMAIN] = {"test_entry_id": {DATA_CLIENT: mock_meraki_client}}

    await manager.async_setup()
    try:
        # 1. Create Key with NO Group Policy
        await manager.create_guest_key(
            config_entry_id="test_entry_id",
            network_id="N_12345",
            ssid_number="1",
            duration_minutes=60,
            name="Guest Default",
        )

        mock_meraki_client.wireless.create_identity_psk.assert_called_with(
            "N_12345", "1", "Guest Default", None, None
        )

        # 2. Create Key WITH Group Policy
        await manager.create_guest_key(
            config_entry_id="test_entry_id",
            network_id="N_12345",
            ssid_number="1",
            duration_minutes=60,
            name="Guest Policy",
            group_policy_id="999",
        )

        mock_meraki_client.wireless.create_identity_psk.assert_called_with(
            "N_12345", "1", "Guest Policy", "999", None
        )
    finally:
        manager.async_unload()
