"""Tests for the camera repository module."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from meraki.exceptions import AsyncAPIError

from custom_components.meraki_ha.core.errors import MerakiInformationalError
from custom_components.meraki_ha.core.repositories.camera_repository import (
    CameraRepository,
)


@pytest.fixture
def mock_api_client() -> MagicMock:
    """Create a mock API client."""
    client = MagicMock()
    client.organization = MagicMock()
    client.organization.get_organization_devices = AsyncMock(return_value=[])
    client.camera = MagicMock()
    client.camera.get_device_camera_analytics_recent = AsyncMock(return_value=[])
    client.camera.get_device_camera_video_link = AsyncMock(return_value={})
    client.camera.generate_device_camera_snapshot = AsyncMock(return_value={})
    client.camera.update_camera_video_settings = AsyncMock()
    client.devices = MagicMock()
    client.devices.get_device = AsyncMock(return_value={})
    client.network = MagicMock()
    client.network.get_network_camera_analytics_history = AsyncMock(return_value=[])
    return client


class TestCameraRepository:
    """Tests for CameraRepository class."""

    def test_initialization(self, mock_api_client: MagicMock) -> None:
        """Test camera repository initialization."""
        repo = CameraRepository(mock_api_client, "org_123")

        assert repo._api_client is mock_api_client
        assert repo._organization_id == "org_123"

    @pytest.mark.asyncio
    async def test_get_camera_features_device_not_found(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test get_camera_features when device is not found."""
        mock_api_client.organization.get_organization_devices.return_value = []
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.get_camera_features("CAM-1234")

        assert result == []

    @pytest.mark.asyncio
    async def test_get_camera_features_basic_camera(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test get_camera_features for basic camera model."""
        mock_api_client.organization.get_organization_devices.return_value = [
            {"serial": "CAM-1234", "model": "MV32"}
        ]
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.get_camera_features("CAM-1234")

        assert "video_stream" in result
        assert "person_detection" not in result
        assert "vehicle_detection" not in result

    @pytest.mark.asyncio
    async def test_get_camera_features_mv12_camera(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test get_camera_features for MV12 camera."""
        mock_api_client.organization.get_organization_devices.return_value = [
            {"serial": "CAM-1234", "model": "MV12W"}
        ]
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.get_camera_features("CAM-1234")

        assert "video_stream" in result
        assert "person_detection" in result
        assert "vehicle_detection" in result

    @pytest.mark.asyncio
    async def test_get_camera_features_mv22_camera(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test get_camera_features for MV22 camera."""
        mock_api_client.organization.get_organization_devices.return_value = [
            {"serial": "CAM-1234", "model": "MV22X"}
        ]
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.get_camera_features("CAM-1234")

        assert "person_detection" in result
        assert "vehicle_detection" in result

    @pytest.mark.asyncio
    async def test_get_analytics_data_success(self, mock_api_client: MagicMock) -> None:
        """Test get_analytics_data success."""
        analytics = [{"timestamp": "2024-01-01", "count": 5}]
        mock_api_client.camera.get_device_camera_analytics_recent.return_value = (
            analytics
        )
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.get_analytics_data("CAM-1234", "person")

        assert result == analytics
        mock_api_client.camera.get_device_camera_analytics_recent.assert_called_once_with(
            "CAM-1234", "person"
        )

    @pytest.mark.asyncio
    async def test_get_analytics_data_error(self, mock_api_client: MagicMock) -> None:
        """Test get_analytics_data handles errors."""
        mock_api_client.camera.get_device_camera_analytics_recent.side_effect = (
            AsyncAPIError(MagicMock(), MagicMock(), "API Error")
        )
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.get_analytics_data("CAM-1234", "person")

        assert result is None

    @pytest.mark.asyncio
    async def test_async_get_cloud_video_url_https(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test async_get_cloud_video_url returns HTTPS URL."""
        mock_api_client.camera.get_device_camera_video_link.return_value = {
            "url": "https://cloud.meraki.com/video/xyz"
        }
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.async_get_cloud_video_url("CAM-1234")

        assert result == "https://cloud.meraki.com/video/xyz"

    @pytest.mark.asyncio
    async def test_async_get_cloud_video_url_http(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test async_get_cloud_video_url accepts HTTP URL."""
        mock_api_client.camera.get_device_camera_video_link.return_value = {
            "url": "http://cloud.meraki.com/video/xyz"
        }
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.async_get_cloud_video_url("CAM-1234")

        assert result == "http://cloud.meraki.com/video/xyz"

    @pytest.mark.asyncio
    async def test_async_get_cloud_video_url_invalid_url(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test async_get_cloud_video_url returns None for invalid URL."""
        mock_api_client.camera.get_device_camera_video_link.return_value = {
            "url": "rtsp://192.168.1.100/stream"
        }
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.async_get_cloud_video_url("CAM-1234")

        assert result is None

    @pytest.mark.asyncio
    async def test_async_get_cloud_video_url_no_url(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test async_get_cloud_video_url returns None when no URL."""
        mock_api_client.camera.get_device_camera_video_link.return_value = {}
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.async_get_cloud_video_url("CAM-1234")

        assert result is None

    @pytest.mark.asyncio
    async def test_async_get_cloud_video_url_informational_error(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test async_get_cloud_video_url handles informational error."""
        mock_api_client.camera.get_device_camera_video_link.side_effect = (
            MerakiInformationalError("Not supported")
        )
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.async_get_cloud_video_url("CAM-1234")

        assert result is None

    @pytest.mark.asyncio
    async def test_async_get_cloud_video_url_generic_error(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test async_get_cloud_video_url handles API error."""
        mock_api_client.camera.get_device_camera_video_link.side_effect = AsyncAPIError(
            MagicMock(), MagicMock(), "API Error"
        )
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.async_get_cloud_video_url("CAM-1234")

        assert result is None

    @pytest.mark.asyncio
    async def test_async_get_rtsp_stream_url_success(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test async_get_rtsp_stream_url returns RTSP URL."""
        mock_api_client.devices.get_device.return_value = {
            "serial": "CAM-1234",
            "model": "MV12W",
        }
        mock_api_client.camera.get_device_camera_video_link.return_value = {
            "url": "rtsp://192.168.1.100/stream"
        }
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.async_get_rtsp_stream_url("CAM-1234")

        assert result == "rtsp://192.168.1.100/stream"

    @pytest.mark.asyncio
    async def test_async_get_rtsp_stream_url_mv2_camera(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test async_get_rtsp_stream_url returns None for MV2 cameras."""
        mock_api_client.devices.get_device.return_value = {
            "serial": "CAM-1234",
            "model": "MV2",
        }
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.async_get_rtsp_stream_url("CAM-1234")

        assert result is None
        mock_api_client.camera.get_device_camera_video_link.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_get_rtsp_stream_url_device_check_error(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test async_get_rtsp_stream_url returns None on device check error."""
        mock_api_client.devices.get_device.side_effect = AsyncAPIError(
            MagicMock(), MagicMock(), "Device error"
        )
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.async_get_rtsp_stream_url("CAM-1234")

        assert result is None

    @pytest.mark.asyncio
    async def test_async_get_rtsp_stream_url_non_rtsp_url(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test async_get_rtsp_stream_url returns None for non-RTSP URL."""
        mock_api_client.devices.get_device.return_value = {"model": "MV12W"}
        mock_api_client.camera.get_device_camera_video_link.return_value = {
            "url": "https://cloud.meraki.com/video"
        }
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.async_get_rtsp_stream_url("CAM-1234")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_analytics_history_success(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test get_analytics_history success."""
        history = [{"timestamp": "2024-01-01", "count": 10}]
        mock_api_client.network.get_network_camera_analytics_history.return_value = (
            history
        )
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.get_analytics_history("N_123", "person")

        assert result == history

    @pytest.mark.asyncio
    async def test_get_analytics_history_error(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test get_analytics_history handles errors."""
        mock_api_client.network.get_network_camera_analytics_history.side_effect = (
            AsyncAPIError(MagicMock(), MagicMock(), "API Error")
        )
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.get_analytics_history("N_123", "person")

        assert result == []

    @pytest.mark.asyncio
    async def test_generate_snapshot_success(self, mock_api_client: MagicMock) -> None:
        """Test generate_snapshot success."""
        mock_api_client.camera.generate_device_camera_snapshot.return_value = {
            "url": "https://snapshot.meraki.com/image.jpg"
        }
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.generate_snapshot("CAM-1234")

        assert result == "https://snapshot.meraki.com/image.jpg"

    @pytest.mark.asyncio
    async def test_generate_snapshot_error(self, mock_api_client: MagicMock) -> None:
        """Test generate_snapshot handles errors."""
        mock_api_client.camera.generate_device_camera_snapshot.side_effect = (
            AsyncAPIError(MagicMock(), MagicMock(), "API Error")
        )
        repo = CameraRepository(mock_api_client, "org_123")

        result = await repo.generate_snapshot("CAM-1234")

        assert result is None

    @pytest.mark.asyncio
    async def test_set_rtsp_stream_enabled_success(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test set_rtsp_stream_enabled success."""
        repo = CameraRepository(mock_api_client, "org_123")

        await repo.set_rtsp_stream_enabled("CAM-1234", True)

        mock_api_client.camera.update_camera_video_settings.assert_called_once_with(
            "CAM-1234", externalRtspEnabled=True
        )

    @pytest.mark.asyncio
    async def test_set_rtsp_stream_disabled(self, mock_api_client: MagicMock) -> None:
        """Test set_rtsp_stream_enabled to disable."""
        repo = CameraRepository(mock_api_client, "org_123")

        await repo.set_rtsp_stream_enabled("CAM-1234", False)

        mock_api_client.camera.update_camera_video_settings.assert_called_once_with(
            "CAM-1234", externalRtspEnabled=False
        )

    @pytest.mark.asyncio
    async def test_set_rtsp_stream_enabled_error(
        self, mock_api_client: MagicMock
    ) -> None:
        """Test set_rtsp_stream_enabled handles errors."""
        mock_api_client.camera.update_camera_video_settings.side_effect = AsyncAPIError(
            MagicMock(), MagicMock(), "API Error"
        )
        repo = CameraRepository(mock_api_client, "org_123")

        # Should not raise, just log error
        await repo.set_rtsp_stream_enabled("CAM-1234", True)
