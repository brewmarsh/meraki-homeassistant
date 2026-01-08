"""Tests for the config flow module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.data_entry_flow import AbortFlow

from custom_components.meraki_ha.config_flow import MerakiConfigFlow
from custom_components.meraki_ha.const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DOMAIN,
)
from custom_components.meraki_ha.core.errors import (
    MerakiAuthenticationError,
    MerakiConnectionError,
)


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock hass instance."""
    hass = MagicMock()
    hass.data = {}
    return hass


def test_config_flow_initialization() -> None:
    """Test config flow initializes with empty data."""
    flow = MerakiConfigFlow()
    assert flow.data == {}
    assert flow.options == {}


@pytest.mark.asyncio
async def test_async_step_user_no_input(mock_hass: MagicMock) -> None:
    """Test step user shows form when no input."""
    flow = MerakiConfigFlow()
    flow.hass = mock_hass

    result = await flow.async_step_user(None)

    assert result["type"] == "form"
    assert result["step_id"] == "user"
    assert result["errors"] == {}


@pytest.mark.asyncio
async def test_async_step_user_invalid_auth(mock_hass: MagicMock) -> None:
    """Test step user shows auth error on invalid credentials."""
    flow = MerakiConfigFlow()
    flow.hass = mock_hass

    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        side_effect=MerakiAuthenticationError("Invalid API key"),
    ):
        result = await flow.async_step_user(
            {CONF_MERAKI_API_KEY: "invalid_key", CONF_MERAKI_ORG_ID: "123456"}
        )

    assert result["type"] == "form"
    errors = result.get("errors") or {}
    assert errors.get("base") == "invalid_auth"


@pytest.mark.asyncio
async def test_async_step_user_connection_error(mock_hass: MagicMock) -> None:
    """Test step user shows connection error."""
    flow = MerakiConfigFlow()
    flow.hass = mock_hass

    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        side_effect=MerakiConnectionError("Cannot connect"),
    ):
        result = await flow.async_step_user(
            {CONF_MERAKI_API_KEY: "test_key", CONF_MERAKI_ORG_ID: "123456"}
        )

    assert result["type"] == "form"
    errors = result.get("errors") or {}
    assert errors.get("base") == "cannot_connect"


@pytest.mark.asyncio
async def test_async_step_user_unknown_error(mock_hass: MagicMock) -> None:
    """Test step user shows unknown error on unexpected exception."""
    flow = MerakiConfigFlow()
    flow.hass = mock_hass

    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        side_effect=Exception("Unexpected error"),
    ):
        result = await flow.async_step_user(
            {CONF_MERAKI_API_KEY: "test_key", CONF_MERAKI_ORG_ID: "123456"}
        )

    assert result["type"] == "form"
    errors = result.get("errors") or {}
    assert errors.get("base") == "unknown"


@pytest.mark.asyncio
async def test_async_step_user_already_configured(mock_hass: MagicMock) -> None:
    """Test step user aborts if already configured."""
    flow = MerakiConfigFlow()
    flow.hass = mock_hass

    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        side_effect=AbortFlow("already_configured"),
    ):
        result = await flow.async_step_user(
            {CONF_MERAKI_API_KEY: "test_key", CONF_MERAKI_ORG_ID: "123456"}
        )

    assert result["type"] == "abort"
    assert result["reason"] == "already_configured"


@pytest.mark.asyncio
async def test_async_step_user_success(mock_hass: MagicMock) -> None:
    """Test step user succeeds with valid credentials."""
    flow = MerakiConfigFlow()
    flow.hass = mock_hass
    object.__setattr__(flow, "async_set_unique_id", AsyncMock())
    object.__setattr__(flow, "_abort_if_unique_id_configured", MagicMock())
    flow.async_show_form = MagicMock(return_value={"type": "form", "step_id": "init"})

    with patch(
        "custom_components.meraki_ha.config_flow.validate_meraki_credentials",
        return_value={"org_name": "Test Org"},
    ):
        await flow.async_step_user(
            {CONF_MERAKI_API_KEY: "valid_key", CONF_MERAKI_ORG_ID: "123456"}
        )

    assert flow.data[CONF_MERAKI_API_KEY] == "valid_key"
    assert flow.data[CONF_MERAKI_ORG_ID] == "123456"
    assert flow.data["org_name"] == "Test Org"


