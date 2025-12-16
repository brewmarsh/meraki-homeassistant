"""End-to-end integration tests for IPSK functionality."""

import logging
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.const import DATA_CLIENT, DOMAIN
from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.timed_access_manager import TimedAccessManager

_LOGGER = logging.getLogger(__name__)


@pytest.fixture
def mock_meraki_client(hass):
    """Create a mock Meraki API client."""
    client = MagicMock(spec=MerakiAPIClient)
    client.wireless = MagicMock()
    client.wireless.create_identity_psk = AsyncMock(
        return_value={"id": "mock_ipsk_id", "name": "Guest User"}
    )
    client.wireless.delete_identity_psk = AsyncMock()
    return client


@pytest.fixture
def mock_hass_config(hass, mock_meraki_client):
    """Set up hass data with mock client."""
    hass.data[DOMAIN] = {"test_entry_id": {DATA_CLIENT: mock_meraki_client}}
    return hass


@pytest.mark.asyncio
async def test_e2e_create_and_expire_ipsk(hass, mock_hass_config, mock_meraki_client):
    """
    Test the full lifecycle of an IPSK creation and expiration logic.

    This simulates the higher-level flow from the TimedAccessManager down to the API
    client, verifying that the correct parameters (including groupPolicyId) are passed.
    """
    manager = TimedAccessManager(hass)
    await manager.async_setup()

    # 1. Create a Key
    # Verify that calling create_key propagates to the client correctly
    key = await manager.create_key(
        config_entry_id="test_entry_id",
        network_id="N_12345",
        ssid_number="1",
        duration_minutes=60,
        name="Guest User",
        group_policy_id="101",
    )

    # Assertions on the returned key object
    assert key.identity_psk_id == "mock_ipsk_id"
    assert key.name == "Guest User"
    assert key.network_id == "N_12345"

    # Assert that the API client was called with the correct arguments
    # Crucially, we are checking that '101' was passed for group_policy_id
    mock_meraki_client.wireless.create_identity_psk.assert_called_once_with(
        "N_12345", "1", "Guest User", "101", key.passphrase
    )

    # 2. Verify deletion logic
    # We simulate deletion to ensure the ID is correctly passed down
    await manager.delete_key(key.identity_psk_id)

    mock_meraki_client.wireless.delete_identity_psk.assert_called_once_with(
        "N_12345", "1", "mock_ipsk_id"
    )


@pytest.fixture
def real_client_with_mock_dashboard(hass):
    """Create a MerakiAPIClient with a real WirelessEndpoints but mock Dashboard."""
    # We need to instantiate the real client
    client = MerakiAPIClient(hass, "key", "org")
    client.dashboard = MagicMock()

    # Mock the run_sync method to bypass the thread executor and just return the result
    # of the callable because we want to inspect the call to the dashboard method.
    async def mock_run_sync(func, *args, **kwargs):
        # We call the func directly, but since dashboard methods are usually sync in the
        # library, we can just return a mock response.
        return {"id": "mock_ipsk_id", "name": "Guest User"}

    client.run_sync = AsyncMock(side_effect=mock_run_sync)

    return client


@pytest.mark.asyncio
async def test_e2e_ipsk_flow_real_endpoints(hass, real_client_with_mock_dashboard):
    """True integration test using real WirelessEndpoints logic."""
    # Setup Hass data
    hass.data[DOMAIN] = {
        "test_entry_id": {DATA_CLIENT: real_client_with_mock_dashboard}
    }

    manager = TimedAccessManager(hass)
    await manager.async_setup()

    # 1. Create Key with NO Group Policy
    await manager.create_key(
        config_entry_id="test_entry_id",
        network_id="N_12345",
        ssid_number="1",
        duration_minutes=60,
        name="Guest Default",
    )

    # Now verify the call to the dashboard.wireless method
    # This proves that WirelessEndpoints.create_identity_psk correctly omitted
    # groupPolicyId instead of sending "Normal"
    real_client_with_mock_dashboard.run_sync.assert_called()

    # Get the arguments passed to run_sync.
    # args[0] is the function
    # (dashboard.wireless.createNetworkWirelessSsidIdentityPsk)
    # kwargs should contain the API parameters
    call_args = real_client_with_mock_dashboard.run_sync.call_args

    wireless = real_client_with_mock_dashboard.dashboard.wireless
    expected_func = wireless.createNetworkWirelessSsidIdentityPsk
    assert call_args[0][0] == expected_func

    # Check the keyword arguments passed to run_sync
    kwargs = call_args[1]
    assert kwargs["networkId"] == "N_12345"
    assert kwargs["number"] == "1"
    # CRITICAL: Confirm that 'groupPolicyId' is NOT present, as per our fix
    assert "groupPolicyId" not in kwargs

    # 2. Create Key WITH Group Policy
    await manager.create_key(
        config_entry_id="test_entry_id",
        network_id="N_12345",
        ssid_number="1",
        duration_minutes=60,
        name="Guest Policy",
        group_policy_id="999",
    )

    call_args = real_client_with_mock_dashboard.run_sync.call_args
    kwargs = call_args[1]
    assert kwargs["groupPolicyId"] == "999"
