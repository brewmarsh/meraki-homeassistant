"""Tests for switch platform init."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.const import DATA_CLIENT, DOMAIN
from custom_components.meraki_ha.switch import async_setup_entry, async_unload_entry


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock hass instance."""
    hass = MagicMock()
    hass.data = {}
    return hass


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry"
    entry.options = {}
    return entry


@pytest.fixture
def mock_add_entities() -> MagicMock:
    """Create a mock add entities callback."""
    return MagicMock()


@pytest.mark.asyncio
async def test_async_setup_entry_no_entry_data(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup returns False when entry not in hass.data."""
    mock_hass.data = {DOMAIN: {}}

    result = await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    assert result is False


@pytest.mark.asyncio
async def test_async_setup_entry_no_api_client(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup returns False when API client not available."""
    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": MagicMock(),
                # No DATA_CLIENT
            }
        }
    }

    result = await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    assert result is False


@pytest.mark.asyncio
async def test_async_setup_entry_with_entities(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup adds switch entities."""
    mock_coordinator = MagicMock()
    mock_api_client = MagicMock()
    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": mock_coordinator,
                DATA_CLIENT: mock_api_client,
            }
        }
    }

    mock_entities = [MagicMock(), MagicMock()]

    with patch(
        "custom_components.meraki_ha.switch.async_setup_switches",
        return_value=mock_entities,
    ):
        result = await async_setup_entry(
            mock_hass, mock_config_entry, mock_add_entities
        )

    assert result is True
    mock_add_entities.assert_called()


@pytest.mark.asyncio
async def test_async_setup_entry_no_entities(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup succeeds with no entities."""
    mock_coordinator = MagicMock()
    mock_api_client = MagicMock()
    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": mock_coordinator,
                DATA_CLIENT: mock_api_client,
            }
        }
    }

    with patch(
        "custom_components.meraki_ha.switch.async_setup_switches",
        return_value=[],
    ):
        result = await async_setup_entry(
            mock_hass, mock_config_entry, mock_add_entities
        )

    assert result is True
    mock_add_entities.assert_not_called()


@pytest.mark.asyncio
async def test_async_setup_entry_large_entity_count(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup chunks large entity counts."""
    mock_coordinator = MagicMock()
    mock_api_client = MagicMock()
    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": mock_coordinator,
                DATA_CLIENT: mock_api_client,
            }
        }
    }

    # Create more than 50 entities to trigger chunking
    mock_entities = [MagicMock() for _ in range(75)]

    with patch(
        "custom_components.meraki_ha.switch.async_setup_switches",
        return_value=mock_entities,
    ):
        with patch.object(asyncio, "sleep", new_callable=AsyncMock):
            result = await async_setup_entry(
                mock_hass, mock_config_entry, mock_add_entities
            )

    assert result is True
    # Should be called twice (50 + 25)
    assert mock_add_entities.call_count == 2


@pytest.mark.asyncio
async def test_async_unload_entry(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test unload entry."""
    mock_hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)

    result = await async_unload_entry(mock_hass, mock_config_entry)

    assert result is True
    mock_hass.config_entries.async_unload_platforms.assert_called_once()

