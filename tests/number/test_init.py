"""Tests for number platform init."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.number import async_setup_entry, async_unload_entry


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
async def test_async_setup_entry_with_entities(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup adds number entities."""
    mock_coordinator = MagicMock()
    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": mock_coordinator,
            }
        }
    }

    mock_entities = [MagicMock(), MagicMock()]

    with patch(
        "custom_components.meraki_ha.number.async_setup_numbers",
        return_value=mock_entities,
    ):
        result = await async_setup_entry(
            mock_hass, mock_config_entry, mock_add_entities
        )

    assert result is True
    mock_add_entities.assert_called_once_with(mock_entities)


@pytest.mark.asyncio
async def test_async_setup_entry_no_entities(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup succeeds with no entities."""
    mock_coordinator = MagicMock()
    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": mock_coordinator,
            }
        }
    }

    with patch(
        "custom_components.meraki_ha.number.async_setup_numbers",
        return_value=[],
    ):
        result = await async_setup_entry(
            mock_hass, mock_config_entry, mock_add_entities
        )

    assert result is True
    mock_add_entities.assert_not_called()


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

