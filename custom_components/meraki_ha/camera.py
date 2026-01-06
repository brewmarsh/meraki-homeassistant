"""Support for Meraki cameras."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import TYPE_CHECKING, Any

import aiohttp
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_CAMERA_ENTITY_MAPPINGS,
    CONF_CAMERA_SNAPSHOT_INTERVAL,
    DEFAULT_CAMERA_SNAPSHOT_INTERVAL,
    DOMAIN,
)
from .core.utils.naming_utils import format_device_name
from .helpers.entity_helpers import format_entity_name

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .meraki_data_coordinator import MerakiDataCoordinator
    from .services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki camera entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    discovered_entities = entry_data.get("entities", [])

    camera_entities = [e for e in discovered_entities if isinstance(e, MerakiCamera)]

    if camera_entities:
        _LOGGER.debug("Adding %d camera entities", len(camera_entities))
        chunk_size = 50
        for i in range(0, len(camera_entities), chunk_size):
            chunk = camera_entities[i : i + chunk_size]
            async_add_entities(chunk)
            if len(camera_entities) > chunk_size:
                await asyncio.sleep(1)


class MerakiCamera(CoordinatorEntity, Camera):
    """
    Representation of a Meraki camera.

    This entity is state-driven by the central MerakiDataCoordinator.
    """

    _attr_brand = "Cisco Meraki"

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        device: dict[str, Any],
        camera_service: CameraService,
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        Camera.__init__(self)
        self._config_entry = config_entry
        self._device_serial = device["serial"]
        self._camera_service = camera_service
        self._attr_unique_id = f"{self._device_serial}-camera"
        self._attr_name = format_entity_name(
            format_device_name(self.device_data, self.coordinator.config_entry.options),
            "",
        )
        self._attr_model = self.device_data.get("model")

        # Snapshot caching for configurable refresh interval
        self._cached_snapshot: bytes | None = None
        self._snapshot_timestamp: float = 0

    @property
    def device_data(self) -> dict[str, Any]:
        """Return the device data from the coordinator."""
        return self.coordinator.get_device(self._device_serial) or {}

    @property
    def _snapshot_interval(self) -> int:
        """Return the configured snapshot refresh interval in seconds."""
        return int(
            self._config_entry.options.get(
                CONF_CAMERA_SNAPSHOT_INTERVAL, DEFAULT_CAMERA_SNAPSHOT_INTERVAL
            )
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(
                self.device_data, self.coordinator.config_entry.options
            ),
            model=self.device_data.get("model"),
            manufacturer="Cisco Meraki",
        )

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera."""
        if self.device_data.get("status") != "online":
            _LOGGER.debug("Skipping snapshot for offline camera: %s", self.name)
            return self._cached_snapshot  # Return cached image if available

        # Check if we should use the cached snapshot based on refresh interval
        interval = self._snapshot_interval
        current_time = time.time()

        if interval > 0 and self._cached_snapshot is not None:
            elapsed = current_time - self._snapshot_timestamp
            if elapsed < interval:
                _LOGGER.debug(
                    "Returning cached snapshot for %s (%.0fs old, interval=%ds)",
                    self.name,
                    elapsed,
                    interval,
                )
                return self._cached_snapshot

        # Fetch a new snapshot
        snapshot = await self._fetch_snapshot()

        # Cache the snapshot if we got one
        if snapshot is not None:
            self._cached_snapshot = snapshot
            self._snapshot_timestamp = current_time

        # Return the new snapshot, or cached one if fetch failed
        return snapshot if snapshot is not None else self._cached_snapshot

    async def _fetch_snapshot(self) -> bytes | None:
        """Fetch a fresh snapshot from the camera."""
        url = await self._camera_service.generate_snapshot(self._device_serial)
        if not url:
            msg = f"Failed to get snapshot URL for {self.name}"
            _LOGGER.debug(msg)
            return None

        # Meraki snapshot generation is asynchronous. The API returns a URL
        # immediately, but the snapshot may not be available for a few seconds.
        # We retry fetching the snapshot with a delay to allow time for generation.
        session = async_get_clientsession(self.hass)
        max_retries = 3
        retry_delay_seconds = 2

        for attempt in range(max_retries):
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.read()
                    if response.status == 202:
                        # 202 Accepted means snapshot is still being generated
                        _LOGGER.debug(
                            "Snapshot still generating for %s (attempt %d/%d)",
                            self.name,
                            attempt + 1,
                            max_retries,
                        )
                    elif response.status == 400:
                        # 400 may mean the snapshot isn't ready yet
                        _LOGGER.debug(
                            "Snapshot not ready for %s (attempt %d/%d), "
                            "retrying after delay",
                            self.name,
                            attempt + 1,
                            max_retries,
                        )
                    else:
                        _LOGGER.debug(
                            "Unexpected status %d fetching snapshot for %s",
                            response.status,
                            self.name,
                        )
            except aiohttp.ClientError as e:
                _LOGGER.debug(
                    "Network error fetching snapshot for %s (attempt %d/%d): %s",
                    self.name,
                    attempt + 1,
                    max_retries,
                    e,
                )

            # Wait before retrying (except on last attempt)
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay_seconds)

        _LOGGER.debug(
            "Failed to fetch snapshot for %s after %d attempts",
            self.name,
            max_retries,
        )
        return None

    async def stream_source(self) -> str | None:
        """Return the source of the stream, if enabled."""
        if not self.is_streaming:
            return None

        # Meraki cameras only support RTSP for direct streaming.
        # The "cloud video link" is a Meraki Dashboard web page URL,
        # not a direct video stream that Home Assistant can process.
        # We always use RTSP when available.
        return self.device_data.get("rtsp_url")

    @property
    def _linked_camera_entity(self) -> str | None:
        """Get the linked camera entity ID from config options."""
        mappings = self._config_entry.options.get(CONF_CAMERA_ENTITY_MAPPINGS, {})
        return mappings.get(self._device_serial)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        video_settings = self.device_data.get("video_settings", {})
        rtsp_enabled = video_settings.get("rtspServerEnabled", False)
        rtsp_url = self.device_data.get("rtsp_url")

        # Determine stream status
        if rtsp_enabled and rtsp_url:
            stream_status = "RTSP Enabled"
        elif not rtsp_enabled:
            stream_status = "RTSP Disabled in Dashboard"
        else:
            stream_status = "RTSP URL Not Available"

        attrs: dict[str, Any] = {
            "snapshot_interval": self._snapshot_interval,
            "stream_status": stream_status,
        }

        # Include cloud video URL for "view in browser" functionality
        # Note: This is a Meraki Dashboard URL, not a direct video stream
        cloud_url = self.device_data.get("cloud_video_url")
        if cloud_url:
            attrs["cloud_video_url"] = cloud_url

        # Include linked camera entity if configured
        # This allows linking to external NVR cameras (e.g., Blue Iris)
        linked_camera = self._linked_camera_entity
        if linked_camera:
            attrs["linked_camera_entity"] = linked_camera

        return attrs

    @property
    def supported_features(self) -> CameraEntityFeature:
        """Return supported features."""
        return CameraEntityFeature.STREAM

    @property
    def is_streaming(self) -> bool:
        """
        Return true if the camera can stream.

        Meraki cameras only support RTSP for direct streaming in Home Assistant.
        The cloud video link is a Dashboard URL (not a direct stream).
        """
        if self.device_data.get("status") != "online":
            return False

        # RTSP streaming requires the server to be enabled and a valid URL
        video_settings = self.device_data.get("video_settings", {})
        if not video_settings.get("rtspServerEnabled", False):
            return False

        url = self.device_data.get("rtsp_url")
        return url is not None and isinstance(url, str) and url.startswith("rtsp://")

    async def async_turn_on(self) -> None:
        """Turn on the camera stream."""
        _LOGGER.debug("Turning on stream for camera %s", self._device_serial)
        await self._camera_service.async_set_rtsp_stream_enabled(
            self._device_serial, True
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """Turn off the camera stream."""
        _LOGGER.debug("Turning off stream for camera %s", self._device_serial)
        await self._camera_service.async_set_rtsp_stream_enabled(
            self._device_serial, False
        )
        await self.coordinator.async_request_refresh()
