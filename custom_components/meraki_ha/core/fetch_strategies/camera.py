"""Camera fetch strategy."""

from __future__ import annotations

import asyncio
from typing import Any

from ...core.models.device import MerakiDevice
from .base import BaseFetchStrategy


class CameraFetchStrategy(BaseFetchStrategy):
    """Strategy for fetching camera data."""

    def build_device_tasks(
        self,
        device: MerakiDevice,
        tasks: dict[str, Any],
        capabilities: list[str],
    ) -> None:
        """Add camera specific device tasks."""
        if "camera_stream" in capabilities:
            tasks[f"video_settings_{device.serial}"] = self.client.run_with_semaphore(
                self.client.camera.get_camera_video_settings(device.serial),
            )

        if "analytics" in capabilities:
            tasks[f"sense_settings_{device.serial}"] = self.client.run_with_semaphore(
                self.client.camera.get_camera_sense_settings(device.serial),
            )
            tasks[f"camera_analytics_{device.serial}"] = self.client.run_with_semaphore(
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
        elif prev_device and hasattr(prev_device, "video_settings"):
            device.video_settings = prev_device.video_settings
            device.rtsp_url = prev_device.rtsp_url

        if settings := detail_data.get(f"sense_settings_{device.serial}"):
            device.sense_settings = settings
        elif prev_device and hasattr(prev_device, "sense_settings"):
            device.sense_settings = prev_device.sense_settings
