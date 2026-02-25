"""Camera fetch strategy."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ...core.models.device import MerakiDevice
from .base import BaseFetchStrategy

if TYPE_CHECKING:
    from ...core.api.client import MerakiAPIClient


class CameraFetchStrategy(BaseFetchStrategy):
    """Strategy for fetching camera data."""

    def __init__(
        self,
        client: MerakiAPIClient,
        _disabled_features: set[str],
        enable_camera_sense: bool = True,
    ) -> None:
        """Initialize the camera fetch strategy."""
        super().__init__(client, _disabled_features)
        self.enable_camera_sense = enable_camera_sense
        self._poll_count = 0

    def increment_poll_count(self) -> None:
        """Increment the poll counter."""
        self._poll_count += 1

    @property
    def should_fetch_sense(self) -> bool:
        """Determine if sense data should be fetched this poll."""
        if not self.enable_camera_sense:
            return False
        # Fetch every 5th poll to save API quota
        return (self._poll_count - 1) % 5 == 0

    def build_device_tasks(
        self,
        device: MerakiDevice,
        tasks: dict[str, Any],
        capabilities: list[str],
        detail_data: dict[str, Any] | None = None,
    ) -> None:
        """Add camera specific device tasks."""
        # 1. Capability Guard: Check if camera supports video streaming
        if "camera_stream" in capabilities:
            tasks[f"video_settings_{device.serial}"] = self.client.run_with_semaphore(
                self.client.camera.get_camera_video_settings(device.serial),
            )

        # 2. Capability Guard: Check if camera supports analytics (Sense)
        if "camera_analytics" in capabilities:
            # Optimization: Only fetch expensive sense settings on specific intervals
            if self.should_fetch_sense:
                tasks[f"sense_settings_{device.serial}"] = (
                    self.client.run_with_semaphore(
                        self.client.camera.get_camera_sense_settings(device.serial),
                    )
                )

            # 3. Batch Awareness: Only add analytics task if NOT provided in batch data
            # AND if we are in a polling cycle that allows fetching it
            analytics_key = f"camera_analytics_{device.serial}"
            if self.should_fetch_sense and (
                not detail_data or analytics_key not in detail_data
            ):
                tasks[analytics_key] = self.client.run_with_semaphore(
                    self.client.camera.get_device_camera_analytics_recent(
                        device.serial,
                    ),
                )

    def process_device_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: MerakiDevice | None,
    ) -> None:
        """Process camera details with type safety."""
        # --- Video Settings ---
        if settings := detail_data.get(f"video_settings_{device.serial}"):
            # Type Safety: Ensure we actually got a dictionary
            if isinstance(settings, dict):
                device.video_settings = settings
                device.rtsp_url = settings.get("rtsp_url")
            else:
                # Handle error objects or None
                device.video_settings = {}
                device.rtsp_url = None
        elif prev_device:
            # Fallback to previous data (using attribute access)
            device.video_settings = getattr(prev_device, "video_settings", None)
            device.rtsp_url = getattr(prev_device, "rtsp_url", None)

        # --- Sense Settings ---
        if settings := detail_data.get(f"sense_settings_{device.serial}"):
            if isinstance(settings, dict):
                device.sense_settings = settings
        elif prev_device:
            device.sense_settings = getattr(prev_device, "sense_settings", None)

        # --- Analytics ---
        # Prioritize fresh batch data
        if analytics := detail_data.get(f"camera_analytics_{device.serial}"):
            if isinstance(analytics, list):
                device.camera_analytics = analytics
        elif prev_device:
            device.camera_analytics = getattr(prev_device, "camera_analytics", [])
