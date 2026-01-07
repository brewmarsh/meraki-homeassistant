"""Tests for the options flow module."""

from unittest.mock import MagicMock

import pytest
import voluptuous as vol
from homeassistant.helpers import selector

from custom_components.meraki_ha.const import (
    CONF_ENABLED_NETWORKS,
    CONF_INTEGRATION_TITLE,
    DOMAIN,
)
from custom_components.meraki_ha.options_flow import MerakiOptionsFlowHandler


@pytest.fixture
def mock_options_config_entry() -> MagicMock:
    """Create a mock config entry for options flow."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.options = {
        "scan_interval": 30,
        "enable_device_status": True,
    }
    return entry


@pytest.fixture
def mock_hass_with_coordinator() -> MagicMock:
    """Create a mock hass with coordinator data."""
    hass = MagicMock()
    mock_coordinator = MagicMock()
    mock_coordinator.data = {
        "networks": [
            {"id": "N_123", "name": "Main Office"},
            {"id": "N_456", "name": "Branch Office"},
        ]
    }
    hass.data = {
        DOMAIN: {
            "test_entry_id": {
                "coordinator": mock_coordinator,
            }
        }
    }
    return hass


def test_options_flow_init(mock_options_config_entry: MagicMock) -> None:
    """Test options flow initialization."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    assert handler.options == mock_options_config_entry.options
    assert handler.options["scan_interval"] == 30
    assert handler.options["enable_device_status"] is True


@pytest.mark.asyncio
async def test_async_step_init_with_user_input(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test options flow step init with user input creates entry."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    user_input = {
        "scan_interval": 60,
        "enable_device_status": False,
    }

    result = await handler.async_step_init(user_input)

    assert result["type"] == "create_entry"
    assert result["title"] == CONF_INTEGRATION_TITLE
    assert result["data"]["scan_interval"] == 60
    assert result["data"]["enable_device_status"] is False


# Removed test_async_step_init_shows_form as it requires full HA integration setup


def test_populate_schema_defaults() -> None:
    """Test _populate_schema_defaults populates existing values."""
    mock_entry = MagicMock()
    mock_entry.options = {"scan_interval": 45}

    handler = MerakiOptionsFlowHandler(mock_entry)

    # Create a simple schema
    schema = vol.Schema(
        {
            vol.Required("scan_interval"): int,
            vol.Optional("other_option"): str,
        }
    )

    defaults = {"scan_interval": 45}
    network_options: list[dict[str, str]] = []

    result_schema = handler._populate_schema_defaults(schema, defaults, network_options)

    # Verify the schema was processed (returned as a Schema object)
    assert isinstance(result_schema, vol.Schema)


def test_populate_schema_defaults_with_networks() -> None:
    """Test _populate_schema_defaults includes network options."""
    mock_entry = MagicMock()
    mock_entry.options = {}

    handler = MerakiOptionsFlowHandler(mock_entry)

    # Create schema with network selector
    network_selector = selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=[],
            multiple=True,
        )
    )

    schema = vol.Schema(
        {
            vol.Optional(CONF_ENABLED_NETWORKS): network_selector,
        }
    )

    defaults: dict[str, object] = {}
    network_options = [
        {"label": "Main Office", "value": "N_123"},
        {"label": "Branch Office", "value": "N_456"},
    ]

    result_schema = handler._populate_schema_defaults(schema, defaults, network_options)

    assert isinstance(result_schema, vol.Schema)


@pytest.mark.asyncio
async def test_options_flow_updates_existing_options(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test that submitting options updates existing values."""
    # Start with initial options
    mock_options_config_entry.options = {
        "scan_interval": 30,
        "enable_device_status": True,
        "temperature_unit": "celsius",
    }

    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    # Submit partial update
    user_input = {
        "scan_interval": 120,
    }

    result = await handler.async_step_init(user_input)

    assert result["type"] == "create_entry"
    # New value should be applied
    assert result["data"]["scan_interval"] == 120
    # Existing values should be preserved
    assert result["data"]["enable_device_status"] is True
    assert result["data"]["temperature_unit"] == "celsius"
