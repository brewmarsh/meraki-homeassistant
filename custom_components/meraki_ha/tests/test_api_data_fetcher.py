"""Tests for the Meraki API Data Fetcher."""

import pytest
from unittest.mock import AsyncMock, MagicMock
import logging # For caplog

from meraki.exceptions import APIError as MerakiSDKAPIError

# Assuming MerakiAPIClient and MerakiApiDataFetcher are importable
# Adjust paths as necessary if your project structure differs
from custom_components.meraki_ha.meraki_api import MerakiAPIClient
from custom_components.meraki_ha.coordinators.api_data_fetcher import MerakiApiDataFetcher

# --- Mock Data ---
MOCK_ORG_DEVICES = [
    {"serial": "Q2AB-CDEF-0001", "name": "Device 1", "model": "MR33", "networkId": "N_123"},
    {"serial": "Q2AB-CDEF-0002", "name": "Device 2", "model": "MS220-8P", "networkId": "N_124"},
]

MOCK_NETWORKS = [
    {"id": "N_123", "name": "Network 1", "organizationId": "test_org_id"},
    {"id": "N_124", "name": "Network 2", "organizationId": "test_org_id"},
]

MOCK_SSIDS_NET1 = [
    {"number": 0, "name": "SSID_Net1_1", "enabled": True},
    {"number": 1, "name": "SSID_Net1_2", "enabled": False},
]

MOCK_SSIDS_NET2 = [
    {"number": 0, "name": "SSID_Net2_1", "enabled": True},
]

MOCK_CLIENTS_NET1 = [
    {"mac": "AA:BB:CC:00:01:01", "description": "Client A Net 1", "ip": "192.168.1.11"},
]

MOCK_CLIENTS_NET2 = [
    {"mac": "AA:BB:CC:00:02:01", "description": "Client B Net 2", "ip": "192.168.2.21"},
]

# --- Fixtures ---

@pytest.fixture
def mock_meraki_client():
    """Mock the MerakiAPIClient."""
    client = MagicMock(spec=MerakiAPIClient)
    client.org_id = "test_org_id"
    
    # Mock the specific controllers and their methods
    client.organizations = AsyncMock()
    client.devices = AsyncMock()
    client.networks = AsyncMock()
    client.wireless = AsyncMock()
    # Add 'clients' controller for client fetching tests
    client.clients = AsyncMock() 
    return client

@pytest.fixture
def data_fetcher(mock_meraki_client: MagicMock) -> MerakiApiDataFetcher:
    """Fixture to create an instance of MerakiApiDataFetcher with a mocked client."""
    return MerakiApiDataFetcher(meraki_client=mock_meraki_client)

# --- Tests for async_get_organization_devices ---

async def test_async_get_organization_devices_success(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock
):
    """Test successful fetching of organization devices."""
    mock_meraki_client.organizations.getOrganizationDevices = AsyncMock(
        return_value=MOCK_ORG_DEVICES
    )
    
    result = await data_fetcher.async_get_organization_devices(org_id="test_org_id")
    
    mock_meraki_client.organizations.getOrganizationDevices.assert_called_once_with(
        "test_org_id"
    )
    assert result == MOCK_ORG_DEVICES

async def test_async_get_organization_devices_api_error(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog
):
    """Test API error when fetching organization devices."""
    mock_meraki_client.organizations.getOrganizationDevices = AsyncMock(
        side_effect=MerakiSDKAPIError(MagicMock(status=500, reason="Server Error"), "test API error")
    )
    
    with caplog.at_level(logging.WARNING):
        result = await data_fetcher.async_get_organization_devices(org_id="test_org_id")
    
    assert result is None
    assert "SDK API error fetching devices for org test_org_id" in caplog.text
    assert "Status 500, Reason: Server Error" in caplog.text

async def test_async_get_organization_devices_unexpected_exception(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog
):
    """Test unexpected exception when fetching organization devices."""
    mock_meraki_client.organizations.getOrganizationDevices = AsyncMock(
        side_effect=Exception("Something broke badly")
    )
    
    with caplog.at_level(logging.ERROR): # Changed to ERROR based on typical logging for unexpected
        result = await data_fetcher.async_get_organization_devices(org_id="test_org_id")
    
    assert result is None
    assert "Unexpected error fetching devices for org test_org_id" in caplog.text
    assert "Something broke badly" in caplog.text


# --- Tests for async_get_networks ---

async def test_async_get_networks_success(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock
):
    """Test successful fetching of networks."""
    mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(
        return_value=MOCK_NETWORKS
    )
    
    result = await data_fetcher.async_get_networks(org_id="test_org_id")
    
    mock_meraki_client.organizations.getOrganizationNetworks.assert_called_once_with(
        organizationId="test_org_id"
    )
    assert result == MOCK_NETWORKS

