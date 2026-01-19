"""Tests for the Meraki webhook handling."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import DOMAIN
<<<<<<< HEAD
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
=======
from custom_components.meraki_ha.meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
from custom_components.meraki_ha.webhook import async_handle_webhook


@pytest.fixture
def mock_hass_with_webhook_data(hass: HomeAssistant) -> HomeAssistant:
    """
    Fixture for a mocked Home Assistant object with webhook data.

    Args:
    ----
        hass: The Home Assistant instance.

    Returns
    -------
        The mocked Home Assistant instance.

    """
    config_entry = MagicMock()
<<<<<<< HEAD
    coordinator = MerakiDataUpdateCoordinator(
        hass,
        config_entry,
=======
    coordinator = MerakiDataCoordinator(
        hass,
        api_client=MagicMock(),
        scan_interval=300,
        entry=config_entry,
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
    )
    coordinator.data = {
        "devices": [{"serial": "Q234-ABCD-5678", "status": "online"}],
        "clients": [],
    }
    hass.data[DOMAIN] = {
        "test_webhook_id": {
            "coordinator": coordinator,
            "secret": "test_secret",
        },
    }
    return hass


@pytest.mark.asyncio
async def test_handle_webhook_device_down(
    mock_hass_with_webhook_data: HomeAssistant,
) -> None:
    """
    Test handling a device down webhook.

    Args:
    ----
        mock_hass_with_webhook_data: The mocked Home Assistant instance.

    """
    # Arrange
    webhook_id = "test_webhook_id"
    request = AsyncMock()
    request.json.return_value = {
        "sharedSecret": "test_secret",
        "alertType": "APs went down",
        "deviceSerial": "Q234-ABCD-5678",
    }
    coordinator = mock_hass_with_webhook_data.data[DOMAIN][webhook_id]["coordinator"]
    coordinator.async_update_listeners = MagicMock()

    # Act
    await async_handle_webhook(mock_hass_with_webhook_data, webhook_id, request)

    # Assert
    assert coordinator.data["devices"][0]["status"] == "offline"
    coordinator.async_update_listeners.assert_called_once()


@pytest.mark.asyncio
async def test_handle_webhook_invalid_secret(
    mock_hass_with_webhook_data: HomeAssistant,
) -> None:
    """
    Test that a webhook with an invalid secret is ignored.

    Args:
    ----
        mock_hass_with_webhook_data: The mocked Home Assistant instance.

    """
    # Arrange
    webhook_id = "test_webhook_id"
    request = AsyncMock()
    request.json.return_value = {
        "sharedSecret": "wrong_secret",
        "alertType": "APs went down",
        "deviceSerial": "Q234-ABCD-5678",
    }
    coordinator = mock_hass_with_webhook_data.data[DOMAIN][webhook_id]["coordinator"]
    coordinator.async_update_listeners = MagicMock()

    # Act
    await async_handle_webhook(mock_hass_with_webhook_data, webhook_id, request)

    # Assert
    assert coordinator.data["devices"][0]["status"] == "online"  # Should not change
    coordinator.async_update_listeners.assert_not_called()


@pytest.mark.asyncio
async def test_handle_webhook_unknown_alert(
    mock_hass_with_webhook_data: HomeAssistant,
) -> None:
    """
    Test that an unknown alert type is ignored.

    Args:
    ----
        mock_hass_with_webhook_data: The mocked Home Assistant instance.

    """
    # Arrange
    webhook_id = "test_webhook_id"
    request = AsyncMock()
    request.json.return_value = {
        "sharedSecret": "test_secret",
        "alertType": "Some other alert",
    }
    coordinator = mock_hass_with_webhook_data.data[DOMAIN][webhook_id]["coordinator"]
    coordinator.async_update_listeners = MagicMock()

    # Act
    await async_handle_webhook(mock_hass_with_webhook_data, webhook_id, request)

    # Assert
    coordinator.async_update_listeners.assert_not_called()
