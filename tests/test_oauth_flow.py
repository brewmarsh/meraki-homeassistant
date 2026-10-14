"""Tests for the Meraki OAuth authentication flow and application credentials."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.application_credentials import (
    async_get_authorization_server,
    async_get_description_placeholders,
)
from custom_components.meraki_ha.const.config import (
    AUTH_TYPE_OAUTH,
    CONF_AUTH_TYPE,
    CONF_ENABLED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_OAUTH_TOKEN,
)
from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.core.api.factory import create_meraki_client
from homeassistant import config_entries, setup
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_application_credentials_platform(hass: HomeAssistant) -> None:
    """Test Meraki application credentials helpers."""
    auth_server = await async_get_authorization_server(hass)
    assert auth_server.authorize_url == "https://as.meraki.com/oauth/authorize"
    assert auth_server.token_url == "https://as.meraki.com/oauth/token"

    placeholders = await async_get_description_placeholders(hass)
    assert placeholders["oauth_url"] == "https://as.meraki.com/oauth/authorize"


async def test_oauth_direct_token_flow(hass: HomeAssistant) -> None:
    """Test user selects OAuth with a direct bearer token."""
    await setup.async_setup_component(hass, "persistent_notification", {})

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
        mock_client.organization.get_organizations = AsyncMock(
            return_value=[{"id": "test-org-id", "name": "Test Org"}]
        )
        mock_client.organization.get_organization_networks = AsyncMock(
            return_value=[{"id": "test-net-id", "name": "Test Network"}]
        )

        result2 = await hass.config_entries.flow.async_configure(
            str(result["flow_id"]),
            {
                CONF_AUTH_TYPE: AUTH_TYPE_OAUTH,
                CONF_OAUTH_TOKEN: "direct-oauth-token-123",
            },
        )
        await hass.async_block_till_done()

        assert result2["type"] == FlowResultType.FORM
        assert result2["step_id"] == "org"

        result3 = await hass.config_entries.flow.async_configure(
            str(result2["flow_id"]),
            {CONF_MERAKI_ORG_ID: "test-org-id"},
        )
        await hass.async_block_till_done()
        assert result3["step_id"] == "networks"

        result4 = await hass.config_entries.flow.async_configure(
            str(result3["flow_id"]),
            {CONF_ENABLED_NETWORKS: ["test-net-id"]},
        )
        await hass.async_block_till_done()

    assert result4["type"] == FlowResultType.CREATE_ENTRY
    assert result4["data"] == {
        CONF_AUTH_TYPE: AUTH_TYPE_OAUTH,
        CONF_MERAKI_API_KEY: "direct-oauth-token-123",
        CONF_MERAKI_ORG_ID: "test-org-id",
        CONF_ENABLED_NETWORKS: ["test-net-id"],
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_oauth_web_authorization_flow(hass: HomeAssistant) -> None:
    """Test OAuth authorization via web flow."""
    await setup.async_setup_component(hass, "persistent_notification", {})

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    flow = hass.config_entries.flow._progress[result["flow_id"]]

    with (
        patch(
            "custom_components.meraki_ha.core.api.create_api_client",
        ) as mock_create_client,
        patch(
            "custom_components.meraki_ha.async_setup_entry",
            new_callable=AsyncMock,
            return_value=True,
        ),
    ):
        mock_client = AsyncMock()
        mock_create_client.return_value = mock_client
        mock_client.async_setup = AsyncMock()
        mock_client.organization.get_organizations = AsyncMock(
            return_value=[{"id": "oauth-org-id", "name": "OAuth Org"}]
        )
        mock_client.organization.get_organization_networks = AsyncMock(
            return_value=[{"id": "oauth-net-id", "name": "OAuth Network"}]
        )

        result_oauth = await flow.async_oauth_create_entry(
            {"token": {"access_token": "bearer-web-token", "token_type": "Bearer"}}
        )
        flow.cur_step = result_oauth
        assert result_oauth["type"] == FlowResultType.FORM
        assert result_oauth["step_id"] == "org"

        result_org = await hass.config_entries.flow.async_configure(
            str(result_oauth["flow_id"]),
            {CONF_MERAKI_ORG_ID: "oauth-org-id"},
        )
        assert result_org["step_id"] == "networks"

        result_finish = await hass.config_entries.flow.async_configure(
            str(result_org["flow_id"]),
            {CONF_ENABLED_NETWORKS: ["oauth-net-id"]},
        )
        await hass.async_block_till_done()

    assert result_finish["type"] == FlowResultType.CREATE_ENTRY
    assert result_finish["data"][CONF_AUTH_TYPE] == AUTH_TYPE_OAUTH
    assert result_finish["data"][CONF_MERAKI_API_KEY] == "bearer-web-token"
    assert result_finish["data"]["token"]["access_token"] == "bearer-web-token"


async def test_create_meraki_client_oauth_token(hass: HomeAssistant) -> None:
    """Test factory creates client using OAuth access token."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_AUTH_TYPE: AUTH_TYPE_OAUTH,
            CONF_MERAKI_API_KEY: "fallback-key",
            CONF_MERAKI_ORG_ID: "test-org",
            "token": {"access_token": "oauth-primary-token"},
        },
        entry_id="test_oauth_factory_entry",
    )

    with patch(
        "custom_components.meraki_ha.core.api.factory.create_api_client"
    ) as mock_create:
        create_meraki_client(hass, entry)
        mock_create.assert_called_once_with(
            hass,
            "oauth-primary-token",
            "test-org",
            enabled_networks=[],
        )
