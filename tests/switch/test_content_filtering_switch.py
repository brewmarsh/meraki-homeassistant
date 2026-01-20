"""Tests for the Meraki content filtering switch."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.switch.content_filtering import (
    MerakiContentFilteringSwitch,
)
from custom_components.meraki_ha.types import MerakiNetwork


@pytest.fixture
def mock_coordinator_with_content_filtering(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator with content filtering data."""
    mock_coordinator.data = {
        "content_filtering": {
            "net_1": {
                "blockedUrlCategories": ["meraki:contentFiltering/category/2"],
            }
        }
    }
    mock_coordinator.async_request_refresh = AsyncMock()
    return mock_coordinator


def test_switch_creation(
    mock_coordinator_with_content_filtering: MagicMock, mock_config_entry: MagicMock
) -> None:
    """Test the creation of the content filtering switch."""
    network = MerakiNetwork(id="net_1", name="Test Network", organization_id="org1")
    category = {"id": "meraki:contentFiltering/category/1", "name": "Social Media"}
    switch = MerakiContentFilteringSwitch(
        mock_coordinator_with_content_filtering, mock_config_entry, network, category
    )
    assert (
        switch.unique_id
        == "meraki-content-filtering-net_1-meraki:contentFiltering/category/1"
    )
    assert switch.name == "Block Social Media"


def test_is_on(
    mock_coordinator_with_content_filtering: MagicMock, mock_config_entry: MagicMock
) -> None:
    """Test the is_on property."""
    network = MerakiNetwork(id="net_1", name="Test Network", organization_id="org1")
    category_on = {"id": "meraki:contentFiltering/category/2", "name": "Gambling"}
    category_off = {"id": "meraki:contentFiltering/category/1", "name": "Social Media"}

    switch_on = MerakiContentFilteringSwitch(
        mock_coordinator_with_content_filtering,
        mock_config_entry,
        network,
        category_on,
    )
    switch_off = MerakiContentFilteringSwitch(
        mock_coordinator_with_content_filtering,
        mock_config_entry,
        network,
        category_off,
    )

    assert switch_on.is_on is True
    assert switch_off.is_on is False


async def test_turn_on(
    mock_coordinator_with_content_filtering: MagicMock, mock_config_entry: MagicMock
) -> None:
    """Test turning the switch on."""
    network = MerakiNetwork(id="net_1", name="Test Network", organization_id="org1")
    category = {"id": "meraki:contentFiltering/category/1", "name": "Social Media"}
    switch = MerakiContentFilteringSwitch(
        mock_coordinator_with_content_filtering, mock_config_entry, network, category
    )

    with (
        patch.object(
            switch._client.appliance,
            "get_network_appliance_content_filtering",
            new_callable=AsyncMock,
            return_value={
                "blockedUrlCategories": ["meraki:contentFiltering/category/2"]
            },
        ) as mock_get,
        patch.object(
            switch._client.appliance,
            "update_network_appliance_content_filtering",
            new_callable=AsyncMock,
        ) as mock_update,
    ):
        await switch.async_turn_on()
        mock_get.assert_called_once_with("net_1")
        mock_update.assert_called_once_with(
            "net_1",
            blockedUrlCategories=[
                "meraki:contentFiltering/category/2",
                "meraki:contentFiltering/category/1",
            ],
        )
        mock_coordinator_with_content_filtering.async_request_refresh.assert_called_once()


async def test_turn_off(
    mock_coordinator_with_content_filtering: MagicMock, mock_config_entry: MagicMock
) -> None:
    """Test turning the switch off."""
    network = MerakiNetwork(id="net_1", name="Test Network", organization_id="org1")
    category = {"id": "meraki:contentFiltering/category/2", "name": "Gambling"}
    switch = MerakiContentFilteringSwitch(
        mock_coordinator_with_content_filtering, mock_config_entry, network, category
    )

    with (
        patch.object(
            switch._client.appliance,
            "get_network_appliance_content_filtering",
            new_callable=AsyncMock,
            return_value={
                "blockedUrlCategories": ["meraki:contentFiltering/category/2"]
            },
        ) as mock_get,
        patch.object(
            switch._client.appliance,
            "update_network_appliance_content_filtering",
            new_callable=AsyncMock,
        ) as mock_update,
    ):
        await switch.async_turn_off()
        mock_get.assert_called_once_with("net_1")
        mock_update.assert_called_once_with(
            "net_1",
            blockedUrlCategories=[],
        )
        mock_coordinator_with_content_filtering.async_request_refresh.assert_called_once()
