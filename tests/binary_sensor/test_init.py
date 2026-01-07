"""Tests for binary sensor platform init."""

from unittest.mock import MagicMock

import pytest
from homeassistant.components.binary_sensor import BinarySensorEntity

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.binary_sensor import async_setup_entry


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
async def test_async_setup_entry_no_entities(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup succeeds with no binary sensor entities."""
    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": MagicMock(),
                "entities": [],
            }
        }
    }

    result = await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    assert result is True
    mock_add_entities.assert_not_called()


@pytest.mark.asyncio
async def test_async_setup_entry_with_binary_sensor_entities(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup adds binary sensor entities."""
    mock_binary_sensor = MagicMock(spec=BinarySensorEntity)
    mock_other_entity = MagicMock()  # Not a BinarySensorEntity

    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": MagicMock(),
                "entities": [mock_binary_sensor, mock_other_entity],
            }
        }
    }

    result = await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    assert result is True
    mock_add_entities.assert_called_once()
    # Should only add the binary sensor entity
    call_args = mock_add_entities.call_args[0][0]
    assert len(call_args) == 1


@pytest.mark.asyncio
async def test_async_setup_entry_filters_other_entities(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
    mock_add_entities: MagicMock,
) -> None:
    """Test setup filters out non-binary-sensor entities."""
    # Only non-binary-sensor entities
    mock_hass.data = {
        DOMAIN: {
            "test_entry": {
                "coordinator": MagicMock(),
                "entities": [MagicMock(), MagicMock()],
            }
        }
    }

    result = await async_setup_entry(mock_hass, mock_config_entry, mock_add_entities)

    assert result is True
    mock_add_entities.assert_not_called()
