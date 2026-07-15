"""Test the Meraki HA config flow."""

from unittest.mock import AsyncMock, patch

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
    """Test the multi-step config flow."""
    from custom_components.meraki_ha.const.config import CONF_ENABLED_NETWORKS

    await setup.async_setup_component(hass, "persistent_notification", {})

    # Step 1: User enters API Key
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    with (
        patch(
            "custom_components.meraki_ha.core.api.create_api_client",
        ) as mock_create_client,
        patch(
            "custom_components.meraki_ha.async_setup_entry",
            new_callable=AsyncMock,
            return_value=True,
        ) as mock_setup_entry,
    ):
        mock_client = AsyncMock()
        mock_create_client.return_value = mock_client

        mock_client.async_setup = AsyncMock()
        mock_client.get_organizations = AsyncMock(
            return_value=[{"id": "test-org-id", "name": "Test Org"}]
        )
        mock_client.organization.get_organization_networks = AsyncMock(
            return_value=[{"id": "test-net-id", "name": "Test Network"}]
        )

        # Submit API Key
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_MERAKI_API_KEY: "test-api-key",
            },
        )
        await hass.async_block_till_done()

        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "org"

        # Step 2: User selects Organization
        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"],
            {
                CONF_MERAKI_ORG_ID: "test-org-id",
            },
        )
        await hass.async_block_till_done()

        assert result3["type"] == FlowResultType.FORM
        assert result3["step_id"] == "networks"

        # Step 3: User selects Networks
        result4 = await hass.config_entries.flow.async_configure(
            result3["flow_id"],
            {
                CONF_ENABLED_NETWORKS: ["test-net-id"],
            },
        )
        await hass.async_block_till_done()

    assert result4["type"] == FlowResultType.CREATE_ENTRY
    assert result4["title"] == "Cisco Meraki"
    assert result4["data"] == {
        CONF_MERAKI_API_KEY: "test-api-key",
        CONF_MERAKI_ORG_ID: "test-org-id",
        CONF_ENABLED_NETWORKS: ["test-net-id"],
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test we handle cannot connect error."""
    await setup.async_setup_component(hass, "persistent_notification", {})
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
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_options_flow(hass: HomeAssistant) -> None:
    """Test the new options flow."""
    # Action 2: Ensure MockConfigEntry has explicit entry_id and is added to hass
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_MERAKI_API_KEY: "test-api-key"},
        options={},
        entry_id="test_entry_id",
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
    # Action 1: Use AsyncMock for reload
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_reload",
        new_callable=AsyncMock,
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

    # Action 1: Use AsyncMock for reload
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_reload",
        new_callable=AsyncMock,
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
    # Action 2: Ensure MockConfigEntry has explicit entry_id and is added to hass
    entry = MockConfigEntry(domain=DOMAIN, entry_id="test_entry_id")
    entry.add_to_hass(hass)
    # Action 1: Use AsyncMock for reload
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_reload",
        new_callable=AsyncMock,
        return_value=None,
    ) as mock_reload:
        from custom_components.meraki_ha import update_listener

        await update_listener(hass, entry)

    mock_reload.assert_called_once_with(entry.entry_id)
