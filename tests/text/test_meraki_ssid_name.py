"""Tests for the Meraki SSID Name text entity."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.text.meraki_ssid_name import MerakiSSIDNameText


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.wireless.update_network_wireless_ssid = AsyncMock()
    return client


@pytest.fixture
def mock_coordinator_with_refresh(mock_coordinator: MagicMock) -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator.

    This fixture includes an async_request_refresh mock.
    """
    mock_coordinator.async_request_refresh = AsyncMock()
    return mock_coordinator


async def test_ssid_name_set_value(
    hass: HomeAssistant,
    mock_coordinator_with_refresh: MagicMock,
    mock_meraki_client: MagicMock,
) -> None:
    """Test the async_set_value method calls the API correctly."""
    config_entry = MagicMock()
    ssid_data = {
        "number": 0,
        "name": "Old SSID Name",
        "networkId": "net1",
    }

    entity = MerakiSSIDNameText(
        mock_coordinator_with_refresh, mock_meraki_client, config_entry, ssid_data
    )
    entity.hass = hass
    entity.entity_id = "text.test_ssid_name"

    new_name = "New SSID Name"
    await entity.async_set_value(new_name)

    # Verify that the API was called with the correct parameters
    mock_meraki_client.wireless.update_network_wireless_ssid.assert_called_once_with(
        network_id="net1",
        number="0",
        name=new_name,
    )

    # Verify that the coordinator was asked to refresh
    mock_coordinator_with_refresh.async_request_refresh.assert_called_once()

    # Verify that the entity's state was optimistically updated
    assert entity.native_value == new_name
