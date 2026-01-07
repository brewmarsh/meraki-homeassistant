"""Tests for the camera service module."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.services.camera_service import CameraService


@pytest.fixture
def mock_camera_repository() -> AsyncMock:
    """Create a mock camera repository."""
    repository = AsyncMock()
    repository.get_camera_features = AsyncMock(return_value=[])
    repository.get_analytics_data = AsyncMock(return_value=None)
    repository.async_get_cloud_video_url = AsyncMock(return_value=None)
    repository.async_get_rtsp_stream_url = AsyncMock(return_value=None)
    repository.generate_snapshot = AsyncMock(return_value=None)
    repository.set_rtsp_stream_enabled = AsyncMock()
    return repository


class TestCameraService:
    """Tests for CameraService class."""

    def test_initialization(self, mock_camera_repository: AsyncMock) -> None:
        """Test camera service initialization."""
        service = CameraService(mock_camera_repository)

        assert service._repository is mock_camera_repository

    @pytest.mark.asyncio
    async def test_get_supported_analytics_with_person_detection(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_supported_analytics with person detection."""
        mock_camera_repository.get_camera_features.return_value = [
            "person_detection",
            "audio_detection",
            "other_feature",
        ]
        service = CameraService(mock_camera_repository)

        result = await service.get_supported_analytics("CAM-1234")

        assert result == ["person_detection"]
        mock_camera_repository.get_camera_features.assert_called_once_with("CAM-1234")

    @pytest.mark.asyncio
    async def test_get_supported_analytics_with_vehicle_detection(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_supported_analytics with vehicle detection."""
        mock_camera_repository.get_camera_features.return_value = [
            "vehicle_detection",
            "motion_detection",
        ]
        service = CameraService(mock_camera_repository)

        result = await service.get_supported_analytics("CAM-1234")

        assert result == ["vehicle_detection"]

    @pytest.mark.asyncio
    async def test_get_supported_analytics_with_both_detections(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_supported_analytics with both person and vehicle detection."""
        mock_camera_repository.get_camera_features.return_value = [
            "person_detection",
            "vehicle_detection",
        ]
        service = CameraService(mock_camera_repository)

        result = await service.get_supported_analytics("CAM-1234")

        assert "person_detection" in result
        assert "vehicle_detection" in result

    @pytest.mark.asyncio
    async def test_get_supported_analytics_no_detection(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_supported_analytics with no detection features."""
        mock_camera_repository.get_camera_features.return_value = [
            "audio_detection",
            "other_feature",
        ]
        service = CameraService(mock_camera_repository)

        result = await service.get_supported_analytics("CAM-1234")

        assert result == []

    @pytest.mark.asyncio
    async def test_get_analytics_data(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_analytics_data."""
        analytics_data = [{"timestamp": "2024-01-01", "count": 5}]
        mock_camera_repository.get_analytics_data.return_value = analytics_data
        service = CameraService(mock_camera_repository)

        result = await service.get_analytics_data("CAM-1234", "person")

        assert result == analytics_data
        mock_camera_repository.get_analytics_data.assert_called_once_with(
            "CAM-1234", "person"
        )

    @pytest.mark.asyncio
    async def test_get_video_stream_url_cloud_available(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_video_stream_url returns cloud URL when available."""
        mock_camera_repository.async_get_cloud_video_url.return_value = (
            "https://cloud.meraki.com/video"
        )
        service = CameraService(mock_camera_repository)

        result = await service.get_video_stream_url("CAM-1234")

        assert result == "https://cloud.meraki.com/video"
        mock_camera_repository.async_get_cloud_video_url.assert_called_once_with(
            "CAM-1234"
        )
        mock_camera_repository.async_get_rtsp_stream_url.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_video_stream_url_fallback_to_rtsp(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_video_stream_url falls back to RTSP when cloud unavailable."""
        mock_camera_repository.async_get_cloud_video_url.return_value = None
        mock_camera_repository.async_get_rtsp_stream_url.return_value = (
            "rtsp://192.168.1.100/stream"
        )
        service = CameraService(mock_camera_repository)

        result = await service.get_video_stream_url("CAM-1234")

        assert result == "rtsp://192.168.1.100/stream"

    @pytest.mark.asyncio
    async def test_get_rtsp_stream_url(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_rtsp_stream_url."""
        mock_camera_repository.async_get_rtsp_stream_url.return_value = (
            "rtsp://192.168.1.100/stream"
        )
        service = CameraService(mock_camera_repository)

        result = await service.get_rtsp_stream_url("CAM-1234")

        assert result == "rtsp://192.168.1.100/stream"
        mock_camera_repository.async_get_rtsp_stream_url.assert_called_once_with(
            "CAM-1234"
        )

    @pytest.mark.asyncio
    async def test_get_cloud_video_url(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_cloud_video_url."""
        mock_camera_repository.async_get_cloud_video_url.return_value = (
            "https://cloud.meraki.com/video"
        )
        service = CameraService(mock_camera_repository)

        result = await service.get_cloud_video_url("CAM-1234")

        assert result == "https://cloud.meraki.com/video"
        mock_camera_repository.async_get_cloud_video_url.assert_called_once_with(
            "CAM-1234"
        )

    @pytest.mark.asyncio
    async def test_get_camera_snapshot(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_camera_snapshot."""
        mock_camera_repository.generate_snapshot.return_value = (
            "https://snapshot.meraki.com/image.jpg"
        )
        service = CameraService(mock_camera_repository)

        result = await service.get_camera_snapshot("CAM-1234")

        assert result == "https://snapshot.meraki.com/image.jpg"
        mock_camera_repository.generate_snapshot.assert_called_once_with("CAM-1234")

    @pytest.mark.asyncio
    async def test_get_motion_history_with_both_types(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_motion_history combines person and vehicle history."""
        person_events = [{"type": "person", "timestamp": "2024-01-01T10:00:00"}]
        vehicle_events = [{"type": "vehicle", "timestamp": "2024-01-01T11:00:00"}]

        async def mock_analytics(serial, obj_type):
            if obj_type == "person":
                return person_events
            if obj_type == "vehicle":
                return vehicle_events
            return None

        mock_camera_repository.get_analytics_data.side_effect = mock_analytics
        service = CameraService(mock_camera_repository)

        result = await service.get_motion_history("CAM-1234")

        assert len(result) == 2
        assert person_events[0] in result
        assert vehicle_events[0] in result

    @pytest.mark.asyncio
    async def test_get_motion_history_person_only(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_motion_history with only person events."""
        person_events = [{"type": "person", "timestamp": "2024-01-01T10:00:00"}]

        async def mock_analytics(serial, obj_type):
            if obj_type == "person":
                return person_events
            return None

        mock_camera_repository.get_analytics_data.side_effect = mock_analytics
        service = CameraService(mock_camera_repository)

        result = await service.get_motion_history("CAM-1234")

        assert len(result) == 1
        assert person_events[0] in result

    @pytest.mark.asyncio
    async def test_get_motion_history_no_events(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test get_motion_history with no events."""
        mock_camera_repository.get_analytics_data.return_value = None
        service = CameraService(mock_camera_repository)

        result = await service.get_motion_history("CAM-1234")

        assert result == []

    @pytest.mark.asyncio
    async def test_generate_snapshot(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test generate_snapshot."""
        mock_camera_repository.generate_snapshot.return_value = (
            "https://snapshot.meraki.com/image.jpg"
        )
        service = CameraService(mock_camera_repository)

        result = await service.generate_snapshot("CAM-1234")

        assert result == "https://snapshot.meraki.com/image.jpg"
        mock_camera_repository.generate_snapshot.assert_called_once_with("CAM-1234")

    @pytest.mark.asyncio
    async def test_async_set_rtsp_stream_enabled(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test async_set_rtsp_stream_enabled."""
        service = CameraService(mock_camera_repository)

        await service.async_set_rtsp_stream_enabled("CAM-1234", True)

        mock_camera_repository.set_rtsp_stream_enabled.assert_called_once_with(
            "CAM-1234", True
        )

    @pytest.mark.asyncio
    async def test_async_set_rtsp_stream_disabled(
        self, mock_camera_repository: AsyncMock
    ) -> None:
        """Test async_set_rtsp_stream_enabled to disable."""
        service = CameraService(mock_camera_repository)

        await service.async_set_rtsp_stream_enabled("CAM-1234", False)

        mock_camera_repository.set_rtsp_stream_enabled.assert_called_once_with(
            "CAM-1234", False
        )

