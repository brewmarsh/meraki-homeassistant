"""Tests for the Meraki base coordinator."""

from datetime import timedelta
from unittest.mock import AsyncMock, patch

from custom_components.meraki_ha.core.api import MerakiAPIClient
from custom_components.meraki_ha.core.coordinators.base import BaseMerakiCoordinator


@patch("homeassistant.core.HomeAssistant")
async def test_base_meraki_coordinator(mock_hass) -> None:
    """Test the base Meraki coordinator."""
    api_client = AsyncMock(spec=MerakiAPIClient)

    coordinator = BaseMerakiCoordinator(
        hass=mock_hass,
        api_client=api_client,
        name="Test Coordinator",
        update_interval=timedelta(seconds=300),
    )

    # Test that the coordinator was initialized properly
    assert coordinator.api_client == api_client
    assert coordinator.name == "Test Coordinator"
    assert coordinator.update_interval == timedelta(seconds=300)

    # Test the _async_update_data method by overriding in a subclass
    class TestCoordinator(BaseMerakiCoordinator):
        async def _async_update_data(self):
            return {"test": "data"}

    test_coordinator = TestCoordinator(
        hass=mock_hass,
        api_client=api_client,
        name="Test Subclass",
        update_interval=timedelta(seconds=300),
    )

    # Test that the update method works
    result = await test_coordinator._async_update_data()
    assert result == {"test": "data"}


async def test_base_meraki_coordinator_update_data(mock_hass) -> None:
    """Test the base Meraki coordinator's update data functionality."""
    api_client = AsyncMock(spec=MerakiAPIClient)

    # Create a test coordinator subclass that implements _async_update_data
    class TestDataCoordinator(BaseMerakiCoordinator):
        async def _async_update_data(self):
            result = await self.api_client.get_devices()
            return {"devices": result}

    coordinator = TestDataCoordinator(
        hass=mock_hass,
        api_client=api_client,
        name="Test Data Coordinator",
        update_interval=timedelta(seconds=300),
    )

    # Mock the API client response
    test_data = [{"serial": "123", "name": "test device"}]
    api_client.get_devices.return_value = test_data

    # Test the update data method
    result = await coordinator._async_update_data()
    assert result == {"devices": test_data}
    api_client.get_devices.assert_called_once()
    await coordinator._async_update_data()
    assert coordinator.data is not None
