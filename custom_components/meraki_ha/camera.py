"""Support for Meraki cameras."""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import aiofiles
import aiohttp
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_CAMERA_SNAPSHOT_INTERVAL,
    DEFAULT_CAMERA_SNAPSHOT_INTERVAL,
    DOMAIN,
)
from .core.utils.naming_utils import format_device_name
from .helpers.device_info_helpers import resolve_device_info
from .helpers.entity_helpers import format_entity_name
from .helpers.logging_helper import MerakiLoggers
from .meraki_data_coordinator import MerakiDataCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .services.camera_service import CameraService


_LOGGER = MerakiLoggers.CAMERA

# Storage file for camera mappings (shared with web_api.py)
CAMERA_MAPPINGS_STORAGE = "meraki_camera_mappings.json"


async def _load_camera_mappings(hass: HomeAssistant) -> dict[str, dict[str, str]]:
    """Load camera mappings from storage file."""
    storage_path = Path(hass.config.path(".storage")) / CAMERA_MAPPINGS_STORAGE
    if not storage_path.exists():
        return {}
    try:
        async with aiofiles.open(storage_path) as f:
            content = await f.read()
            return json.loads(content) if content else {}
    except (json.JSONDecodeError, OSError) as e:
        _LOGGER.warning("Failed to load camera mappings: %s", e)
        return {}


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