async def test_async_get_networks_api_error(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog
):
    """Test API error when fetching networks."""
    mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(
        side_effect=MerakiSDKAPIError(MagicMock(status=403, reason="Forbidden"), "test network API error")
    )
    
    with caplog.at_level(logging.WARNING):
        result = await data_fetcher.async_get_networks(org_id="test_org_id")
        
    assert result is None
    assert "SDK API error during getNetworks" in caplog.text # Message from async_get_networks
    assert "Status 403, Reason: Forbidden" in caplog.text

async def test_async_get_networks_returns_none(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog
):
    """Test when getOrganizationNetworks returns None."""
    mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(return_value=None)
    
    with caplog.at_level(logging.WARNING):
        result = await data_fetcher.async_get_networks(org_id="test_org_id")
        
    assert result is None
    assert "Call to organizations.getOrganizationNetworks for org ID test_org_id returned None." in caplog.text

async def test_async_get_networks_returns_empty_list(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog
):
    """Test when getOrganizationNetworks returns an empty list (treated as no networks found)."""
    mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(return_value=[])
    
    with caplog.at_level(logging.WARNING):
        result = await data_fetcher.async_get_networks(org_id="test_org_id")
        
    assert result is None # Current implementation returns None for empty list
    assert "No networks found for organization ID test_org_id" in caplog.text


# --- Tests for async_get_network_ssids ---

async def test_async_get_network_ssids_success(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock
):
    """Test successful fetching of SSIDs for a network."""
    mock_meraki_client.wireless.get_network_wireless_ssids = AsyncMock(
        return_value=MOCK_SSIDS_NET1
    )
    
    result = await data_fetcher.async_get_network_ssids(network_id="N_123")
    
    mock_meraki_client.wireless.get_network_wireless_ssids.assert_called_once_with(
        network_id="N_123"
    )
    assert result == MOCK_SSIDS_NET1

async def test_async_get_network_ssids_api_error_404(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog
):
    """Test API error 404 (No SSIDs/Wireless) when fetching SSIDs."""
    mock_meraki_client.wireless.get_network_wireless_ssids = AsyncMock(
        side_effect=MerakiSDKAPIError(MagicMock(status=404, reason="Not found"), "SSID not found")
    )
    
    with caplog.at_level(logging.INFO): # 404 is logged as INFO
        result = await data_fetcher.async_get_network_ssids(network_id="N_NONEXIST")
        
    assert result == [] # Should return an empty list for 404
    assert "SSID resource not found for network N_NONEXIST" in caplog.text

async def test_async_get_network_ssids_api_error_other(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog
):
    """Test other API errors when fetching SSIDs."""
    mock_meraki_client.wireless.get_network_wireless_ssids = AsyncMock(
        side_effect=MerakiSDKAPIError(MagicMock(status=500, reason="Server Error"), "SSID fetch error")
    )
    
    with caplog.at_level(logging.WARNING):
        result = await data_fetcher.async_get_network_ssids(network_id="N_123")
        
    assert result is None
    assert "SDK API error fetching SSIDs for network N_123" in caplog.text
    assert "Status 500, Reason: Server Error" in caplog.text

# --- Tests for _async_get_mr_device_details (helper for fetch_all_data) ---

async def test_async_get_mr_device_details_success(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock
):
    """Test successful fetching of MR device details (clients and radio settings)."""
    device_dict = {"serial": "MR_SERIAL", "name": "Test MR"}
    mock_clients_data = [{"mac": "client1"}, {"mac": "client2"}]
    mock_radio_data = {"band": "2.4 GHz", "channel": 6}

    mock_meraki_client.devices.get_device_clients = AsyncMock(return_value=mock_clients_data)
    mock_meraki_client.wireless.get_device_wireless_radio_settings = AsyncMock(return_value=mock_radio_data)

    await data_fetcher._async_get_mr_device_details(device_dict, "MR_SERIAL")

    mock_meraki_client.devices.get_device_clients.assert_called_once_with(serial="MR_SERIAL")
    mock_meraki_client.wireless.get_device_wireless_radio_settings.assert_called_once_with(serial="MR_SERIAL")
    
    assert device_dict["connected_clients_count"] == 2
    assert device_dict["radio_settings"] == mock_radio_data

