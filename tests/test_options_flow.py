"""Tests for the Meraki options flow."""

from __future__ import annotations

import pytest
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import (
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_ENABLE_VLAN_MANAGEMENT,
    CONF_IGNORED_NETWORKS,
    DOMAIN,
)


@pytest.mark.asyncio
async def test_options_flow(hass: HomeAssistant) -> None:
    """
    Test the options flow.

    Args:
    ----
        hass: The Home Assistant instance.

    """
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

    # Submit updated options
    options_input = {
        CONF_SCAN_INTERVAL: 120,
        CONF_ENABLE_DEVICE_TRACKER: False,
        CONF_IGNORED_NETWORKS: "Guest Network, Temp Network",
        CONF_ENABLE_VLAN_MANAGEMENT: True,
    }
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input=options_input,
    )
    await hass.async_block_till_done()

    assert result["type"] == "create_entry"
    assert config_entry.options == options_input
