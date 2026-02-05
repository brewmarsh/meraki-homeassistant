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
        detail_data: dict[str, Any] | None = None,
    ) -> None:
        """Add camera specific device tasks."""
        tasks[f"video_settings_{device.serial}"] = self.client.run_with_semaphore(
            self.client.camera.get_camera_video_settings(device.serial),
        )
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
        prev_device: dict[str, Any] | None,
    ) -> None:
        """Process camera details."""
        if settings := detail_data.get(f"video_settings_{device.serial}"):
            device.video_settings = settings
            if isinstance(settings, dict):
                device.rtsp_url = settings.get("rtsp_url")
            else:
                device.rtsp_url = None
        elif prev_device and "video_settings" in prev_device:
            device.video_settings = prev_device["video_settings"]
            device.rtsp_url = prev_device.get("rtsp_url")

        if settings := detail_data.get(f"sense_settings_{device.serial}"):
            device.sense_settings = settings
        elif prev_device and "sense_settings" in prev_device:
            device.sense_settings = prev_device["sense_settings"]

        if analytics := detail_data.get(f"camera_analytics_{device.serial}"):
            if isinstance(analytics, list):
                device.analytics = analytics
        elif prev_device and "analytics" in prev_device:
            device.analytics = prev_device["analytics"]
