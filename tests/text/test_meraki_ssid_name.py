"""Tests for the Meraki SSID Name text entity."""

import pytest
from unittest.mock import MagicMock, AsyncMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.text.meraki_ssid_name import MerakiSSIDNameText


@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.wireless.update_network_wireless_ssid = AsyncMock()
    return client


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


async def test_ssid_name_set_value(
    hass: HomeAssistant, mock_coordinator, mock_meraki_client
):
    """Test the async_set_value method calls the API correctly."""
    config_entry = MagicMock()
    ssid_data = {
        "number": 0,
        "name": "Old SSID Name",
        "networkId": "net1",
    }

    entity = MerakiSSIDNameText(
        mock_coordinator, mock_meraki_client, config_entry, ssid_data
    )
    entity.hass = hass
    entity.entity_id = "text.test_ssid_name"

    new_name = "New SSID Name"
    await entity.async_set_value(new_name)

    # Verify that the API was called with the correct parameters
    mock_meraki_client.wireless.update_network_wireless_ssid.assert_called_once_with(
        networkId="net1",
        number="0",
        name=new_name,
    )

    # Verify that the coordinator was asked to refresh
    mock_coordinator.async_request_refresh.assert_called_once()

    # Verify that the entity's state was optimistically updated
    assert entity.native_value == new_name
