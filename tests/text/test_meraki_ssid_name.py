"""Tests for the Meraki SSID name text entity."""

import pytest
from unittest.mock import MagicMock, AsyncMock

from custom_components.meraki_ha.text.meraki_ssid_name import (
    MerakiSSIDNameText,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiNetworkCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "ssid_0": {
            "number": 0,
            "name": "Test SSID",
            "enabled": True,
            "networkId": "net-123",
            "unique_id": "ssid_0",
            "productType": "ssid",
        }
    }
    return coordinator


@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.update_network_wireless_ssid = AsyncMock()
    return client


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {}
    return entry


async def test_meraki_ssid_name_text(
    mock_coordinator, mock_meraki_client, mock_config_entry
) -> None:
    """Test the Meraki SSID name text entity."""
    ssid_data = mock_coordinator.data["ssid_0"]
    text = MerakiSSIDNameText(
        mock_coordinator, mock_meraki_client, mock_config_entry, "ssid_0", ssid_data
    )

    assert text.native_value == "Test SSID"
    assert text.name == "[Ssid] Test SSID"

    await text.async_set_value("New Name")
    mock_meraki_client.update_network_wireless_ssid.assert_called_with(
        network_id="net-123", number=0, name="New Name"
    )
