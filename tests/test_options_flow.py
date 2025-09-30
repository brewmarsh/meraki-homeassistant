"""Tests for the Meraki options flow."""
import sys
from unittest.mock import MagicMock

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL

from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_WEB_UI,
    CONF_WEB_UI_PORT,
    CONF_IGNORED_NETWORKS,
)

# Mock the hass_frontend module
sys.modules['hass_frontend'] = MagicMock()


@pytest.mark.asyncio
async def test_options_flow(hass: HomeAssistant, mocker) -> None:
    """Test the options flow."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry_id",
        title="Test Org",
        data={
            "meraki_api_key": "test-api-key",
            "meraki_org_id": "test-org-id",
        },
        options={
            CONF_SCAN_INTERVAL: 60,
            CONF_ENABLE_DEVICE_TRACKER: True,
        },
    )
    config_entry.add_to_hass(hass)

    # Start the options flow
    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert result["type"] == "form"
    assert result["step_id"] == "init"

    # Select "general" from the menu
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], user_input={"next_step": "general"}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "general"

    # Submit general options
    general_input = {
        CONF_SCAN_INTERVAL: 120,
        CONF_ENABLE_DEVICE_TRACKER: False,
    }
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], user_input=general_input
    )
    await hass.async_block_till_done()

    assert result["type"] == "create_entry"
    assert config_entry.options == general_input

    # Start the options flow again
    result = await hass.config_entries.options.async_init(config_entry.entry_id)

    # Select "advanced" from the menu
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], user_input={"next_step": "advanced"}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "advanced"

    # Submit advanced options
    advanced_input = {
        CONF_IGNORED_NETWORKS: "Guest Network, Temp Network",
        CONF_ENABLE_WEB_UI: False,
        CONF_WEB_UI_PORT: 8080,
    }
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], user_input=advanced_input
    )
    await hass.async_block_till_done()

    assert result["type"] == "create_entry"
    expected_options = {**general_input, **advanced_input}
    assert config_entry.options == expected_options
