"""Tests for the Meraki Web UI API handlers."""

from __future__ import annotations

import json
from collections.abc import Callable, Coroutine
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.components.websocket_api import ActiveConnection
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import (
    CONF_CAMERA_ENTITY_MAPPINGS,
    CONF_ENABLED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DATA_CLIENT,
    DOMAIN,
)
from custom_components.meraki_ha.web_api import (
    async_setup_api,
    handle_create_timed_access_key,
    handle_get_available_cameras,
    handle_get_camera_mappings,
    handle_get_camera_snapshot,
    handle_get_camera_stream_url,
    handle_get_config,
    handle_set_camera_mapping,
    handle_update_enabled_networks,
)

from .const import MOCK_ALL_DATA

# Type alias for websocket handler functions
WebSocketHandler = Callable[
    [HomeAssistant, ActiveConnection, dict[str, Any]],
    Coroutine[Any, Any, None],
]


def get_wrapped(
    func: Callable[[HomeAssistant, ActiveConnection, dict[str, Any]], None],
) -> WebSocketHandler:
    """Get the wrapped async function from a websocket handler.

    The @websocket_api.async_response decorator wraps the function,
    and we need to access __wrapped__ to call the underlying coroutine directly.
    """
    return func.__wrapped__  # type: ignore[attr-defined]


@pytest.fixture
def mock_config_entry_with_options() -> MockConfigEntry:
    """Fixture for a mock config entry with options."""
    return MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry_id",
        data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
        options={
            CONF_ENABLED_NETWORKS: ["N_12345"],
            CONF_CAMERA_ENTITY_MAPPINGS: {"Q234-CAM1": "camera.blue_iris_front"},
        },
    )


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.data = MOCK_ALL_DATA
    return coordinator


@pytest.fixture
def mock_camera_service() -> MagicMock:
    """Fixture for a mocked CameraService."""
    service = MagicMock()
    service.get_video_stream_url = AsyncMock(return_value="https://stream.url/video")
    service.get_cloud_video_url = AsyncMock(return_value="https://cloud.url/video")
    service.get_rtsp_stream_url = AsyncMock(
        return_value="rtsp://192.168.1.100:9000/live"
    )
    service.get_camera_snapshot = AsyncMock(return_value="https://snapshot.url/image")
    return service


@pytest.fixture
def mock_api_client() -> MagicMock:
    """Fixture for a mocked API client."""
    return MagicMock()


@pytest.fixture
def mock_connection() -> MagicMock:
    """Fixture for a mocked WebSocket connection."""
    connection = MagicMock()
    connection.send_result = MagicMock()
    connection.send_error = MagicMock()
    return connection


@pytest.fixture
async def setup_hass_data(
    hass: HomeAssistant,
    mock_config_entry_with_options: MockConfigEntry,
    mock_coordinator: MagicMock,
    mock_camera_service: MagicMock,
    mock_api_client: MagicMock,
) -> None:
    """Set up hass.data with mocked integration data."""
    mock_config_entry_with_options.add_to_hass(hass)
    hass.data[DOMAIN] = {
        "test_entry_id": {
            "coordinator": mock_coordinator,
            "camera_service": mock_camera_service,
            DATA_CLIENT: mock_api_client,
        }
    }


class TestAsyncSetupApi:
    """Tests for async_setup_api."""

    async def test_async_setup_api_registers_commands(
        self, hass: HomeAssistant
    ) -> None:
        """Test that async_setup_api registers all WebSocket commands."""
        with patch(
            "custom_components.meraki_ha.web_api.websocket_api.async_register_command"
        ) as mock_register:
            async_setup_api(hass)

            # Verify all 8 commands are registered
            assert mock_register.call_count == 8

            # Extract registered command names
            command_names = [call[0][1] for call in mock_register.call_args_list]
            assert "meraki_ha/get_config" in command_names
            assert "meraki_ha/get_camera_stream_url" in command_names
            assert "meraki_ha/get_camera_snapshot" in command_names
            assert "meraki_ha/update_enabled_networks" in command_names
            assert "meraki_ha/create_timed_access_key" in command_names
            assert "meraki_ha/get_camera_mappings" in command_names
            assert "meraki_ha/set_camera_mapping" in command_names
            assert "meraki_ha/get_available_cameras" in command_names


