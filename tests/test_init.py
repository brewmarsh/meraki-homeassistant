"""Tests for the main __init__.py module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.exceptions import ConfigEntryNotReady

from custom_components.meraki_ha import async_setup_entry, async_unload_entry
from custom_components.meraki_ha.const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DATA_CLIENT,
    DOMAIN,
)


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock hass instance."""
    hass = MagicMock()
    hass.data = {}
    hass.config_entries = MagicMock()
    hass.config_entries.async_forward_entry_setups = AsyncMock()
    hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)
    hass.states = MagicMock()
    return hass


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry"
    entry.data = {
        CONF_MERAKI_API_KEY: "test_api_key",
        CONF_MERAKI_ORG_ID: "test_org_id",
    }
    entry.options = {}
    entry.domain = DOMAIN
    return entry


@pytest.mark.asyncio
async def test_async_setup_entry_missing_api_key(
    mock_hass: MagicMock,
) -> None:
    """Test setup fails when API key is missing."""
    mock_entry = MagicMock()
    mock_entry.entry_id = "test_entry"
    mock_entry.data = {}  # Missing API key
    mock_entry.options = {}

    result = await async_setup_entry(mock_hass, mock_entry)

    assert result is False


@pytest.mark.asyncio
async def test_async_setup_entry_success(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test successful setup entry."""
    mock_api_client = MagicMock()
    mock_api_client.async_setup = AsyncMock()

    mock_coordinator = MagicMock()
    mock_coordinator.async_config_entry_first_refresh = AsyncMock()
    mock_coordinator.data = {"networks": [], "devices": []}

    with (
        patch(
            "custom_components.meraki_ha.MerakiAPIClient",
            return_value=mock_api_client,
        ),
        patch(
            "custom_components.meraki_ha.MerakiDataCoordinator",
            return_value=mock_coordinator,
        ),
        patch(
            "custom_components.meraki_ha.MerakiRepository",
        ),
        patch(
            "custom_components.meraki_ha.SwitchPortStatusCoordinator",
        ) as mock_switch_port_coord,
        patch(
            "custom_components.meraki_ha.CameraRepository",
        ),
        patch(
            "custom_components.meraki_ha.CameraService",
        ),
        patch(
            "custom_components.meraki_ha.DeviceControlService",
        ),
        patch(
            "custom_components.meraki_ha.NetworkControlService",
        ),
        patch(
            "custom_components.meraki_ha.DeviceDiscoveryService",
        ) as mock_discovery,
        patch(
            "custom_components.meraki_ha.async_setup_api",
        ),
        patch(
            "custom_components.meraki_ha.async_setup_websocket_api",
        ),
        patch(
            "custom_components.meraki_ha.async_register_static_path",
        ),
        patch(
            "custom_components.meraki_ha.async_register_panel",
        ),
        patch(
            "custom_components.meraki_ha.async_register_webhook",
        ),
    ):
        mock_discovery_instance = MagicMock()
        mock_discovery_instance.discover_entities = AsyncMock(return_value=[])
        mock_discovery.return_value = mock_discovery_instance

        # Configure switch port coordinator mock
        mock_spc_instance = MagicMock()
        mock_spc_instance.async_refresh = AsyncMock()
        mock_switch_port_coord.return_value = mock_spc_instance  # type: ignore[name-defined]

        result = await async_setup_entry(mock_hass, mock_config_entry)

    assert result is True
    assert DOMAIN in mock_hass.data
    assert mock_config_entry.entry_id in mock_hass.data[DOMAIN]


@pytest.mark.asyncio
async def test_async_setup_entry_coordinator_not_ready(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test setup raises ConfigEntryNotReady on coordinator failure."""
    mock_api_client = MagicMock()
    mock_api_client.async_setup = AsyncMock()

    mock_coordinator = MagicMock()
    mock_coordinator.async_config_entry_first_refresh = AsyncMock(
        side_effect=ConfigEntryNotReady("Failed to fetch data")
    )

    with (
        patch(
            "custom_components.meraki_ha.MerakiAPIClient",
            return_value=mock_api_client,
        ),
        patch(
            "custom_components.meraki_ha.MerakiDataCoordinator",
            return_value=mock_coordinator,
        ),
        pytest.raises(ConfigEntryNotReady),
    ):
        await async_setup_entry(mock_hass, mock_config_entry)


@pytest.mark.asyncio
async def test_async_setup_entry_existing_coordinator(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test setup entry uses existing coordinator if present."""
    mock_api_client = MagicMock()
    mock_api_client.async_setup = AsyncMock()

    mock_coordinator = MagicMock()
    mock_coordinator.async_refresh = AsyncMock()
    mock_coordinator.data = {"networks": [], "devices": []}

    # Pre-populate entry data
    mock_hass.data = {
        DOMAIN: {
            mock_config_entry.entry_id: {
                DATA_CLIENT: mock_api_client,
                "coordinator": mock_coordinator,
            }
        }
    }

    with (
        patch(
            "custom_components.meraki_ha.MerakiRepository",
        ),
        patch(
            "custom_components.meraki_ha.SwitchPortStatusCoordinator",
        ) as mock_switch_port_coord,
        patch(
            "custom_components.meraki_ha.CameraRepository",
        ),
        patch(
            "custom_components.meraki_ha.CameraService",
        ),
        patch(
            "custom_components.meraki_ha.DeviceControlService",
        ),
        patch(
            "custom_components.meraki_ha.NetworkControlService",
        ),
        patch(
            "custom_components.meraki_ha.DeviceDiscoveryService",
        ) as mock_discovery,
        patch(
            "custom_components.meraki_ha.async_setup_api",
        ),
        patch(
            "custom_components.meraki_ha.async_setup_websocket_api",
        ),
        patch(
            "custom_components.meraki_ha.async_register_static_path",
        ),
        patch(
            "custom_components.meraki_ha.async_register_panel",
        ),
        patch(
            "custom_components.meraki_ha.async_register_webhook",
        ),
    ):
        mock_discovery_instance = MagicMock()
        mock_discovery_instance.discover_entities = AsyncMock(return_value=[])
        mock_discovery.return_value = mock_discovery_instance

        # Configure switch port coordinator mock
        mock_spc_instance = MagicMock()
        mock_spc_instance.async_refresh = AsyncMock()
        mock_switch_port_coord.return_value = mock_spc_instance

        result = await async_setup_entry(mock_hass, mock_config_entry)

    assert result is True
    mock_coordinator.async_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_async_unload_entry(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test unload entry."""
    mock_coordinator = MagicMock()
    mock_web_server = MagicMock()
    mock_web_server.stop = AsyncMock()

    mock_hass.data = {
        DOMAIN: {
            mock_config_entry.entry_id: {
                "coordinator": mock_coordinator,
                "web_server": mock_web_server,
                "timed_access_manager": MagicMock(),
            }
        }
    }

    with (
        patch(
            "custom_components.meraki_ha.async_unregister_webhook",
        ),
        patch(
            "custom_components.meraki_ha.async_unregister_frontend",
        ),
    ):
        result = await async_unload_entry(mock_hass, mock_config_entry)

    assert result is True
    mock_web_server.stop.assert_called_once()


@pytest.mark.asyncio
async def test_async_unload_entry_no_web_server(
    mock_hass: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test unload entry when no web server is present."""
    mock_coordinator = MagicMock()

    mock_hass.data = {
        DOMAIN: {
            mock_config_entry.entry_id: {
                "coordinator": mock_coordinator,
            }
        }
    }

    with (
        patch(
            "custom_components.meraki_ha.async_unregister_webhook",
        ),
        patch(
            "custom_components.meraki_ha.async_unregister_frontend",
        ),
    ):
        result = await async_unload_entry(mock_hass, mock_config_entry)

    assert result is True

