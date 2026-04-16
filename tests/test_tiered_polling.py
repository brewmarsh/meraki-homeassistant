"""Tests for tiered polling logic in the Meraki data coordinator."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.config import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.coordinators import (
    MerakiMainCoordinator,
)


@pytest.fixture
def coordinator(hass):
    """Fixture for a MerakiMainCoordinator instance."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
        options={},
        entry_id="test_entry_id",
    )
    entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.meraki_ha.coordinators.base.ApiClient"
        ) as mock_api_client_class,
        patch(
            "custom_components.meraki_ha.coordinators.base.DataFetchManager"
        ) as mock_fetch_manager_class,
    ):
        mock_api_client = mock_api_client_class.return_value
        mock_api_client.organization_id = "test-org"
        mock_fetch_manager = mock_fetch_manager_class.return_value
        mock_fetch_manager.get_sensor_data = AsyncMock(
            return_value={"networks": [], "devices": []}
        )
        mock_fetch_manager.get_device_data = AsyncMock(
            return_value={"networks": [], "devices": []}
        )

        coord = MerakiMainCoordinator(
            hass=hass, entry=entry, api_client=mock_api_client
        )
        # Initialize update_processor and polling_manager mocks
        coord.update_processor = AsyncMock()
        coord.update_processor.process_success.return_value = ({}, {}, {}, False)
        coord.polling_manager = AsyncMock()
        coord.polling_manager.record_success.return_value = {}
        coord.polling_manager.update_interval = None

        yield coord


@pytest.mark.asyncio
async def test_tiered_polling_logic(coordinator):
    """Test that tiered polling switches between fast and slow polls correctly."""
    # 1. Initial poll should be a slow poll (full refresh)
    with patch("time.time", return_value=1000.0):
        await coordinator._async_update_data()
        coordinator.data_fetch_manager.get_sensor_data.assert_called_once()
        coordinator.data_fetch_manager.get_device_data.assert_not_called()
        coordinator.data_fetch_manager.get_sensor_data.reset_mock()

    # 2. Next poll (after 30s) should be a fast poll
    with patch("time.time", return_value=1030.0):
        await coordinator._async_update_data()
        coordinator.data_fetch_manager.get_sensor_data.assert_not_called()
        coordinator.data_fetch_manager.get_device_data.assert_called_once()
        coordinator.data_fetch_manager.get_device_data.reset_mock()

    # 3. Poll after 9 minutes (total 9m 30s) should still be a fast poll
    with patch("time.time", return_value=1570.0):
        await coordinator._async_update_data()
        coordinator.data_fetch_manager.get_sensor_data.assert_not_called()
        coordinator.data_fetch_manager.get_device_data.assert_called_once()
        coordinator.data_fetch_manager.get_device_data.reset_mock()

    # 4. Poll after 10 minutes (total 10m 30s) should be a slow poll
    with patch("time.time", return_value=1631.0):
        await coordinator._async_update_data()
        coordinator.data_fetch_manager.get_sensor_data.assert_called_once()
        coordinator.data_fetch_manager.get_device_data.assert_not_called()
