"""Tests for MerakiContentFilteringSelect."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.exceptions import HomeAssistantError

from custom_components.meraki_ha.select.meraki_content_filtering import (
    MerakiContentFilteringSelect,
)
from tests.const import MOCK_NETWORK

# Cast MOCK_NETWORK to dict[str, Any] for the tests
_MOCK_NETWORK_DATA: dict[str, Any] = dict(MOCK_NETWORK)


@pytest.fixture
def mock_content_filtering_coordinator(mock_coordinator: MagicMock) -> MagicMock:
    """Create a mock coordinator with content filtering data."""
    mock_coordinator.data = {
        "content_filtering": {
            MOCK_NETWORK["id"]: {
                "urlCategoryListSize": "topSites",
                "blockedUrlCategories": [],
            }
        }
    }
    mock_coordinator.async_request_refresh = AsyncMock()
    return mock_coordinator


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Create a mock Meraki API client."""
    client = MagicMock()
    client.appliance = MagicMock()
    client.appliance.update_network_appliance_content_filtering = AsyncMock()
    return client


def test_content_filtering_initialization(
    mock_content_filtering_coordinator: MagicMock,
    mock_meraki_client: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test content filtering select initialization."""
    select = MerakiContentFilteringSelect(
        coordinator=mock_content_filtering_coordinator,
        meraki_client=mock_meraki_client,
        config_entry=mock_config_entry,
        network_data=_MOCK_NETWORK_DATA,
    )

    assert select._network_id == MOCK_NETWORK["id"]
    assert select.entity_description.name == "Content Filtering Policy"
    assert select.entity_description.icon == "mdi:web-filter"


def test_content_filtering_current_option(
    mock_content_filtering_coordinator: MagicMock,
    mock_meraki_client: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test content filtering current option."""
    select = MerakiContentFilteringSelect(
        coordinator=mock_content_filtering_coordinator,
        meraki_client=mock_meraki_client,
        config_entry=mock_config_entry,
        network_data=_MOCK_NETWORK_DATA,
    )

    assert select._attr_current_option == "topSites"
    assert "topSites" in select._attr_options
    assert "fullList" in select._attr_options


def test_content_filtering_no_data(
    mock_content_filtering_coordinator: MagicMock,
    mock_meraki_client: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test content filtering with no data."""
    mock_content_filtering_coordinator.data = {}

    select = MerakiContentFilteringSelect(
        coordinator=mock_content_filtering_coordinator,
        meraki_client=mock_meraki_client,
        config_entry=mock_config_entry,
        network_data=_MOCK_NETWORK_DATA,
    )

    assert select._attr_current_option is None
    assert select._attr_options == []


@pytest.mark.asyncio
async def test_content_filtering_select_option(
    mock_content_filtering_coordinator: MagicMock,
    mock_meraki_client: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test selecting a content filtering option."""
    select = MerakiContentFilteringSelect(
        coordinator=mock_content_filtering_coordinator,
        meraki_client=mock_meraki_client,
        config_entry=mock_config_entry,
        network_data=_MOCK_NETWORK_DATA,
    )

    # Mock async_write_ha_state
    object.__setattr__(select, "async_write_ha_state", MagicMock())

    await select.async_select_option("fullList")

    assert select._attr_current_option == "fullList"
    mock_meraki_client.appliance.update_network_appliance_content_filtering.assert_called_once_with(
        networkId=MOCK_NETWORK["id"],
        urlCategoryListSize="fullList",
    )
    mock_content_filtering_coordinator.async_request_refresh.assert_called()


@pytest.mark.asyncio
async def test_content_filtering_select_option_error(
    mock_content_filtering_coordinator: MagicMock,
    mock_meraki_client: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test error handling when selecting option fails."""
    appliance = mock_meraki_client.appliance
    appliance.update_network_appliance_content_filtering.side_effect = Exception(
        "API Error"
    )

    select = MerakiContentFilteringSelect(
        coordinator=mock_content_filtering_coordinator,
        meraki_client=mock_meraki_client,
        config_entry=mock_config_entry,
        network_data=_MOCK_NETWORK_DATA,
    )

    with pytest.raises(
        HomeAssistantError, match="Failed to set content filtering policy"
    ):
        await select.async_select_option("fullList")


def test_content_filtering_unique_id(
    mock_content_filtering_coordinator: MagicMock,
    mock_meraki_client: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test content filtering unique ID format."""
    select = MerakiContentFilteringSelect(
        coordinator=mock_content_filtering_coordinator,
        meraki_client=mock_meraki_client,
        config_entry=mock_config_entry,
        network_data=_MOCK_NETWORK_DATA,
    )

    assert (
        select._attr_unique_id
        == f"meraki-network-{MOCK_NETWORK['id']}-content-filtering"
    )


def test_content_filtering_available(
    mock_content_filtering_coordinator: MagicMock,
    mock_meraki_client: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test content filtering availability."""
    mock_content_filtering_coordinator.last_update_success = True

    select = MerakiContentFilteringSelect(
        coordinator=mock_content_filtering_coordinator,
        meraki_client=mock_meraki_client,
        config_entry=mock_config_entry,
        network_data=_MOCK_NETWORK_DATA,
    )

    assert select.available is True


def test_content_filtering_unavailable_no_data(
    mock_content_filtering_coordinator: MagicMock,
    mock_meraki_client: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test content filtering unavailable when no data."""
    mock_content_filtering_coordinator.data = None
    mock_content_filtering_coordinator.last_update_success = True

    select = MerakiContentFilteringSelect(
        coordinator=mock_content_filtering_coordinator,
        meraki_client=mock_meraki_client,
        config_entry=mock_config_entry,
        network_data=_MOCK_NETWORK_DATA,
    )

    assert select.available is False


def test_content_filtering_coordinator_update(
    mock_content_filtering_coordinator: MagicMock,
    mock_meraki_client: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test content filtering handles coordinator updates."""
    select = MerakiContentFilteringSelect(
        coordinator=mock_content_filtering_coordinator,
        meraki_client=mock_meraki_client,
        config_entry=mock_config_entry,
        network_data=_MOCK_NETWORK_DATA,
    )

    # Mock async_write_ha_state
    object.__setattr__(select, "async_write_ha_state", MagicMock())

    # Initial state
    assert select._attr_current_option == "topSites"

    # Update coordinator data
    mock_content_filtering_coordinator.data = {
        "content_filtering": {
            MOCK_NETWORK["id"]: {
                "urlCategoryListSize": "fullList",
            }
        }
    }

    # Trigger update
    select._handle_coordinator_update()

    assert select._attr_current_option == "fullList"
