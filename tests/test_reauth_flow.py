"""Tests for the reauth flow module."""

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest
from homeassistant.exceptions import ConfigEntryAuthFailed

from custom_components.meraki_ha.const import CONF_MERAKI_API_KEY, CONF_MERAKI_ORG_ID
from custom_components.meraki_ha.reauth_flow import async_step_reauth


@pytest.fixture
def mock_config_flow() -> MagicMock:
    """Create a mock config flow instance."""
    flow = MagicMock()
    flow.hass = MagicMock()
    flow.context = {"entry_id": "test_entry"}
    flow.async_abort = MagicMock(return_value={"type": "abort", "reason": "unknown"})
    flow.async_show_form = MagicMock(return_value={"type": "form", "step_id": "reauth"})
    return flow


@pytest.fixture
def mock_existing_entry() -> MagicMock:
    """Create a mock existing config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry"
    entry.data = {
        CONF_MERAKI_API_KEY: "old_key",
        CONF_MERAKI_ORG_ID: "123456",
    }
    return entry


@pytest.mark.asyncio
async def test_reauth_no_existing_entry(mock_config_flow: MagicMock) -> None:
    """Test reauth aborts when entry not found."""
    mock_config_flow.hass.config_entries.async_get_entry = MagicMock(return_value=None)

    _result = await async_step_reauth(mock_config_flow, None)  # noqa: F841

    mock_config_flow.async_abort.assert_called_once_with(reason="unknown_entry")


@pytest.mark.asyncio
async def test_reauth_shows_form_no_input(
    mock_config_flow: MagicMock,
    mock_existing_entry: MagicMock,
) -> None:
    """Test reauth shows form when no input provided."""
    mock_config_flow.hass.config_entries.async_get_entry = MagicMock(
        return_value=mock_existing_entry
    )

    result = await async_step_reauth(mock_config_flow, None)

    mock_config_flow.async_show_form.assert_called_once()
    assert result["type"] == "form"
    assert result["step_id"] == "reauth"


@pytest.mark.asyncio
async def test_reauth_success(
    mock_config_flow: MagicMock,
    mock_existing_entry: MagicMock,
) -> None:
    """Test successful reauthentication."""
    mock_config_flow.hass.config_entries.async_get_entry = MagicMock(
        return_value=mock_existing_entry
    )
    mock_config_flow.hass.config_entries.async_update_entry = MagicMock()
    mock_config_flow.hass.config_entries.async_reload = AsyncMock()
    mock_config_flow.async_abort = MagicMock(
        return_value={"type": "abort", "reason": "reauth_successful"}
    )

    with patch(
        "custom_components.meraki_ha.reauth_flow.validate_meraki_credentials",
        return_value={"org_name": "Test Org"},
    ):
        _result = await async_step_reauth(  # noqa: F841
            mock_config_flow,
            {CONF_MERAKI_API_KEY: "new_key", CONF_MERAKI_ORG_ID: "123456"},
        )

    mock_config_flow.hass.config_entries.async_update_entry.assert_called_once()
    mock_config_flow.async_abort.assert_called_with(reason="reauth_successful")


@pytest.mark.asyncio
async def test_reauth_invalid_auth(
    mock_config_flow: MagicMock,
    mock_existing_entry: MagicMock,
) -> None:
    """Test reauth with invalid credentials."""
    mock_config_flow.hass.config_entries.async_get_entry = MagicMock(
        return_value=mock_existing_entry
    )

    with patch(
        "custom_components.meraki_ha.reauth_flow.validate_meraki_credentials",
        side_effect=ConfigEntryAuthFailed("Invalid"),
    ):
        _result = await async_step_reauth(  # noqa: F841
            mock_config_flow,
            {CONF_MERAKI_API_KEY: "bad_key", CONF_MERAKI_ORG_ID: "123456"},
        )

    mock_config_flow.async_show_form.assert_called_once()


@pytest.mark.asyncio
async def test_reauth_invalid_org_id(
    mock_config_flow: MagicMock,
    mock_existing_entry: MagicMock,
) -> None:
    """Test reauth with invalid org ID."""
    mock_config_flow.hass.config_entries.async_get_entry = MagicMock(
        return_value=mock_existing_entry
    )

    with patch(
        "custom_components.meraki_ha.reauth_flow.validate_meraki_credentials",
        side_effect=ValueError("Invalid org ID"),
    ):
        _result = await async_step_reauth(  # noqa: F841
            mock_config_flow,
            {CONF_MERAKI_API_KEY: "key", CONF_MERAKI_ORG_ID: "invalid"},
        )

    mock_config_flow.async_show_form.assert_called_once()


@pytest.mark.asyncio
async def test_reauth_connection_error(
    mock_config_flow: MagicMock,
    mock_existing_entry: MagicMock,
) -> None:
    """Test reauth with connection error."""
    mock_config_flow.hass.config_entries.async_get_entry = MagicMock(
        return_value=mock_existing_entry
    )

    with patch(
        "custom_components.meraki_ha.reauth_flow.validate_meraki_credentials",
        side_effect=aiohttp.ClientError("Connection failed"),
    ):
        _result = await async_step_reauth(  # noqa: F841
            mock_config_flow,
            {CONF_MERAKI_API_KEY: "key", CONF_MERAKI_ORG_ID: "123456"},
        )

    mock_config_flow.async_show_form.assert_called_once()


@pytest.mark.asyncio
async def test_reauth_unknown_error(
    mock_config_flow: MagicMock,
    mock_existing_entry: MagicMock,
) -> None:
    """Test reauth with unknown error."""
    mock_config_flow.hass.config_entries.async_get_entry = MagicMock(
        return_value=mock_existing_entry
    )

    with patch(
        "custom_components.meraki_ha.reauth_flow.validate_meraki_credentials",
        side_effect=Exception("Unexpected error"),
    ):
        _result = await async_step_reauth(  # noqa: F841
            mock_config_flow,
            {CONF_MERAKI_API_KEY: "key", CONF_MERAKI_ORG_ID: "123456"},
        )

    mock_config_flow.async_show_form.assert_called_once()
