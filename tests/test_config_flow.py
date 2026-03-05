# TODO:
# SETUP-P0-01: Test successful setup with valid API key and organization ID
# - Mock the Meraki API client to return valid data.
# - Trigger the config flow with the mock client.
# - Assert that the flow completes successfully and a config entry is created.
#
# SETUP-P0-02: Test setup failure with invalid API key
# - Mock the Meraki API client to raise an AuthenticationError.
# - Trigger the config flow.
# - Assert that the flow shows an "invalid_auth" error.

"""Test the Meraki HA config flow."""

from unittest.mock import MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.const_conf import (
    CONF_ENABLE_CAMERA_ENTITIES,
    CONF_ENABLE_VLAN_MANAGEMENT,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
)
from custom_components.meraki_ha.core.errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
)
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
            "custom_components.meraki_ha.authentication.validate_meraki_credentials",
            return_value={"valid": True, "org_name": "Test Org"},
        ),
        patch(
            "custom_components.meraki_ha.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "meraki_api_key": "test-api-key",
                "meraki_org_id": "test-org-id",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Test Org"
    assert result2["data"] == {
        "meraki_api_key": "test-api-key",
        "meraki_org_id": "test-org-id",
        "enable_vpn_management": False,
        "enable_firewall_rules": False,
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_auth(hass: HomeAssistant) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.meraki_ha.authentication.validate_meraki_credentials",
        side_effect=MerakiAuthenticationError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "meraki_api_key": "test-api-key",
                "meraki_org_id": "test-org-id",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.meraki_ha.authentication.validate_meraki_credentials",
        side_effect=MerakiConnectionError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "meraki_api_key": "test-api-key",
                "meraki_org_id": "test-org-id",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_reconfigure(hass: HomeAssistant) -> None:
    """Test reconfigure flow regression (fix for AttributeError and TypeError)."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_MERAKI_API_KEY: "test-api-key", CONF_MERAKI_ORG_ID: "test-org-id"},
        options={},
    )
    entry.add_to_hass(hass)

    # Mock the coordinator and data
    coordinator = MagicMock()
    # Simulate data as objects (as returned by client.py)
    mock_network = MagicMock()
    mock_network.id = "net1"
    mock_network.name = "Network 1"
    # Ensure subscripting fails to verify we handle objects correctly
    mock_network.__getitem__ = MagicMock(side_effect=TypeError("Not subscriptable"))

    coordinator.data = {"networks": [mock_network]}

    # Setup hass.data as it is in __init__.py
    hass.data[DOMAIN] = {entry.entry_id: {"coordinator": coordinator}}

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_RECONFIGURE,
            "entry_id": entry.entry_id,
        },
    )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reconfigure"


async def test_options_flow(hass: HomeAssistant) -> None:
    """Test the new options flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_MERAKI_API_KEY: "test-api-key", CONF_MERAKI_ORG_ID: "test-org-id"},
        options={},
    )
    entry.add_to_hass(hass)

    # Mock the coordinator and data
    coordinator = MagicMock()
    coordinator.data = {"devices": [], "networks": []}

    # Setup hass.data
    hass.data[DOMAIN] = {entry.entry_id: {"coordinator": coordinator}}

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] == FlowResultType.MENU
    assert result["step_id"] == "init"
    assert "general" in result["menu_options"]
    assert "sensors" in result["menu_options"]

    # Test General Settings step
    result_general = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"next_step_id": "general"},
    )
    assert result_general["type"] == FlowResultType.FORM
    assert result_general["step_id"] == "general"

    # Save General Settings
    result_save = await hass.config_entries.options.async_configure(
        result_general["flow_id"],
        user_input={
            CONF_SCAN_INTERVAL: "300",
            "enabled_networks": [],
            "enable_device_tracker": True,
        },
    )
    assert result_save["type"] == FlowResultType.CREATE_ENTRY


async def test_reconfigure_flow_without_devices(hass: HomeAssistant) -> None:
    """Test reconfigure flow when cameras and switches are NOT present."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_MERAKI_API_KEY: "test-api-key", CONF_MERAKI_ORG_ID: "test-org-id"},
        options={CONF_SCAN_INTERVAL: "300"},
    )
    entry.add_to_hass(hass)

    # Mock the coordinator and data
    coordinator = MagicMock()
    coordinator.data = {"devices": [], "networks": []}

    # Setup hass.data
    hass.data[DOMAIN] = {entry.entry_id: {"coordinator": coordinator}}

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_RECONFIGURE,
            "entry_id": entry.entry_id,
        },
    )

    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reconfigure"
    assert result["data_schema"] is not None

    schema = result["data_schema"].schema
    schema_keys = [k.schema for k in schema.keys()]

    # These should be hidden
    assert CONF_ENABLE_CAMERA_ENTITIES not in schema_keys
    assert CONF_ENABLE_VLAN_MANAGEMENT not in schema_keys

    # Scan interval should still be there
    assert CONF_SCAN_INTERVAL in schema_keys