@pytest.mark.asyncio
async def test_async_step_init_no_input() -> None:
    """Test step init shows form when no input."""
    flow = MerakiConfigFlow()
    flow.async_show_form = MagicMock(return_value={"type": "form", "step_id": "init"})

    result = await flow.async_step_init(None)

    assert result["type"] == "form"
    assert result["step_id"] == "init"


@pytest.mark.asyncio
async def test_async_step_init_creates_entry() -> None:
    """Test step init creates entry with valid input."""
    flow = MerakiConfigFlow()
    flow.data = {"org_name": "Test Org", CONF_MERAKI_API_KEY: "key"}
    flow.options = {}
    flow.async_create_entry = MagicMock(
        return_value={"type": "create_entry", "title": "Test Org"}
    )

    _result = await flow.async_step_init({"scan_interval": 60})  # noqa: F841

    assert flow.options["scan_interval"] == 60
    flow.async_create_entry.assert_called_once()


def test_async_get_options_flow() -> None:
    """Test options flow is returned correctly."""
    mock_entry = MagicMock()
    mock_entry.options = {}

    options_flow = MerakiConfigFlow.async_get_options_flow(mock_entry)

    assert options_flow is not None


@pytest.mark.asyncio
async def test_async_step_reconfigure_no_entry(mock_hass: MagicMock) -> None:
    """Test reconfigure step aborts if entry not found."""
    flow = MerakiConfigFlow()
    flow.hass = mock_hass
    flow.hass.config_entries.async_get_entry = MagicMock(return_value=None)
    flow.context = {"entry_id": "test_entry"}
    flow.async_abort = MagicMock(return_value={"type": "abort"})

    _result = await flow.async_step_reconfigure(None)  # noqa: F841

    flow.async_abort.assert_called_once_with(reason="unknown_entry")


@pytest.mark.asyncio
async def test_async_step_reconfigure_with_input(mock_hass: MagicMock) -> None:
    """Test reconfigure step updates entry with input."""
    mock_entry = MagicMock()
    mock_entry.entry_id = "test_entry"
    mock_entry.options = {"scan_interval": 30}

    flow = MerakiConfigFlow()
    flow.hass = mock_hass
    flow.hass.config_entries.async_get_entry = MagicMock(return_value=mock_entry)
    flow.hass.config_entries.async_update_entry = MagicMock()
    flow.hass.config_entries.async_reload = AsyncMock()
    flow.context = {"entry_id": "test_entry"}
    flow.async_abort = MagicMock(
        return_value={"type": "abort", "reason": "reconfigure_successful"}
    )

    _result = await flow.async_step_reconfigure({"scan_interval": 60})  # noqa: F841

    flow.hass.config_entries.async_update_entry.assert_called_once()
    flow.async_abort.assert_called_with(reason="reconfigure_successful")


@pytest.mark.asyncio
async def test_async_step_reconfigure_shows_form(mock_hass: MagicMock) -> None:
    """Test reconfigure step shows form when no input."""
    mock_entry = MagicMock()
    mock_entry.entry_id = "test_entry"
    mock_entry.options = {"scan_interval": 30}

    flow = MerakiConfigFlow()
    flow.hass = mock_hass
    flow.hass.config_entries.async_get_entry = MagicMock(return_value=mock_entry)
    flow.context = {"entry_id": "test_entry"}
    flow.hass.data = {}
    flow.async_show_form = MagicMock(
        return_value={"type": "form", "step_id": "reconfigure"}
    )

    result = await flow.async_step_reconfigure(None)

    assert result["type"] == "form"
    assert result["step_id"] == "reconfigure"


@pytest.mark.asyncio
async def test_async_step_reconfigure_with_networks(mock_hass: MagicMock) -> None:
    """Test reconfigure step shows networks from coordinator."""
    mock_entry = MagicMock()
    mock_entry.entry_id = "test_entry"
    mock_entry.options = {}

    mock_coordinator = MagicMock()
    mock_coordinator.data = {
        "networks": [
            {"name": "Network 1", "id": "N_1"},
            {"name": "Network 2", "id": "N_2"},
        ]
    }

    flow = MerakiConfigFlow()
    flow.hass = mock_hass
    flow.hass.config_entries.async_get_entry = MagicMock(return_value=mock_entry)
    flow.context = {"entry_id": "test_entry"}
    flow.hass.data = {DOMAIN: {"test_entry": {"coordinator": mock_coordinator}}}
    flow.async_show_form = MagicMock(
        return_value={"type": "form", "step_id": "reconfigure"}
    )

    _result = await flow.async_step_reconfigure(None)  # noqa: F841

    flow.async_show_form.assert_called_once()
