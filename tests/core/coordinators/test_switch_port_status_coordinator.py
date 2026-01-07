"""Tests for switch port status coordinator."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.coordinators.switch_port_status_coordinator import (
    SwitchPortStatusCoordinator,
)


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock hass instance."""
    return MagicMock()


@pytest.fixture
def mock_repository() -> MagicMock:
    """Create a mock repository."""
    repo = MagicMock()
    repo.async_get_switch_port_statuses = AsyncMock(return_value=[])
    return repo


@pytest.fixture
def mock_main_coordinator() -> MagicMock:
    """Create a mock main coordinator."""
    coordinator = MagicMock()
    coordinator.data = {"devices": []}
    return coordinator


@pytest.fixture
def mock_config_entry_for_coordinator() -> MagicMock:
    """Create a mock config entry for coordinator tests."""
    entry = MagicMock()
    entry.entry_id = "test_entry"
    return entry


def test_coordinator_initialization(
    mock_hass: MagicMock,
    mock_repository: MagicMock,
    mock_main_coordinator: MagicMock,
    mock_config_entry_for_coordinator: MagicMock,
) -> None:
    """Test coordinator initializes correctly."""
    coordinator = SwitchPortStatusCoordinator(
        hass=mock_hass,
        repository=mock_repository,
        main_coordinator=mock_main_coordinator,
        config_entry=mock_config_entry_for_coordinator,
        update_interval=30,
    )

    assert coordinator.repository is mock_repository
    assert coordinator.main_coordinator is mock_main_coordinator
    # Note: config_entry may be set to None by parent DataUpdateCoordinator
    # The value we passed is stored, but the parent class also has config_entry attr


@pytest.mark.asyncio
async def test_async_update_data_empty_devices(
    mock_hass: MagicMock,
    mock_repository: MagicMock,
    mock_main_coordinator: MagicMock,
    mock_config_entry_for_coordinator: MagicMock,
) -> None:
    """Test update returns empty when no switch devices."""
    mock_main_coordinator.data = {"devices": []}

    coordinator = SwitchPortStatusCoordinator(
        hass=mock_hass,
        repository=mock_repository,
        main_coordinator=mock_main_coordinator,
        config_entry=mock_config_entry_for_coordinator,
    )

    result = await coordinator._async_update_data()

    assert result == {"port_statuses": {}}


@pytest.mark.asyncio
async def test_async_update_data_no_data(
    mock_hass: MagicMock,
    mock_repository: MagicMock,
    mock_main_coordinator: MagicMock,
    mock_config_entry_for_coordinator: MagicMock,
) -> None:
    """Test update returns empty when main coordinator has no data."""
    mock_main_coordinator.data = None

    coordinator = SwitchPortStatusCoordinator(
        hass=mock_hass,
        repository=mock_repository,
        main_coordinator=mock_main_coordinator,
        config_entry=mock_config_entry_for_coordinator,
    )

    result = await coordinator._async_update_data()

    assert result == {"port_statuses": {}}


@pytest.mark.asyncio
async def test_async_update_data_with_switch_devices(
    mock_hass: MagicMock,
    mock_repository: MagicMock,
    mock_main_coordinator: MagicMock,
    mock_config_entry_for_coordinator: MagicMock,
) -> None:
    """Test update fetches port statuses for switch devices."""
    mock_main_coordinator.data = {
        "devices": [
            {"serial": "SW-001", "productType": "switch"},
            {"serial": "AP-001", "productType": "wireless"},
        ]
    }
    mock_repository.async_get_switch_port_statuses.return_value = [
        {"portId": "1", "status": "Connected"},
        {"portId": "2", "status": "Disconnected"},
    ]

    coordinator = SwitchPortStatusCoordinator(
        hass=mock_hass,
        repository=mock_repository,
        main_coordinator=mock_main_coordinator,
        config_entry=mock_config_entry_for_coordinator,
    )

    result = await coordinator._async_update_data()

    assert "port_statuses" in result
    assert "SW-001" in result["port_statuses"]
    assert len(result["port_statuses"]["SW-001"]) == 2
    mock_repository.async_get_switch_port_statuses.assert_called_once_with("SW-001")


@pytest.mark.asyncio
async def test_async_update_data_handles_errors(
    mock_hass: MagicMock,
    mock_repository: MagicMock,
    mock_main_coordinator: MagicMock,
    mock_config_entry_for_coordinator: MagicMock,
) -> None:
    """Test update handles errors gracefully."""
    mock_main_coordinator.data = {
        "devices": [
            {"serial": "SW-001", "productType": "switch"},
        ]
    }
    mock_repository.async_get_switch_port_statuses.side_effect = Exception("API Error")

    coordinator = SwitchPortStatusCoordinator(
        hass=mock_hass,
        repository=mock_repository,
        main_coordinator=mock_main_coordinator,
        config_entry=mock_config_entry_for_coordinator,
    )

    result = await coordinator._async_update_data()

    # Should return empty dict for failed device, not raise
    assert result == {"port_statuses": {}}


@pytest.mark.asyncio
async def test_async_update_data_multiple_switches(
    mock_hass: MagicMock,
    mock_repository: MagicMock,
    mock_main_coordinator: MagicMock,
    mock_config_entry_for_coordinator: MagicMock,
) -> None:
    """Test update fetches port statuses for multiple switches."""
    mock_main_coordinator.data = {
        "devices": [
            {"serial": "SW-001", "productType": "switch"},
            {"serial": "SW-002", "productType": "switch"},
        ]
    }
    mock_repository.async_get_switch_port_statuses.side_effect = [
        [{"portId": "1", "status": "Connected"}],
        [{"portId": "1", "status": "Disconnected"}],
    ]

    coordinator = SwitchPortStatusCoordinator(
        hass=mock_hass,
        repository=mock_repository,
        main_coordinator=mock_main_coordinator,
        config_entry=mock_config_entry_for_coordinator,
    )

    result = await coordinator._async_update_data()

    assert "SW-001" in result["port_statuses"]
    assert "SW-002" in result["port_statuses"]
