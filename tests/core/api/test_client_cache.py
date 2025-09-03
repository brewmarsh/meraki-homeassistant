"""Tests for the caching functionality of the Meraki API client."""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from tests.const import MOCK_DEVICE


@pytest.fixture
def mock_hass(tmp_path):
    """Fixture for a mocked Home Assistant object."""
    hass = MagicMock()
    hass.config.path.return_value = str(tmp_path)
    return hass


@pytest.mark.asyncio
async def test_caching_logic(mock_hass):
    """Test that the API client caches the results of get_all_data."""
    # Arrange
    api_client = MerakiAPIClient(
        hass=mock_hass,
        api_key="fake_key",
        org_id="fake_org",
    )
    api_client._cache.clear()

    # Mock the internal data fetching methods to track calls
    api_client._async_fetch_initial_data = AsyncMock(return_value=([], [], [], []))
    api_client._process_initial_data = MagicMock(
        return_value={"networks": [], "devices": [MOCK_DEVICE], "appliance_uplink_statuses": []}
    )
    api_client._async_fetch_client_data = AsyncMock(return_value=[])
    api_client._build_detail_tasks = MagicMock(return_value={})
    api_client._process_detailed_data = MagicMock(
        return_value={
            "ssids": [],
            "appliance_traffic": {},
            "vlans": {},
            "rf_profiles": {},
        }
    )

    # Act
    # Call get_all_data for the first time
    first_call_result = await api_client.get_all_data()

    # Call get_all_data for the second time
    second_call_result = await api_client.get_all_data()

    # Assert
    # The fetching logic should only have been called once
    api_client._async_fetch_initial_data.assert_called_once()
    api_client._process_initial_data.assert_called_once()
    api_client._async_fetch_client_data.assert_called_once()
    api_client._build_detail_tasks.assert_called_once()
    api_client._process_detailed_data.assert_called_once()

    # The results of both calls should be identical
    assert first_call_result == second_call_result

    # Let's also verify that the data is in the cache
    cache_key = f"meraki_data_{api_client.organization_id}"
    cached_item = api_client._cache.get(cache_key)
    assert cached_item is not None
    assert cached_item == first_call_result

    # Clear the cache and try again to ensure the fetch logic is called a second time
    api_client._cache.clear()
    third_call_result = await api_client.get_all_data()
    assert api_client._async_fetch_initial_data.call_count == 2
    assert third_call_result is not None


@pytest.mark.asyncio
async def test_partial_data_merging(mock_hass):
    """Test that if a detail task fails, data from the previous run is used."""
    # Arrange
    api_client = MerakiAPIClient(hass=mock_hass, api_key="fake_key", org_id="fake_org")
    api_client._cache.clear()  # Ensure no caching for this test

    # Mock initial data fetching
    mock_networks = [{"id": "N_1", "productTypes": ["wireless"]}]
    mock_devices = [{"serial": "D_1", "productType": "camera"}]
    api_client._async_fetch_initial_data = AsyncMock(return_value=([], [], [], []))
    api_client._process_initial_data = MagicMock(
        return_value={"networks": mock_networks, "devices": mock_devices, "appliance_uplink_statuses": []}
    )
    api_client._async_fetch_client_data = AsyncMock(return_value=[])

    # This represents the last successful run
    previous_data = {
        "ssids_N_1": [{"name": "Old SSID"}],
        "video_settings_D_1": {"setting": "old"},
    }

    # In the new run, the SSID fetch will fail, but video settings will succeed
    with patch("asyncio.gather", new=AsyncMock()) as mock_gather:
        mock_gather.return_value = [
            Exception("Failed to fetch SSIDs"),  # Corresponds to ssids_N_1
            None,  # Corresponds to rf_profiles_N_1
            {"setting": "new"},  # Corresponds to video_settings_D_1
            None,  # Corresponds to sense_settings_D_1
        ]

        # Act
        result = await api_client.get_all_data(previous_data=previous_data)

        # Assert
        # Check that the new, successful data is present
        assert result["devices"][0]["video_settings"]["setting"] == "new"
        # Check that the old, fallback data is present for the failed call
        assert result["ssids"][0]["name"] == "Old SSID"