class MerakiCamera(CoordinatorEntity, Camera):  # type: ignore[type-arg]
    """
    Representation of a Meraki camera.

    This entity is state-driven by the central MerakiDataCoordinator.
    """

    coordinator: MerakiDataCoordinator
    _attr_brand = "Cisco Meraki"

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        device: Mapping[str, Any],
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
            format_device_name(self.device_data, config_entry.options),
            "",
        )
        self._attr_model = self.device_data.get("model")

        # Snapshot caching for configurable refresh interval
        self._cached_snapshot: bytes | None = None
        self._snapshot_timestamp: float = 0
        # Cached linked camera entity for sync property access
        self._cached_linked_entity: str | None = None

    @property
    def device_data(self) -> dict[str, Any]:
        """Return the device data from the coordinator."""
        device = self.coordinator.get_device(self._device_serial)
        return cast(dict[str, Any], device or {})

    @property
    def _snapshot_interval(self) -> int:
        """Return the configured snapshot refresh interval in seconds."""
        if self._config_entry is None:
            return DEFAULT_CAMERA_SNAPSHOT_INTERVAL
        return int(
            self._config_entry.options.get(
                CONF_CAMERA_SNAPSHOT_INTERVAL, DEFAULT_CAMERA_SNAPSHOT_INTERVAL
            )
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information with network hierarchy."""
        if self.coordinator.config_entry is None:
            return None
        return resolve_device_info(
            entity_data=self.device_data,
            config_entry=self.coordinator.config_entry,
        )

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera."""
        try:
            # If we have a linked camera, ONLY use its image (no fallback to Meraki)
            linked_entity_id = await self._get_linked_camera_entity()
            if linked_entity_id:
                linked_image = await self._get_linked_camera_image(linked_entity_id)
                if linked_image:
                    return linked_image
                # Return cached snapshot if linked camera fails
                # (don't fall back to Meraki - linked camera is authoritative)
                _LOGGER.debug(
                    "Linked camera %s failed, returning cached snapshot for %s",
                    linked_entity_id,
                    self.name,
                )
                return self._cached_snapshot
        except Exception as e:
            _LOGGER.debug("Error checking linked camera for %s: %s", self.name, e)
            # Continue to try Meraki snapshot

        try:
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
        except Exception as e:
            _LOGGER.warning("Error fetching camera image for %s: %s", self.name, e)
            return self._cached_snapshot

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
        # If we have a linked camera, ONLY use its stream (no fallback to Meraki RTSP)
        linked_entity_id = await self._get_linked_camera_entity()
        if linked_entity_id:
            stream = await self._get_linked_camera_stream(linked_entity_id)
            if stream:
                return stream
            # Don't fall back to Meraki RTSP when linked - the linked camera
            # is the authoritative source (e.g., Blue Iris already has RTSP)
            _LOGGER.debug(
                "Linked camera %s has no stream source for %s",
                linked_entity_id,
                self.name,
            )
            return None

        if not self.is_streaming:
            return None

        # Meraki cameras only support RTSP for direct streaming.
        # The "cloud video link" is a Meraki Dashboard web page URL,
        # not a direct video stream that Home Assistant can process.
        # We always use RTSP when available.
        return self.device_data.get("rtsp_url")

    async def _get_linked_camera_entity(self) -> str | None:
        """Get the linked camera entity ID from storage file."""
        all_mappings = await _load_camera_mappings(self.hass)
        entry_mappings = all_mappings.get(self._config_entry.entry_id, {})
        linked_entity = entry_mappings.get(self._device_serial)
        # Cache for sync property access in extra_state_attributes
        self._cached_linked_entity = linked_entity
        return linked_entity

    async def _get_linked_camera_stream(self, entity_id: str) -> str | None:
        """Get the stream source from a linked camera entity."""
        # Get the linked camera's state
        state = self.hass.states.get(entity_id)
        if not state:
            _LOGGER.debug("Linked camera %s not found", entity_id)
            return None

        # Try to get the stream source from the linked camera
        # First check if the linked camera has stream support
        camera_component = self.hass.data.get("camera")
        if camera_component:
            linked_camera = camera_component.get_entity(entity_id)
            if linked_camera and hasattr(linked_camera, "stream_source"):
                try:
                    return await linked_camera.stream_source()
                except Exception as e:
                    _LOGGER.debug("Error getting stream from %s: %s", entity_id, e)

        return None

    async def _get_linked_camera_image(self, entity_id: str) -> bytes | None:
        """Get an image from the linked camera entity."""
        camera_component = self.hass.data.get("camera")
        if not camera_component:
            return None

        linked_camera = camera_component.get_entity(entity_id)
        if linked_camera and hasattr(linked_camera, "async_camera_image"):
            try:
                return await linked_camera.async_camera_image()
            except Exception as e:
                _LOGGER.debug("Error getting image from %s: %s", entity_id, e)

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attrs: dict[str, Any] = {
            "snapshot_interval": self._snapshot_interval,
        }

        # Check if camera is linked to an external NVR
        linked_entity = (
            self._cached_linked_entity
            if hasattr(self, "_cached_linked_entity")
            else None
        )

        if linked_entity:
            # Linked camera - show linked status
            attrs["stream_status"] = f"Linked to {linked_entity}"
            attrs["linked_camera_entity"] = linked_entity
            attrs["stream_source"] = "linked_camera"
        else:
            # Not linked - show Meraki RTSP status
            video_settings = self.device_data.get("video_settings", {})
            rtsp_enabled = video_settings.get("rtspServerEnabled", False)
            rtsp_url = self.device_data.get("rtsp_url")

            if rtsp_enabled and rtsp_url:
                attrs["stream_status"] = "RTSP Enabled"
                attrs["stream_source"] = "meraki_rtsp"
            elif not rtsp_enabled:
                attrs["stream_status"] = "RTSP Disabled in Dashboard"
                attrs["stream_source"] = "none"
            else:
                attrs["stream_status"] = "RTSP URL Not Available"
                attrs["stream_source"] = "none"

        # Include cloud video URL for "view in browser" functionality
        # Note: This is a Meraki Dashboard URL, not a direct video stream
        cloud_url = self.device_data.get("cloud_video_url")
        if cloud_url:
            attrs["cloud_video_url"] = cloud_url

        return attrs

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # Check coordinator is working
        if not self.coordinator.last_update_success:
            return False
        # Check device exists in coordinator data
        return self.coordinator.get_device(self._device_serial) is not None

    @property
    def supported_features(self) -> CameraEntityFeature:
        """Return supported features."""
        return CameraEntityFeature.STREAM

    @property
    def is_streaming(self) -> bool:
        """
        Return true if the camera can stream.

        When a camera is linked to an external NVR (e.g., Blue Iris), we assume
        streaming is available through the linked camera. Otherwise, Meraki cameras
        only support RTSP for direct streaming in Home Assistant.
        """
        # If we have a linked camera configured, streaming is handled by it
        # Note: We use the cached value here since this is a sync property
        if hasattr(self, "_cached_linked_entity") and self._cached_linked_entity:
            # Check if the linked camera entity exists and is available
            state = self.hass.states.get(self._cached_linked_entity)
            return state is not None and state.state != "unavailable"

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