class TestHandleGetConfig:
    """Tests for handle_get_config handler."""

    async def test_get_config_success(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry_with_options: MockConfigEntry,
    ) -> None:
        """Test successful get_config request."""
        mock_config_entry_with_options.add_to_hass(hass)
        hass.data[DOMAIN] = {
            "test_entry_id": {
                "coordinator": mock_coordinator,
            }
        }

        msg = {
            "id": 1,
            "type": "meraki_ha/get_config",
            "config_entry_id": "test_entry_id",
        }

        # Mock the manifest file reading
        mock_manifest = json.dumps({"version": "1.0.0"})
        with patch("aiofiles.open", create=True) as mock_aiofiles_open:
            mock_file = AsyncMock()
            mock_file.read = AsyncMock(return_value=mock_manifest)
            mock_file.__aenter__ = AsyncMock(return_value=mock_file)
            mock_file.__aexit__ = AsyncMock(return_value=None)
            mock_aiofiles_open.return_value = mock_file

            # Call the underlying async function via __wrapped__
            await get_wrapped(handle_get_config)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once()
        result = mock_connection.send_result.call_args[0][1]
        assert result["config_entry_id"] == "test_entry_id"
        assert result["enabled_networks"] == ["N_12345"]
        assert result["version"] == "1.0.0"

    async def test_get_config_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test get_config when config entry is not found."""
        hass.data[DOMAIN] = {}

        msg = {
            "id": 1,
            "type": "meraki_ha/get_config",
            "config_entry_id": "nonexistent_entry",
        }

        await get_wrapped(handle_get_config)(hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "not_found", "Config entry not found"
        )

    async def test_get_config_default_enabled_networks(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test get_config uses default enabled networks when not configured."""
        # Create config entry without CONF_ENABLED_NETWORKS
        config_entry = MockConfigEntry(
            domain=DOMAIN,
            entry_id="test_entry_id",
            data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
            options={},  # No enabled_networks
        )
        config_entry.add_to_hass(hass)

        hass.data[DOMAIN] = {
            "test_entry_id": {
                "coordinator": mock_coordinator,
            }
        }

        msg = {
            "id": 1,
            "type": "meraki_ha/get_config",
            "config_entry_id": "test_entry_id",
        }

        mock_manifest = json.dumps({"version": "1.0.0"})
        with patch("aiofiles.open", create=True) as mock_aiofiles_open:
            mock_file = AsyncMock()
            mock_file.read = AsyncMock(return_value=mock_manifest)
            mock_file.__aenter__ = AsyncMock(return_value=mock_file)
            mock_file.__aexit__ = AsyncMock(return_value=None)
            mock_aiofiles_open.return_value = mock_file

            await get_wrapped(handle_get_config)(hass, mock_connection, msg)

        result = mock_connection.send_result.call_args[0][1]
        # Should default to all network IDs from coordinator data
        assert "N_12345" in result["enabled_networks"]

    async def test_get_config_entry_in_domain_but_not_config_entries(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test get_config when entry exists in domain data but not config_entries."""
        # Entry exists in hass.data[DOMAIN] but not in hass.config_entries
        hass.data[DOMAIN] = {
            "orphan_entry_id": {
                "coordinator": mock_coordinator,
            }
        }

        msg = {
            "id": 1,
            "type": "meraki_ha/get_config",
            "config_entry_id": "orphan_entry_id",
        }

        await get_wrapped(handle_get_config)(hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "not_found", "Config entry not found"
        )


class TestHandleGetCameraStreamUrl:
    """Tests for handle_get_camera_stream_url handler."""

    async def test_get_camera_stream_url_default(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        setup_hass_data: None,
    ) -> None:
        """Test get_camera_stream_url with default stream source."""
        msg = {
            "id": 1,
            "type": "meraki_ha/get_camera_stream_url",
            "config_entry_id": "test_entry_id",
            "serial": "Q234-CAM1",
        }

        await get_wrapped(handle_get_camera_stream_url)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once_with(
            1, {"url": "https://stream.url/video"}
        )

    async def test_get_camera_stream_url_cloud(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        setup_hass_data: None,
    ) -> None:
        """Test get_camera_stream_url with cloud stream source."""
        msg = {
            "id": 1,
            "type": "meraki_ha/get_camera_stream_url",
            "config_entry_id": "test_entry_id",
            "serial": "Q234-CAM1",
            "stream_source": "cloud",
        }

        await get_wrapped(handle_get_camera_stream_url)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once_with(
            1, {"url": "https://cloud.url/video"}
        )

    async def test_get_camera_stream_url_rtsp(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        setup_hass_data: None,
    ) -> None:
        """Test get_camera_stream_url with RTSP stream source."""
        msg = {
            "id": 1,
            "type": "meraki_ha/get_camera_stream_url",
            "config_entry_id": "test_entry_id",
            "serial": "Q234-CAM1",
            "stream_source": "rtsp",
        }

        await get_wrapped(handle_get_camera_stream_url)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once_with(
            1, {"url": "rtsp://192.168.1.100:9000/live"}
        )

    async def test_get_camera_stream_url_not_found(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test get_camera_stream_url when config entry not found."""
        hass.data[DOMAIN] = {}

        msg = {
            "id": 1,
            "type": "meraki_ha/get_camera_stream_url",
            "config_entry_id": "nonexistent",
            "serial": "Q234-CAM1",
        }

        await get_wrapped(handle_get_camera_stream_url)(hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "not_found", "Config entry not found"
        )


class TestHandleGetCameraSnapshot:
    """Tests for handle_get_camera_snapshot handler."""

    async def test_get_camera_snapshot_success(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        setup_hass_data: None,
    ) -> None:
        """Test successful camera snapshot request."""
        msg = {
            "id": 1,
            "type": "meraki_ha/get_camera_snapshot",
            "config_entry_id": "test_entry_id",
            "serial": "Q234-CAM1",
        }

        await get_wrapped(handle_get_camera_snapshot)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once_with(
            1, {"url": "https://snapshot.url/image"}
        )

    async def test_get_camera_snapshot_not_found(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test camera snapshot when config entry not found."""
        hass.data[DOMAIN] = {}

        msg = {
            "id": 1,
            "type": "meraki_ha/get_camera_snapshot",
            "config_entry_id": "nonexistent",
            "serial": "Q234-CAM1",
        }

        await get_wrapped(handle_get_camera_snapshot)(hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "not_found", "Config entry not found"
        )


class TestHandleUpdateEnabledNetworks:
    """Tests for handle_update_enabled_networks handler."""

    async def test_update_enabled_networks_success(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        mock_config_entry_with_options: MockConfigEntry,
    ) -> None:
        """Test successful update of enabled networks."""
        mock_config_entry_with_options.add_to_hass(hass)
        hass.data[DOMAIN] = {"test_entry_id": {}}

        msg = {
            "id": 1,
            "type": "meraki_ha/update_enabled_networks",
            "config_entry_id": "test_entry_id",
            "enabled_networks": ["N_12345", "N_67890"],
        }

        await get_wrapped(handle_update_enabled_networks)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once_with(1, {"success": True})

        # Verify the config entry was updated
        updated_entry = hass.config_entries.async_get_entry("test_entry_id")
        assert updated_entry.options[CONF_ENABLED_NETWORKS] == ["N_12345", "N_67890"]

    async def test_update_enabled_networks_domain_not_found(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test update when config entry not in domain data."""
        hass.data[DOMAIN] = {}

        msg = {
            "id": 1,
            "type": "meraki_ha/update_enabled_networks",
            "config_entry_id": "nonexistent",
            "enabled_networks": ["N_12345"],
        }

        await get_wrapped(handle_update_enabled_networks)(hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "not_found", "Config entry not found"
        )

    async def test_update_enabled_networks_entry_not_found(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test update when config entry doesn't exist in hass."""
        # Entry in domain data but not in config_entries
        hass.data[DOMAIN] = {"ghost_entry": {}}

        msg = {
            "id": 1,
            "type": "meraki_ha/update_enabled_networks",
            "config_entry_id": "ghost_entry",
            "enabled_networks": ["N_12345"],
        }

        await get_wrapped(handle_update_enabled_networks)(hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "not_found", "Config entry not found"
        )


class TestHandleCreateTimedAccessKey:
    """Tests for handle_create_timed_access_key handler."""

    async def test_create_timed_access_key_success(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        setup_hass_data: None,
    ) -> None:
        """Test successful timed access key creation."""
        msg = {
            "id": 1,
            "type": "meraki_ha/create_timed_access_key",
            "config_entry_id": "test_entry_id",
            "network_id": "N_12345",
            "ssid_number": "0",
            "name": "Guest Key",
            "passphrase": "test_passphrase",
            "duration_hours": 24,
            "group_policy_id": "101",
        }

        with patch(
            "custom_components.meraki_ha.web_api.TimedAccessManager"
        ) as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.create_timed_access_key = AsyncMock(
                return_value={"id": "key123", "name": "Guest Key"}
            )
            mock_manager_class.return_value = mock_manager

            handler = get_wrapped(handle_create_timed_access_key)
            await handler(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once_with(
            1, {"id": "key123", "name": "Guest Key"}
        )

    async def test_create_timed_access_key_not_found(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test timed access key creation when entry not found."""
        hass.data[DOMAIN] = {}

        msg = {
            "id": 1,
            "type": "meraki_ha/create_timed_access_key",
            "config_entry_id": "nonexistent",
            "network_id": "N_12345",
            "ssid_number": "0",
            "name": "Guest Key",
            "passphrase": "test_passphrase",
            "duration_hours": 24,
        }

        await get_wrapped(handle_create_timed_access_key)(hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "not_found", "Config entry not found"
        )

    async def test_create_timed_access_key_invalid_input(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        setup_hass_data: None,
    ) -> None:
        """Test timed access key creation with invalid input."""
        msg = {
            "id": 1,
            "type": "meraki_ha/create_timed_access_key",
            "config_entry_id": "test_entry_id",
            "network_id": "N_12345",
            "ssid_number": "0",
            "name": "Guest Key",
            "passphrase": "test_passphrase",
            "duration_hours": 24,
        }

        with patch(
            "custom_components.meraki_ha.web_api.TimedAccessManager"
        ) as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.create_timed_access_key = AsyncMock(
                side_effect=ValueError("Invalid passphrase")
            )
            mock_manager_class.return_value = mock_manager

            handler = get_wrapped(handle_create_timed_access_key)
            await handler(hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "invalid_input", "Invalid passphrase"
        )

    async def test_create_timed_access_key_api_error(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        setup_hass_data: None,
    ) -> None:
        """Test timed access key creation with API error."""
        from custom_components.meraki_ha.core.errors import MerakiError

        msg = {
            "id": 1,
            "type": "meraki_ha/create_timed_access_key",
            "config_entry_id": "test_entry_id",
            "network_id": "N_12345",
            "ssid_number": "0",
            "name": "Guest Key",
            "passphrase": "test_passphrase",
            "duration_hours": 24,
        }

        with patch(
            "custom_components.meraki_ha.web_api.TimedAccessManager"
        ) as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.create_timed_access_key = AsyncMock(
                side_effect=MerakiError("API rate limit exceeded")
            )
            mock_manager_class.return_value = mock_manager

            handler = get_wrapped(handle_create_timed_access_key)
            await handler(hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "api_error", "API rate limit exceeded"
        )


class TestHandleGetCameraMappings:
    """Tests for handle_get_camera_mappings handler."""

    async def test_get_camera_mappings_success(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        mock_config_entry_with_options: MockConfigEntry,
    ) -> None:
        """Test successful get camera mappings."""
        mock_config_entry_with_options.add_to_hass(hass)

        msg = {
            "id": 1,
            "type": "meraki_ha/get_camera_mappings",
            "config_entry_id": "test_entry_id",
        }

        await get_wrapped(handle_get_camera_mappings)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once_with(
            1, {"mappings": {"Q234-CAM1": "camera.blue_iris_front"}}
        )

    async def test_get_camera_mappings_empty(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test get camera mappings when none configured."""
        config_entry = MockConfigEntry(
            domain=DOMAIN,
            entry_id="test_entry_id",
            data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
            options={},  # No mappings
        )
        config_entry.add_to_hass(hass)

        msg = {
            "id": 1,
            "type": "meraki_ha/get_camera_mappings",
            "config_entry_id": "test_entry_id",
        }

        await get_wrapped(handle_get_camera_mappings)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once_with(1, {"mappings": {}})

    async def test_get_camera_mappings_not_found(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test get camera mappings when entry not found."""
        msg = {
            "id": 1,
            "type": "meraki_ha/get_camera_mappings",
            "config_entry_id": "nonexistent",
        }

        await get_wrapped(handle_get_camera_mappings)(hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "not_found", "Config entry not found"
        )


class TestHandleSetCameraMapping:
    """Tests for handle_set_camera_mapping handler."""

    async def test_set_camera_mapping_add(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        mock_config_entry_with_options: MockConfigEntry,
    ) -> None:
        """Test adding a new camera mapping."""
        mock_config_entry_with_options.add_to_hass(hass)

        msg = {
            "id": 1,
            "type": "meraki_ha/set_camera_mapping",
            "config_entry_id": "test_entry_id",
            "serial": "Q234-CAM2",
            "linked_entity_id": "camera.blue_iris_back",
        }

        await get_wrapped(handle_set_camera_mapping)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once()
        result = mock_connection.send_result.call_args[0][1]
        assert result["success"] is True
        assert result["mappings"]["Q234-CAM2"] == "camera.blue_iris_back"
        # Original mapping should still exist
        assert result["mappings"]["Q234-CAM1"] == "camera.blue_iris_front"

    async def test_set_camera_mapping_remove(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
        mock_config_entry_with_options: MockConfigEntry,
    ) -> None:
        """Test removing a camera mapping."""
        mock_config_entry_with_options.add_to_hass(hass)

        msg = {
            "id": 1,
            "type": "meraki_ha/set_camera_mapping",
            "config_entry_id": "test_entry_id",
            "serial": "Q234-CAM1",
            "linked_entity_id": "",  # Empty string removes mapping
        }

        await get_wrapped(handle_set_camera_mapping)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once()
        result = mock_connection.send_result.call_args[0][1]
        assert result["success"] is True
        assert "Q234-CAM1" not in result["mappings"]

    async def test_set_camera_mapping_not_found(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test set camera mapping when entry not found."""
        msg = {
            "id": 1,
            "type": "meraki_ha/set_camera_mapping",
            "config_entry_id": "nonexistent",
            "serial": "Q234-CAM1",
            "linked_entity_id": "camera.test",
        }

        await get_wrapped(handle_set_camera_mapping)(hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "not_found", "Config entry not found"
        )


class TestHandleGetAvailableCameras:
    """Tests for handle_get_available_cameras handler."""

    async def test_get_available_cameras_filters_meraki(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test that Meraki cameras are filtered out."""
        # Set up mock camera states
        hass.states.async_set(
            "camera.blue_iris_front",
            "idle",
            {"friendly_name": "Blue Iris Front"},
        )
        hass.states.async_set(
            "camera.meraki_front_door",
            "idle",
            {"friendly_name": "Meraki Front Door"},
        )
        hass.states.async_set(
            "camera.garage",
            "recording",
            {"friendly_name": "Garage Camera"},
        )

        msg = {
            "id": 1,
            "type": "meraki_ha/get_available_cameras",
        }

        await get_wrapped(handle_get_available_cameras)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once()
        result = mock_connection.send_result.call_args[0][1]
        cameras = result["cameras"]

        # Should only contain non-Meraki cameras
        entity_ids = [c["entity_id"] for c in cameras]
        assert "camera.blue_iris_front" in entity_ids
        assert "camera.garage" in entity_ids
        assert "camera.meraki_front_door" not in entity_ids

    async def test_get_available_cameras_sorted_by_name(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test that cameras are sorted by friendly name."""
        hass.states.async_set(
            "camera.zebra",
            "idle",
            {"friendly_name": "Zebra Camera"},
        )
        hass.states.async_set(
            "camera.alpha",
            "idle",
            {"friendly_name": "Alpha Camera"},
        )

        msg = {
            "id": 1,
            "type": "meraki_ha/get_available_cameras",
        }

        await get_wrapped(handle_get_available_cameras)(hass, mock_connection, msg)

        result = mock_connection.send_result.call_args[0][1]
        cameras = result["cameras"]

        # Should be sorted alphabetically by friendly name
        assert cameras[0]["friendly_name"] == "Alpha Camera"
        assert cameras[1]["friendly_name"] == "Zebra Camera"

    async def test_get_available_cameras_empty(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test when no cameras are available."""
        msg = {
            "id": 1,
            "type": "meraki_ha/get_available_cameras",
        }

        await get_wrapped(handle_get_available_cameras)(hass, mock_connection, msg)

        mock_connection.send_result.assert_called_once_with(1, {"cameras": []})

    async def test_get_available_cameras_includes_state(
        self,
        hass: HomeAssistant,
        mock_connection: MagicMock,
    ) -> None:
        """Test that camera state is included in response."""
        hass.states.async_set(
            "camera.test_cam",
            "recording",
            {"friendly_name": "Test Cam"},
        )

        msg = {
            "id": 1,
            "type": "meraki_ha/get_available_cameras",
        }

        await get_wrapped(handle_get_available_cameras)(hass, mock_connection, msg)

        result = mock_connection.send_result.call_args[0][1]
        cameras = result["cameras"]
        assert cameras[0]["state"] == "recording"
