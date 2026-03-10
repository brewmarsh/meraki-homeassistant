"""Test the Meraki HA config flow."""

from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.config import (
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_DEVICE_STATUS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant import config_entries, setup


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

        async def mock_async_setup():
            pass

        mock_client.async_setup = mock_async_setup

        async def mock_get_organizations():
            return [{"id": "test-org-id", "name": "Test Org"}]

        mock_client.get_organizations = mock_get_organizations

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_MERAKI_API_KEY: "test-api-key",
                CONF_MERAKI_ORG_ID: "test-org-id",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Meraki"
    assert result2["data"] == {
        CONF_MERAKI_API_KEY: "test-api-key",
        CONF_MERAKI_ORG_ID: "test-org-id",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test we handle cannot connect error."""
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

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "init"

    # Save Settings
    result_save = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            CONF_ENABLE_DEVICE_STATUS: True,
            "enable_device_sensors": True,
            "enable_port_sensors": False,
            CONF_ENABLE_CAMERA_ENTITIES: True,
        },
    )
    assert result_save["type"] == FlowResultType.CREATE_ENTRY
