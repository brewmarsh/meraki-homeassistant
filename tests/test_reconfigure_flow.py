"""Tests for the Meraki reconfiguration flow."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.config import (
    AUTH_TYPE_API_KEY,
    AUTH_TYPE_OAUTH,
    CONF_AUTH_TYPE,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_OAUTH_TOKEN,
)
from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.core.errors import (
    ApiClientCommunicationError,
    MerakiAuthenticationError,
)
from homeassistant import config_entries, setup
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def _init_reconfigure_flow(
    hass: HomeAssistant,
    entry: MockConfigEntry,
) -> dict[str, object]:
    """Helper to initialize reconfigure flow."""
    return await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_RECONFIGURE,
            "entry_id": entry.entry_id,
        },
    )


async def test_reconfigure_flow_api_key_success(hass: HomeAssistant) -> None:
    """Test successful reconfiguration with a new API key."""
    await setup.async_setup_component(hass, "persistent_notification", {})

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_AUTH_TYPE: AUTH_TYPE_API_KEY,
            CONF_MERAKI_API_KEY: "old-api-key",
            CONF_MERAKI_ORG_ID: "test-org-id",
        },
        entry_id="test_reconfig_entry_1",
    )
    entry.add_to_hass(hass)

    result = await _init_reconfigure_flow(hass, entry)
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    with (
        patch(
            "custom_components.meraki_ha.reconfigure_flow.validate_meraki_credentials",
            new_callable=AsyncMock,
            return_value=True,
        ),
        patch(
            "homeassistant.config_entries.ConfigEntries.async_reload",
            new_callable=AsyncMock,
            return_value=True,
        ) as mock_reload,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            str(result["flow_id"]),
            user_input={
                CONF_AUTH_TYPE: AUTH_TYPE_API_KEY,
                CONF_MERAKI_API_KEY: "new-api-key",
            },
        )

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "reconfigure_successful"
    assert entry.data[CONF_MERAKI_API_KEY] == "new-api-key"
    assert entry.data[CONF_AUTH_TYPE] == AUTH_TYPE_API_KEY
    mock_reload.assert_called_once_with(entry.entry_id)


async def test_reconfigure_flow_oauth_direct_token_success(
    hass: HomeAssistant,
) -> None:
    """Test successful reconfiguration with a direct OAuth token."""
    await setup.async_setup_component(hass, "persistent_notification", {})

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_AUTH_TYPE: AUTH_TYPE_API_KEY,
            CONF_MERAKI_API_KEY: "old-api-key",
            CONF_MERAKI_ORG_ID: "test-org-id",
        },
        entry_id="test_reconfig_entry_2",
    )
    entry.add_to_hass(hass)

    result = await _init_reconfigure_flow(hass, entry)
    assert result["type"] == FlowResultType.FORM

    with (
        patch(
            "custom_components.meraki_ha.reconfigure_flow.validate_meraki_credentials",
            new_callable=AsyncMock,
            return_value=True,
        ),
        patch(
            "homeassistant.config_entries.ConfigEntries.async_reload",
            new_callable=AsyncMock,
            return_value=True,
        ) as mock_reload,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            str(result["flow_id"]),
            user_input={
                CONF_AUTH_TYPE: AUTH_TYPE_OAUTH,
                CONF_OAUTH_TOKEN: "new-oauth-token",
            },
        )

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "reconfigure_successful"
    assert entry.data[CONF_MERAKI_API_KEY] == "new-oauth-token"
    assert entry.data[CONF_AUTH_TYPE] == AUTH_TYPE_OAUTH
    mock_reload.assert_called_once_with(entry.entry_id)


async def test_reconfigure_flow_invalid_auth(hass: HomeAssistant) -> None:
    """Test reconfigure flow handles invalid authentication error."""
    await setup.async_setup_component(hass, "persistent_notification", {})

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_AUTH_TYPE: AUTH_TYPE_API_KEY,
            CONF_MERAKI_API_KEY: "old-api-key",
            CONF_MERAKI_ORG_ID: "test-org-id",
        },
        entry_id="test_reconfig_entry_3",
    )
    entry.add_to_hass(hass)

    result = await _init_reconfigure_flow(hass, entry)
    assert result["type"] == FlowResultType.FORM

    with patch(
        "custom_components.meraki_ha.reconfigure_flow.validate_meraki_credentials",
        side_effect=MerakiAuthenticationError("Invalid credentials"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            str(result["flow_id"]),
            user_input={
                CONF_AUTH_TYPE: AUTH_TYPE_API_KEY,
                CONF_MERAKI_API_KEY: "wrong-api-key",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_reconfigure_flow_cannot_connect(hass: HomeAssistant) -> None:
    """Test reconfigure flow handles connection errors."""
    await setup.async_setup_component(hass, "persistent_notification", {})

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_AUTH_TYPE: AUTH_TYPE_API_KEY,
            CONF_MERAKI_API_KEY: "old-api-key",
            CONF_MERAKI_ORG_ID: "test-org-id",
        },
        entry_id="test_reconfig_entry_4",
    )
    entry.add_to_hass(hass)

    result = await _init_reconfigure_flow(hass, entry)
    assert result["type"] == FlowResultType.FORM

    with patch(
        "custom_components.meraki_ha.reconfigure_flow.validate_meraki_credentials",
        side_effect=ApiClientCommunicationError("Cannot reach server"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            str(result["flow_id"]),
            user_input={
                CONF_AUTH_TYPE: AUTH_TYPE_API_KEY,
                CONF_MERAKI_API_KEY: "test-key",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_reconfigure_flow_oauth_web_success(hass: HomeAssistant) -> None:
    """Test reconfigure flow completes successfully via OAuth web authorization."""
    await setup.async_setup_component(hass, "persistent_notification", {})

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_AUTH_TYPE: AUTH_TYPE_API_KEY,
            CONF_MERAKI_API_KEY: "old-api-key",
            CONF_MERAKI_ORG_ID: "test-org-id",
        },
        entry_id="test_reconfig_entry_oauth_web",
    )
    entry.add_to_hass(hass)

    result = await _init_reconfigure_flow(hass, entry)
    assert result["type"] == FlowResultType.FORM

    flow = hass.config_entries.flow._progress[result["flow_id"]]

    with patch(
        "homeassistant.config_entries.ConfigEntries.async_reload",
        new_callable=AsyncMock,
        return_value=True,
    ) as mock_reload:
        result2 = await flow.async_oauth_create_entry(
            {
                "token": {
                    "access_token": "oauth-web-access-token",
                    "token_type": "Bearer",
                }
            }
        )

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "reconfigure_successful"
    assert entry.data[CONF_MERAKI_API_KEY] == "oauth-web-access-token"
    assert entry.data[CONF_AUTH_TYPE] == AUTH_TYPE_OAUTH
    assert entry.data["token"]["access_token"] == "oauth-web-access-token"
    mock_reload.assert_called_once_with(entry.entry_id)
