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
    with patch("diskcache.Cache") as MockCache:
        # Arrange
        mock_cache_instance = MockCache.return_value
        mock_cache_instance.get.return_value = None  # First call misses cache

        api_client = MerakiAPIClient(
            hass=mock_hass,
            api_key="fake_key",
            org_id="fake_org",
        )
        assert api_client._cache is mock_cache_instance

        # Mock the internal data fetching methods
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

        # Act: First call (cache miss)
        first_call_result = await api_client.get_all_data()

        # Assert: Check that data was fetched and cached
        api_client._async_fetch_initial_data.assert_called_once()
        mock_cache_instance.set.assert_called_once()

        # Prepare for second call (cache hit)
        mock_cache_instance.get.return_value = first_call_result

        # Act: Second call
        second_call_result = await api_client.get_all_data()

        # Assert: Check that fetch was not called again and cache was used
        api_client._async_fetch_initial_data.assert_called_once() # Still called only once
        assert mock_cache_instance.get.call_count == 2
        assert second_call_result == first_call_result


@pytest.mark.asyncio
async def test_partial_data_merging(mock_hass):
    """Test that if a detail task fails, data from the previous run is used."""
    # Arrange
    api_client = MerakiAPIClient(hass=mock_hass, api_key="fake_key", org_id="fake_org")
    api_client._cache.clear()  # Ensure no caching for this test

    # Mock initial data fetching
    mock_networks = [{"id": "N_1", "product_types": ["wireless"]}]
    mock_devices = [{"serial": "D_1", "product_type": "camera"}]
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

    # Let's mock _build_detail_tasks to return only the tasks we care about
    api_client._build_detail_tasks = MagicMock(
        return_value={
            f"ssids_{mock_networks[0]['id']}": "ssids_task",
            f"video_settings_{mock_devices[0]['serial']}": "video_task",
        }
    )

    # In the new run, the SSID fetch will fail, but video settings will succeed
    with patch("asyncio.gather", new=AsyncMock()) as mock_gather:
        mock_gather.return_value = [
            Exception("Failed to fetch SSIDs"),
            {"setting": "new"},
        ]

        # Act
        result = await api_client.get_all_data(previous_data=previous_data)

        # Assert
        # Check that the new, successful data is present
        assert result["devices"][0]["video_settings"]["setting"] == "new"
        # Check that the old, fallback data is present for the failed call
        assert result["ssids"][0]["name"] == "Old SSID"
