"""Tests for the Meraki camera module."""

from typing import cast
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.components.camera import CameraEntityFeature
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.camera import (
    MerakiCamera,
    _load_camera_mappings,
    async_setup_entry,
)
from custom_components.meraki_ha.const import (
    CONF_CAMERA_SNAPSHOT_INTERVAL,
    DEFAULT_CAMERA_SNAPSHOT_INTERVAL,
    DOMAIN,
)
from custom_components.meraki_ha.types import MerakiDevice

MOCK_CAMERA_DEVICE = cast(
    MerakiDevice,
    {
        "serial": "CAM-1234-ABCD",
        "name": "Test Camera",
        "model": "MV12W",
        "networkId": "N_12345",
        "productType": "camera",
        "lanIp": "192.168.1.100",
        "status": "online",
        "rtsp_url": "rtsp://192.168.1.100/stream",
        "video_settings": {"rtspServerEnabled": True},
        "cloud_video_url": "https://example.meraki.com/video",
    },
)


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [MOCK_CAMERA_DEVICE],
        "networks": [{"id": "N_12345", "name": "Test Network"}],
    }
    coordinator.last_update_success = True
    coordinator.get_device = MagicMock(return_value=MOCK_CAMERA_DEVICE)
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


@pytest.fixture
def mock_camera_service() -> AsyncMock:
    """Create a mock camera service."""
    service = AsyncMock()
    service.generate_snapshot = AsyncMock(
        return_value="https://snapshot.meraki.com/image.jpg"
    )
    service.async_set_rtsp_stream_enabled = AsyncMock()
    return service


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.options = {CONF_CAMERA_SNAPSHOT_INTERVAL: DEFAULT_CAMERA_SNAPSHOT_INTERVAL}
    return entry


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock Home Assistant instance."""
    hass = MagicMock(spec=HomeAssistant)
    hass.data = {DOMAIN: {"test_entry_id": {}}}
    hass.config = MagicMock()
    hass.config.path.return_value = "/tmp/.storage"
    hass.states = MagicMock()
    hass.states.get.return_value = None
    return hass


class TestAsyncSetupEntry:
    """Tests for async_setup_entry function."""

    @pytest.mark.asyncio
    async def test_setup_no_cameras(
        self, mock_hass: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test setup with no camera entities."""
        mock_hass.data[DOMAIN][mock_config_entry.entry_id] = {"entities": []}
        async_add_entities = MagicMock()

        await async_setup_entry(mock_hass, mock_config_entry, async_add_entities)

        async_add_entities.assert_not_called()

    @pytest.mark.asyncio
    async def test_setup_with_cameras(
        self,
        mock_hass: MagicMock,
        mock_config_entry: MagicMock,
        mock_coordinator: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test setup with camera entities."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )
        camera.hass = mock_hass

        mock_hass.data[DOMAIN][mock_config_entry.entry_id] = {"entities": [camera]}
        async_add_entities = MagicMock()

        await async_setup_entry(mock_hass, mock_config_entry, async_add_entities)

        async_add_entities.assert_called_once()
        assert len(async_add_entities.call_args[0][0]) == 1


class TestLoadCameraMappings:
    """Tests for _load_camera_mappings function."""

    @pytest.mark.asyncio
    async def test_load_mappings_file_not_exists(self, mock_hass: MagicMock) -> None:
        """Test loading mappings when file doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            result = await _load_camera_mappings(mock_hass)
            assert result == {}

    @pytest.mark.asyncio
    async def test_load_mappings_success(self, mock_hass: MagicMock) -> None:
        """Test loading mappings successfully."""
        mappings = {"entry_id": {"CAM-1234": "camera.other_camera"}}
        mock_file = AsyncMock()
        json_content = '{"entry_id": {"CAM-1234": "camera.other_camera"}}'
        mock_file.read = AsyncMock(return_value=json_content)
        mock_file.__aenter__ = AsyncMock(return_value=mock_file)
        mock_file.__aexit__ = AsyncMock(return_value=None)

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("aiofiles.open", return_value=mock_file),
        ):
            result = await _load_camera_mappings(mock_hass)
            assert result == mappings

    @pytest.mark.asyncio
    async def test_load_mappings_json_error(self, mock_hass: MagicMock) -> None:
        """Test loading mappings with JSON decode error."""
        mock_file = AsyncMock()
        mock_file.read = AsyncMock(return_value="invalid json")
        mock_file.__aenter__ = AsyncMock(return_value=mock_file)
        mock_file.__aexit__ = AsyncMock(return_value=None)

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("aiofiles.open", return_value=mock_file),
        ):
            result = await _load_camera_mappings(mock_hass)
            assert result == {}


class TestMerakiCamera:
    """Tests for MerakiCamera class."""

    def test_camera_initialization(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test camera initialization."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )

        assert camera._device_serial == MOCK_CAMERA_DEVICE["serial"]
        assert camera._attr_unique_id == f"{MOCK_CAMERA_DEVICE['serial']}-camera"
        assert camera._attr_brand == "Cisco Meraki"
        assert camera._attr_model == "MV12W"

    def test_device_data_property(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test device_data property."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )

        assert camera.device_data == MOCK_CAMERA_DEVICE
        mock_coordinator.get_device.assert_called_with(MOCK_CAMERA_DEVICE["serial"])

    def test_snapshot_interval_default(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test snapshot interval with default value."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )

        assert camera._snapshot_interval == DEFAULT_CAMERA_SNAPSHOT_INTERVAL

    def test_snapshot_interval_custom(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test snapshot interval with custom value."""
        config_entry = MagicMock()
        config_entry.options = {CONF_CAMERA_SNAPSHOT_INTERVAL: 30}
        camera = MerakiCamera(
            mock_coordinator, config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )

        assert camera._snapshot_interval == 30

    def test_device_info(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test device_info property."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )
        device_info = camera.device_info

        assert (DOMAIN, MOCK_CAMERA_DEVICE["serial"]) in device_info["identifiers"]
        assert device_info["model"] == "MV12W"
        assert device_info["manufacturer"] == "Cisco Meraki"

    def test_available_coordinator_failed(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test available when coordinator update failed."""
        mock_coordinator.last_update_success = False
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )

        assert camera.available is False

    def test_available_device_not_found(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test available when device not found."""
        mock_coordinator.get_device.return_value = None
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )

        assert camera.available is False

    def test_available_success(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test available when everything is good."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )

        assert camera.available is True

    def test_supported_features(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test supported_features property."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )

        assert camera.supported_features == CameraEntityFeature.STREAM

    def test_is_streaming_online_rtsp_enabled(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test is_streaming when camera is online and RTSP enabled."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )

        assert camera.is_streaming is True

    def test_is_streaming_offline(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test is_streaming when camera is offline."""
        offline_device = dict(MOCK_CAMERA_DEVICE)
        offline_device["status"] = "offline"
        mock_coordinator.get_device.return_value = offline_device

        camera = MerakiCamera(
            mock_coordinator,
            mock_config_entry,
            cast(MerakiDevice, offline_device),
            mock_camera_service,
        )

        assert camera.is_streaming is False

    def test_is_streaming_rtsp_disabled(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test is_streaming when RTSP is disabled."""
        device_no_rtsp = dict(MOCK_CAMERA_DEVICE)
        device_no_rtsp["video_settings"] = {"rtspServerEnabled": False}
        mock_coordinator.get_device.return_value = device_no_rtsp

        camera = MerakiCamera(
            mock_coordinator,
            mock_config_entry,
            cast(MerakiDevice, device_no_rtsp),
            mock_camera_service,
        )

        assert camera.is_streaming is False

    def test_extra_state_attributes_with_rtsp(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test extra_state_attributes with RTSP enabled."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )
        attrs = camera.extra_state_attributes

        assert attrs["snapshot_interval"] == DEFAULT_CAMERA_SNAPSHOT_INTERVAL
        assert attrs["stream_status"] == "RTSP Enabled"
        assert attrs["stream_source"] == "meraki_rtsp"
        assert "cloud_video_url" in attrs

    def test_extra_state_attributes_rtsp_disabled(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test extra_state_attributes with RTSP disabled."""
        device_no_rtsp = dict(MOCK_CAMERA_DEVICE)
        device_no_rtsp["video_settings"] = {"rtspServerEnabled": False}
        mock_coordinator.get_device.return_value = device_no_rtsp

        camera = MerakiCamera(
            mock_coordinator,
            mock_config_entry,
            cast(MerakiDevice, device_no_rtsp),
            mock_camera_service,
        )
        attrs = camera.extra_state_attributes

        assert attrs["stream_status"] == "RTSP Disabled in Dashboard"
        assert attrs["stream_source"] == "none"

    def test_extra_state_attributes_linked_camera(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
    ) -> None:
        """Test extra_state_attributes with linked camera."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )
        camera._cached_linked_entity = "camera.blue_iris_front_door"
        attrs = camera.extra_state_attributes

        assert "Linked to camera.blue_iris_front_door" in attrs["stream_status"]
        assert attrs["linked_camera_entity"] == "camera.blue_iris_front_door"
        assert attrs["stream_source"] == "linked_camera"

    @pytest.mark.asyncio
    async def test_async_camera_image_offline(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
        mock_hass: MagicMock,
    ) -> None:
        """Test async_camera_image when camera is offline."""
        offline_device = dict(MOCK_CAMERA_DEVICE)
        offline_device["status"] = "offline"
        mock_coordinator.get_device.return_value = offline_device

        camera = MerakiCamera(
            mock_coordinator,
            mock_config_entry,
            cast(MerakiDevice, offline_device),
            mock_camera_service,
        )
        camera.hass = mock_hass

        # Mock the _get_linked_camera_entity to return None (no linked camera)
        with patch.object(
            camera,
            "_get_linked_camera_entity",
            new_callable=AsyncMock,
            return_value=None,
        ):
            result = await camera.async_camera_image()

        assert result is None
        mock_camera_service.generate_snapshot.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_camera_image_cached(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
        mock_hass: MagicMock,
    ) -> None:
        """Test async_camera_image returns cached image on error."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )
        camera.hass = mock_hass
        camera._cached_snapshot = b"cached_image"

        # Mock the _get_linked_camera_entity and _fetch_snapshot to avoid
        # creating real HTTP sessions that cause lingering timer issues
        with (
            patch.object(
                camera,
                "_get_linked_camera_entity",
                new_callable=AsyncMock,
                return_value=None,
            ),
            patch.object(
                camera,
                "_fetch_snapshot",
                new_callable=AsyncMock,
                side_effect=Exception("Simulated error"),
            ),
        ):
            result = await camera.async_camera_image()

        # Should return cached image on error
        assert result == b"cached_image"

    @pytest.mark.asyncio
    async def test_stream_source_rtsp(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
        mock_hass: MagicMock,
    ) -> None:
        """Test stream_source returns RTSP URL."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )
        camera.hass = mock_hass

        # Mock the _get_linked_camera_entity to return None (no linked camera)
        with patch.object(
            camera,
            "_get_linked_camera_entity",
            new_callable=AsyncMock,
            return_value=None,
        ):
            result = await camera.stream_source()

        assert result == "rtsp://192.168.1.100/stream"

    @pytest.mark.asyncio
    async def test_stream_source_not_streaming(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
        mock_hass: MagicMock,
    ) -> None:
        """Test stream_source when not streaming."""
        device_no_rtsp = dict(MOCK_CAMERA_DEVICE)
        device_no_rtsp["video_settings"] = {"rtspServerEnabled": False}
        mock_coordinator.get_device.return_value = device_no_rtsp

        camera = MerakiCamera(
            mock_coordinator,
            mock_config_entry,
            cast(MerakiDevice, device_no_rtsp),
            mock_camera_service,
        )
        camera.hass = mock_hass

        # Mock the _get_linked_camera_entity to return None (no linked camera)
        with patch.object(
            camera,
            "_get_linked_camera_entity",
            new_callable=AsyncMock,
            return_value=None,
        ):
            result = await camera.stream_source()

        assert result is None

    @pytest.mark.asyncio
    async def test_async_turn_on(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
        mock_hass: MagicMock,
    ) -> None:
        """Test async_turn_on enables RTSP."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )
        camera.hass = mock_hass

        await camera.async_turn_on()

        mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
            MOCK_CAMERA_DEVICE["serial"], True
        )
        mock_coordinator.async_request_refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_turn_off(
        self,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
        mock_camera_service: AsyncMock,
        mock_hass: MagicMock,
    ) -> None:
        """Test async_turn_off disables RTSP."""
        camera = MerakiCamera(
            mock_coordinator, mock_config_entry, MOCK_CAMERA_DEVICE, mock_camera_service
        )
        camera.hass = mock_hass

        await camera.async_turn_off()

        mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
            MOCK_CAMERA_DEVICE["serial"], False
        )
        mock_coordinator.async_request_refresh.assert_called_once()
