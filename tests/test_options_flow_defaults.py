"""Test the Meraki HA options flow defaults."""

from typing import Any
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.config import (
    CONF_ENABLE_DEVICE_STATUS,
    CONF_MERAKI_API_KEY,
    CONF_SCAN_INTERVAL,
)
from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant import config_entries

async def test_options_flow_defaults(hass: HomeAssistant) -> None:
    """Test that the options flow correctly pre-fills defaults from existing options."""
    options = {
        CONF_SCAN_INTERVAL: "900",
        CONF_ENABLE_DEVICE_STATUS: False,
    }
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_MERAKI_API_KEY: "test-api-key"},
        options=options,
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] == FlowResultType.MENU

    # Check General Settings Step
    result_general = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"next_step_id": "general"},
    )
    assert result_general["type"] == FlowResultType.FORM

    # In Home Assistant, the suggested values are passed to the form.
    # Since we are setting them as defaults in the schema,
    # we should check if the schema has the correct default values.
    schema = result_general["data_schema"].schema
    for key in schema:
        if key == CONF_SCAN_INTERVAL:
            assert key.default() == "900"

    # Check Sensors Step
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result_sensors = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"next_step_id": "sensors"},
    )
    assert result_sensors["type"] == FlowResultType.FORM
    schema = result_sensors["data_schema"].schema
    for key in schema:
        if key == CONF_ENABLE_DEVICE_STATUS:
            assert key.default() == False
