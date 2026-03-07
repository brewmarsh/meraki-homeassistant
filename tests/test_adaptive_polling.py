"""Tests for adaptive polling logic in the Meraki data coordinator."""

from datetime import timedelta
from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.const.config import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)

# Resolved: Using the centralized coordinator path from the 2.3.0-beta.120 refactor
from custom_components.meraki_ha.coordinators import (
    MerakiMainCoordinator as MerakiDataCoordinator,
)


@pytest.fixture
def coordinator(hass):
    """Fixture for a MerakiDataCoordinator instance."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
        options={},
    )
    entry.add_to_hass(hass)
    # Patched to reflect the new internal module structure
    with (
        patch(
            "custom_components.meraki_ha.coordinators.base.ApiClient"
        ) as mock_api_client_class,
        patch(
            "custom_components.meraki_ha.coordinators.base.DataFetchManager"
        ) as mock_fetch_manager_class,
    ):
        mock_api_client = mock_api_client_class.return_value
        mock_fetch_manager = mock_fetch_manager_class.return_value
        mock_fetch_manager.get_sensor_data = AsyncMock()
        mock_fetch_manager.get_all_data = mock_fetch_manager.get_sensor_data

        coord = MerakiDataCoordinator(
            hass=hass, entry=entry, api_client=mock_api_client
        )
        yield coord


@pytest.mark.asyncio
async def test_adaptive_polling_429(coordinator):
    """Test that update_interval increases on 429 error."""
    # Set default interval
    coordinator.polling_manager.default_interval = timedelta(seconds=30)
    coordinator.polling_manager._current_interval = timedelta(seconds=30)
    coordinator.update_interval = timedelta(seconds=30)
    coordinator.last_successful_data = {"some": "data"}  # Avoid raising UpdateFailed

    # Mock 429 error
    coordinator.data_fetch_manager.get_sensor_data.side_effect = Exception(
        "meraki.exceptions.APIError: 429 Too Many Requests"
    )

    # Trigger update
    try:
        await coordinator._async_update_data()
    except Exception:
        pass

    # Interval should have doubled (30 * 2 = 60)
    assert coordinator.update_interval == timedelta(seconds=60)
    assert coordinator.polling_manager.consecutive_successes == 0
    assert False in coordinator.polling_manager.success_history

    # Another 429
    try:
        await coordinator._async_update_data()
    except Exception:
        pass
    assert coordinator.update_interval == timedelta(seconds=120)


@pytest.mark.asyncio
async def test_adaptive_polling_recovery(coordinator):
    """Test that update_interval resets after 3 consecutive successes."""
    # Start in cooldown
    coordinator.polling_manager.default_interval = timedelta(seconds=30)
    coordinator.polling_manager._current_interval = timedelta(seconds=120)
    coordinator.update_interval = timedelta(seconds=120)
    coordinator.polling_manager._consecutive_successes = 0

    # Success 1
    coordinator.data_fetch_manager.get_sensor_data.side_effect = None
    coordinator.data_fetch_manager.get_sensor_data.return_value = {"success": True}
    await coordinator._async_update_data()
    assert coordinator.update_interval == timedelta(seconds=120)
    assert coordinator.polling_manager.consecutive_successes == 1

    # Success 2
    await coordinator._async_update_data()
    assert coordinator.update_interval == timedelta(seconds=120)
    assert coordinator.polling_manager.consecutive_successes == 2

    # Success 3
    await coordinator._async_update_data()
    # Should reset to default
    assert coordinator.update_interval == timedelta(seconds=30)
    assert coordinator.polling_manager.consecutive_successes == 3


@pytest.mark.asyncio
async def test_success_history_limit(coordinator):
    """Test that success_history only keeps the last 5 updates."""
    coordinator.data_fetch_manager.get_all_data.return_value = {"success": True}

    # 6 successful updates
    for _ in range(6):
        await coordinator._async_update_data()

    assert len(coordinator.polling_manager.success_history) == 5
    assert all(coordinator.polling_manager.success_history)
