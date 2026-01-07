"""Tests for sensor platform init."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.components.sensor import SensorEntity

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.sensor import async_setup_entry


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


@pytest.fixture
def mock_sensor_entity() -> MagicMock:
    """Create a mock sensor entity."""
    entity = MagicMock(spec=SensorEntity)
    return entity


@pytest.mark.asyncio
async def test_async_setup_entry_no_entities(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup succeeds with no discovered entities."""
    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "entities": [],
            }
        }
    }

    result = await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    assert result is True
    mock_add_entities.assert_not_called()


@pytest.mark.asyncio
async def test_async_setup_entry_with_sensor_entities(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
    mock_sensor_entity: MagicMock,
) -> None:
    """Test setup adds sensor entities."""
    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "entities": [mock_sensor_entity, mock_sensor_entity],
            }
        }
    }

    result = await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    assert result is True
    mock_add_entities.assert_called()


@pytest.mark.asyncio
async def test_async_setup_entry_filters_non_sensors(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
    mock_sensor_entity: MagicMock,
) -> None:
    """Test setup filters out non-sensor entities."""
    # Create a non-sensor entity
    non_sensor = MagicMock()  # Not spec'd as SensorEntity

    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "entities": [mock_sensor_entity, non_sensor],
            }
        }
    }

    result = await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    assert result is True
    # Only the sensor entity should be added
    mock_add_entities.assert_called_once()
    call_args = mock_add_entities.call_args[0][0]
    assert len(call_args) == 1


@pytest.mark.asyncio
async def test_async_setup_entry_chunks_large_lists(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup chunks large entity lists."""
    # Create more than 50 sensor entities
    entities = [MagicMock(spec=SensorEntity) for _ in range(75)]

    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "entities": entities,
            }
        }
    }

    with patch.object(asyncio, "sleep", new_callable=AsyncMock):
        result = await async_setup_entry(
            mock_hass, mock_config_entry, mock_add_entities
        )

    assert result is True
    # Should be called twice (50 + 25)
    assert mock_add_entities.call_count == 2

