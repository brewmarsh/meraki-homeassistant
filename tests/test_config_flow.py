"""Test the Meraki HA config flow."""

from unittest.mock import AsyncMock, MagicMock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.config import (
    CONF_ENABLE_DEVICE_STATUS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant import config_entries, setup
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_form(hass: HomeAssistant) -> None:
    """Test we get the form."""
    await setup.async_setup_component(hass, "persistent_notification", {})
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    with (
        patch(
            "custom_components.meraki_ha.core.api.create_api_client",
        ) as mock_create_client,
        patch(
            "custom_components.meraki_ha.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
    ):
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client

        mock_client.async_setup = AsyncMock()
        mock_client.get_organizations = AsyncMock(
            return_value=[{"id": "test-org-id", "name": "Test Org"}]
        )

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_MERAKI_API_KEY: "test-api-key",
                CONF_MERAKI_ORG_ID: "test-org-id",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Cisco Meraki"
    assert result2["data"] == {
        CONF_MERAKI_API_KEY: "test-api-key",
        CONF_MERAKI_ORG_ID: "test-org-id",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test we handle cannot connect error."""
    result = await setup.async_setup_component(hass, "persistent_notification", {})
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.meraki_ha.core.api.create_api_client",
        side_effect=Exception,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_MERAKI_API_KEY: "test-api-key",
                CONF_MERAKI_ORG_ID: "test-org-id",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_options_flow(hass: HomeAssistant) -> None:
    """Test the new options flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_MERAKI_API_KEY: "test-api-key"},
        options={},
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] == FlowResultType.MENU
    assert result["step_id"] == "init"

    # Test General Settings Step
    result_general = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"next_step_id": "general"},
    )
    assert result_general["type"] == FlowResultType.FORM
    assert result_general["step_id"] == "general"

    # Save General Settings
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_reload",
        return_value=None,
    ):
        result_save = await hass.config_entries.options.async_configure(
            result_general["flow_id"],
            user_input={
                "scan_interval": "300",
                "enable_device_tracker": True,
            },
        )
        await hass.async_block_till_done()

    assert result_save["type"] == FlowResultType.CREATE_ENTRY
    assert entry.options["scan_interval"] == "300"
    assert entry.options["enable_device_tracker"] is True

    # Test Sensors Step (verifying merge)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result_sensors = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"next_step_id": "sensors"},
    )
    assert result_sensors["type"] == FlowResultType.FORM

    with patch(
        "homeassistant.config_entries.ConfigEntries.async_reload",
        return_value=None,
    ):
        result_save = await hass.config_entries.options.async_configure(
            result_sensors["flow_id"],
            user_input={
                CONF_ENABLE_DEVICE_STATUS: False,
            },
        )
        await hass.async_block_till_done()

    assert result_save["type"] == FlowResultType.CREATE_ENTRY
    assert entry.options["scan_interval"] == "300"  # Preserved
    assert entry.options[CONF_ENABLE_DEVICE_STATUS] is False  # Updated


async def test_update_listener(hass: HomeAssistant) -> None:
    """Test the update listener."""
    entry = MockConfigEntry(domain=DOMAIN, entry_id="test_entry_id")
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_reload",
        return_value=None,
    ) as mock_reload:
        from custom_components.meraki_ha import update_listener

        await update_listener(hass, entry)

    mock_reload.assert_called_once_with(entry.entry_id)
