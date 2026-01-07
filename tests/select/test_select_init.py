"""Tests for select platform init."""

from unittest.mock import MagicMock, patch

import pytest

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.select import async_setup_entry


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
async def test_async_setup_entry_no_networks(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup with no networks creates no entities."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = {"networks": []}
    mock_coordinator.api = MagicMock()

    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": mock_coordinator,
            }
        }
    }

    await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    mock_add_entities.assert_not_called()


@pytest.mark.asyncio
async def test_async_setup_entry_with_networks(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup creates select entities for networks."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = {
        "networks": [
            {"id": "N_123", "name": "Test Network"},
        ]
    }
    mock_coordinator.api = MagicMock()

    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": mock_coordinator,
            }
        }
    }

    with patch(
        "custom_components.meraki_ha.select.MerakiContentFilteringSelect"
    ) as MockSelect:
        MockSelect.return_value = MagicMock()
        await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    mock_add_entities.assert_called_once()


@pytest.mark.asyncio
async def test_async_setup_entry_no_coordinator_data(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup handles missing coordinator data."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = None
    mock_coordinator.api = MagicMock()

    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": mock_coordinator,
            }
        }
    }

    await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    mock_add_entities.assert_not_called()
