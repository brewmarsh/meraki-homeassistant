"""Tests for the caching functionality of the Meraki API client."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

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

    # Mock the internal data fetching methods to track calls
    api_client._async_fetch_initial_data = AsyncMock(return_value=([], [], [], []))
    api_client._process_initial_data = MagicMock(
        return_value={"networks": [], "devices": [MOCK_DEVICE]}
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