async def test_async_get_mr_device_details_clients_api_error(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog
):
    """Test API error when fetching clients for MR device details."""
    device_dict = {"serial": "MR_SERIAL", "name": "Test MR"}
    mock_radio_data = {"band": "5 GHz"}

    mock_meraki_client.devices.get_device_clients = AsyncMock(
        side_effect=MerakiSDKAPIError(MagicMock(status=500), "Client fetch error")
    )
    mock_meraki_client.wireless.get_device_wireless_radio_settings = AsyncMock(return_value=mock_radio_data)

    with caplog.at_level(logging.WARNING):
        await data_fetcher._async_get_mr_device_details(device_dict, "MR_SERIAL")

    assert "Failed to fetch client count for MR device Test MR" in caplog.text
    assert device_dict["connected_clients_count"] == 0 # Default value
    assert device_dict["radio_settings"] == mock_radio_data # Radio settings should still be fetched

async def test_async_get_mr_device_details_radio_api_error(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog
):
    """Test API error when fetching radio settings for MR device details."""
    device_dict = {"serial": "MR_SERIAL", "name": "Test MR"}
    mock_clients_data = [{"mac": "client1"}]

    mock_meraki_client.devices.get_device_clients = AsyncMock(return_value=mock_clients_data)
    mock_meraki_client.wireless.get_device_wireless_radio_settings = AsyncMock(
        side_effect=MerakiSDKAPIError(MagicMock(status=500), "Radio fetch error")
    )
    
    with caplog.at_level(logging.WARNING):
        await data_fetcher._async_get_mr_device_details(device_dict, "MR_SERIAL")

    assert "Failed to fetch radio settings for MR device Test MR" in caplog.text
    assert device_dict["connected_clients_count"] == 1 # Client count should be fetched
    assert device_dict["radio_settings"] is None # Default value

# --- Tests for fetch_all_data (Main Orchestration Method) ---

async def test_fetch_all_data_success(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, hass_mock # Add hass_mock if needed by fetch_all_data
):
    """Test successful fetching of all data types."""
    # Setup mocks for all underlying fetch methods
    mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(return_value=MOCK_NETWORKS)
    mock_meraki_client.organizations.getOrganizationDevices = AsyncMock(return_value=MOCK_ORG_DEVICES)
    
    # Mock SSIDs for each network
    def mock_get_ssids(network_id):
        if network_id == "N_123":
            return AsyncMock(return_value=MOCK_SSIDS_NET1)()
        elif network_id == "N_124":
            return AsyncMock(return_value=MOCK_SSIDS_NET2)()
        return AsyncMock(return_value=[])() # Default empty for other networks
    mock_meraki_client.wireless.get_network_wireless_ssids = MagicMock(side_effect=mock_get_ssids)

    # Mock clients for each network
    def mock_get_clients(network_id, timespan): # Add timespan
        if network_id == "N_123":
            return AsyncMock(return_value=MOCK_CLIENTS_NET1)()
        elif network_id == "N_124":
            return AsyncMock(return_value=MOCK_CLIENTS_NET2)()
        return AsyncMock(return_value=[])()
    # Ensure the path matches the one used in fetch_all_data:
    # It was self.meraki_client.networks.get_network_clients
    mock_meraki_client.networks.get_network_clients = MagicMock(side_effect=mock_get_clients)


    # Mock MR device details (client count and radio settings)
    # For simplicity, assume one MR device from MOCK_ORG_DEVICES
    mr_device_serial = "Q2AB-CDEF-0001" # Assuming this is an MR device
    mock_meraki_client.devices.get_device_clients = AsyncMock(return_value=[{"mac": "client_mr"}])
    mock_meraki_client.wireless.get_device_wireless_radio_settings = AsyncMock(return_value={"band": "2.4GHz"})

    hass_mock_instance = MagicMock() # Mock HomeAssistant instance if needed by the method

    all_data = await data_fetcher.fetch_all_data(hass=hass_mock_instance)

    assert all_data["networks"] == MOCK_NETWORKS
    assert all_data["devices"] == MOCK_ORG_DEVICES # MR device details are added in-place
    assert len(all_data["ssids"]) == len(MOCK_SSIDS_NET1) + len(MOCK_SSIDS_NET2)
    assert len(all_data["clients"]) == len(MOCK_CLIENTS_NET1) + len(MOCK_CLIENTS_NET2)
    
    # Verify MR device details were fetched for the MR device
    # Find the MR device in the results and check
    updated_mr_device = next(d for d in all_data["devices"] if d["serial"] == mr_device_serial)
    assert updated_mr_device["connected_clients_count"] == 1
    assert updated_mr_device["radio_settings"] == {"band": "2.4GHz"}

