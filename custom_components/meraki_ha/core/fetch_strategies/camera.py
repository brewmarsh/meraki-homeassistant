"""Camera fetch strategy."""

from __future__ import annotations

from typing import Any

from ...core.models.device import MerakiDevice
from .base import BaseFetchStrategy


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
        # Fetch every 5th poll (poll_count 1, 6, 11... or 0, 5, 10...)
        # If we want the first poll to always fetch, we should start at 0 and use % 5 == 0
        # and increment before checking, or start at 1.
        # DataFetchManager calls increment_poll_count() before anything else.
        # So first poll will be 1.
        # (self._poll_count - 1) % 5 == 0 will be True for 1, 6, 11...
        return (self._poll_count - 1) % 5 == 0

    def build_device_tasks(
        self,
        device: MerakiDevice,
        tasks: dict[str, Any],
        detail_data: dict[str, Any] | None = None,
    ) -> None:
        """Add camera specific device tasks."""
        tasks[f"video_settings_{device.serial}"] = self.client.run_with_semaphore(
            self.client.camera.get_camera_video_settings(device.serial),
        )
        if self.should_fetch_sense:
            tasks[f"sense_settings_{device.serial}"] = self.client.run_with_semaphore(
                self.client.camera.get_camera_sense_settings(device.serial),
            )

            # Only add analytics task if not already provided in batch data
            analytics_key = f"camera_analytics_{device.serial}"
            if not detail_data or analytics_key not in detail_data:
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
        """Process camera details."""
        if settings := detail_data.get(f"video_settings_{device.serial}"):
            device.video_settings = settings
            if isinstance(settings, dict):
                device.rtsp_url = settings.get("rtsp_url")
            else:
                device.rtsp_url = None
        elif prev_device and prev_device.video_settings:
            device.video_settings = prev_device.video_settings
            device.rtsp_url = prev_device.rtsp_url

        if settings := detail_data.get(f"sense_settings_{device.serial}"):
            device.sense_settings = settings
        elif prev_device and prev_device.sense_settings:
            device.sense_settings = prev_device.sense_settings

        if analytics := detail_data.get(f"camera_analytics_{device.serial}"):
            if isinstance(analytics, list):
                device.analytics = analytics
        elif prev_device and prev_device.analytics:
            device.analytics = prev_device.analytics