async def test_fetch_all_data_networks_fail(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog, hass_mock
):
    """Test fetch_all_data when fetching networks fails."""
    mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(return_value=None) # Simulate failure
    hass_mock_instance = MagicMock()

    with pytest.raises(UpdateFailed) as excinfo:
        await data_fetcher.fetch_all_data(hass=hass_mock_instance)
    
    assert "Could not fetch Meraki networks for org test_org_id" in str(excinfo.value)
    assert "Could not fetch Meraki networks for org ID: test_org_id. Aborting update." in caplog.text

async def test_fetch_all_data_devices_fail(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog, hass_mock
):
    """Test fetch_all_data when fetching devices fails."""
    mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(return_value=MOCK_NETWORKS) # Networks succeed
    mock_meraki_client.organizations.getOrganizationDevices = AsyncMock(return_value=None) # Devices fail
    hass_mock_instance = MagicMock()

    with pytest.raises(UpdateFailed) as excinfo:
        await data_fetcher.fetch_all_data(hass=hass_mock_instance)
        
    assert "Could not fetch Meraki devices for org test_org_id" in str(excinfo.value)
    assert "Could not fetch Meraki devices for org ID: test_org_id. Aborting update." in caplog.text

async def test_fetch_all_data_ssids_fail_for_one_network(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog, hass_mock
):
    """Test fetch_all_data when fetching SSIDs fails for one network but continues for others."""
    mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(return_value=MOCK_NETWORKS)
    mock_meraki_client.organizations.getOrganizationDevices = AsyncMock(return_value=MOCK_ORG_DEVICES)
    mock_meraki_client.networks.get_network_clients = AsyncMock(return_value=[]) # No clients for simplicity here

    # SSIDs for N_123 fail, N_124 succeed
    def mock_get_ssids_partial_fail(network_id):
        if network_id == "N_123":
            # Simulate an API error that results in async_get_network_ssids returning None
            raise MerakiSDKAPIError(MagicMock(status=500), "SSID Error N_123") 
        elif network_id == "N_124":
            return AsyncMock(return_value=MOCK_SSIDS_NET2)()
        return AsyncMock(return_value=[])()
    mock_meraki_client.wireless.get_network_wireless_ssids = MagicMock(side_effect=mock_get_ssids_partial_fail)
    
    hass_mock_instance = MagicMock()
    
    with caplog.at_level(logging.WARNING): # Expect warnings for the failed SSID fetch
        all_data = await data_fetcher.fetch_all_data(hass=hass_mock_instance)

    assert "Error fetching SSIDs for network N_123 was not handled by async_get_network_ssids" in caplog.text
    assert "Status: 500, Reason: None. Skipping." in caplog.text # Reason might be None if not set in mock
    assert len(all_data["ssids"]) == len(MOCK_SSIDS_NET2) # Only SSIDs from N_124
    assert all_data["networks"] is not None # Other data should be present
    assert all_data["devices"] is not None

async def test_fetch_all_data_clients_fail_for_one_network(
    data_fetcher: MerakiApiDataFetcher, mock_meraki_client: MagicMock, caplog, hass_mock
):
    """Test fetch_all_data when fetching clients fails for one network."""
    mock_meraki_client.organizations.getOrganizationNetworks = AsyncMock(return_value=MOCK_NETWORKS)
    mock_meraki_client.organizations.getOrganizationDevices = AsyncMock(return_value=MOCK_ORG_DEVICES)
    mock_meraki_client.wireless.get_network_wireless_ssids = AsyncMock(return_value=[]) # No SSIDs

    def mock_get_clients_partial_fail(network_id, timespan):
        if network_id == "N_123":
            raise MerakiSDKAPIError(MagicMock(status=500), "Client Error N_123")
        elif network_id == "N_124":
            return AsyncMock(return_value=MOCK_CLIENTS_NET2)()
        return AsyncMock(return_value=[])()
    mock_meraki_client.networks.get_network_clients = MagicMock(side_effect=mock_get_clients_partial_fail)

    hass_mock_instance = MagicMock()

    with caplog.at_level(logging.WARNING):
        all_data = await data_fetcher.fetch_all_data(hass=hass_mock_instance)

    assert "Meraki SDK API error fetching clients for network N_123" in caplog.text
    assert len(all_data["clients"]) == len(MOCK_CLIENTS_NET2) # Only clients from N_124


# Pytest needs a hass_mock fixture if used by any tests.
# If HomeAssistant instance is not actually used by fetch_all_data, this can be simplified.
@pytest.fixture
def hass_mock():
    """Mock the HomeAssistant object."""
    return MagicMock()

from homeassistant.helpers.update_coordinator import UpdateFailed # Ensure this is imported
```
