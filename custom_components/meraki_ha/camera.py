"""Support for Meraki cameras."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

import aiohttp
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

<<<<<<< HEAD
from .const import DOMAIN, PLATFORM_CAMERA
from .core.utils.naming_utils import format_device_name
from .core.utils.network_utils import construct_rtsp_url
=======
from .const import DOMAIN
from .core.utils.naming_utils import format_device_name
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
from .helpers.entity_helpers import format_entity_name

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

<<<<<<< HEAD
    from .coordinator import MerakiDataUpdateCoordinator
=======
    from .meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
    from .services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)

<<<<<<< HEAD
SUPPORT_STREAM = CameraEntityFeature.STREAM

=======
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
<<<<<<< HEAD
    """
    Set up Meraki camera entities from a config entry.

    Args:
        hass: The Home Assistant instance.
        config_entry: The config entry.
        async_add_entities: Callback to add entities.

    """
    if config_entry.entry_id not in hass.data[DOMAIN]:
        return
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: MerakiDataUpdateCoordinator = entry_data["coordinator"]
    camera_service: CameraService = entry_data["camera_service"]

    camera_entities = [
        MerakiCamera(coordinator, config_entry, device, camera_service)
        for device in coordinator.data["devices"]
        if device.get("productType", "").startswith("camera")
    ]

    if camera_entities:
        async_add_entities(camera_entities)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Unload a config entry.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry.

    Returns
    -------
        Whether the unload was successful.

    """
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_CAMERA])
=======
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
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)


class MerakiCamera(CoordinatorEntity, Camera):
    """
    Representation of a Meraki camera.

<<<<<<< HEAD
    This entity is state-driven by the central MerakiDataUpdateCoordinator.
=======
    This entity is state-driven by the central MerakiDataCoordinator.
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
    """

    _attr_brand = "Cisco Meraki"

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
        config_entry: ConfigEntry,
        device: dict[str, Any],
        camera_service: CameraService,
    ) -> None:
<<<<<<< HEAD
        """
        Initialize the camera.

        Args:
            coordinator: The data update coordinator.
            config_entry: The config entry.
            device: The device data.
            camera_service: The camera service.

        """
        super().__init__(coordinator)
        # We need to call Camera's __init__ as well due to multiple inheritance
=======
        """Initialize the camera."""
        super().__init__(coordinator)
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
        Camera.__init__(self)
        self._config_entry = config_entry
        self._device_serial = device["serial"]
        self._camera_service = camera_service
<<<<<<< HEAD
        self._device_data = device  # Store initial data
        self._attr_unique_id = f"{self._device_serial}-camera"
        self._attr_name = format_entity_name(
            format_device_name(self._device_data, self._config_entry.options),
            "",
        )
        self._attr_model = self._device_data.get("model")
        self._attr_entity_registry_enabled_default = True
        self._disabled_reason: str | None = None

        video_settings = self._device_data.get("video_settings", {})
        if not video_settings.get("rtspUrl") and not self._device_data.get("lanIp"):
            self._attr_entity_registry_enabled_default = False
            self._disabled_reason = "No stream URL or LAN IP address from the API."

        # Set supported features based on camera model
        if self._attr_model and self._attr_model.startswith("MV2"):
            self._attr_supported_features = CameraEntityFeature(0)
        else:
            self._attr_supported_features = SUPPORT_STREAM

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.coordinator.is_pending(self.unique_id):
            return  # Ignore update during cooldown

        # Find the updated device data from the coordinator's payload
        self._device_data = next(
            (
                device
                for device in self.coordinator.data.get("devices", [])
                if device.get("serial") == self._device_serial
            ),
            self._device_data,
        )
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for the camera."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(self._device_data, self._config_entry.options),
            model=self._device_data.get("model"),
=======
        self._attr_unique_id = f"{self._device_serial}-camera"
        self._attr_name = format_entity_name(
            format_device_name(self.device_data, self.coordinator.config_entry.options),
            "",
        )
        self._attr_model = self.device_data.get("model")

    @property
    def device_data(self) -> dict[str, Any]:
        """Return the device data from the coordinator."""
        return self.coordinator.get_device(self._device_serial) or {}

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(
                self.device_data, self.coordinator.config_entry.options
            ),
            model=self.device_data.get("model"),
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
            manufacturer="Cisco Meraki",
        )

    async def async_camera_image(
<<<<<<< HEAD
        self,
        width: int | None = None,
        height: int | None = None,
    ) -> bytes | None:
        """
        Return a still image from the camera.

        This method includes a retry mechanism to handle the delay in snapshot
        generation by the Meraki cloud.

        Args:
            width: The desired width of the image.
            height: The desired height of the image.

        Returns
        -------
            The image bytes or None if an error occurred.

        """
        if self._device_data.get("status") != "online":
            _LOGGER.debug(
                "Not fetching snapshot for camera %s because it is not online",
                self.name,
            )
            return None
        snapshot_url = await self._camera_service.generate_snapshot(self._device_serial)

        if not snapshot_url:
            _LOGGER.error("Could not generate snapshot for camera %s", self.name)
            return None

        for attempt in range(3):  # Retry up to 3 times
            try:
                session = async_get_clientsession(self.hass)
                async with session.get(snapshot_url) as response:
                    if response.status == 200:
                        return await response.read()
                    _LOGGER.debug(
                        "Attempt %d to fetch snapshot for %s failed with status %s",
                        attempt + 1,
                        self.name,
                        response.status,
                    )
            except aiohttp.ClientError as err:
                _LOGGER.debug(
                    "Attempt %d to fetch snapshot for %s failed with error: %s",
                    attempt + 1,
                    self.name,
                    err,
                )

            if attempt < 2:  # Don't sleep on the last attempt
                await asyncio.sleep(2)  # Wait 2 seconds before retrying

        _LOGGER.error(
            "Failed to fetch snapshot for %s after multiple attempts.",
            self.name,
        )
        return None

    async def stream_source(self) -> str | None:
        """Return the source of the stream, prioritizing LAN IP."""
        if not self.is_streaming:
            return None

        lan_ip = self._device_data.get("lanIp")
        video_settings = self._device_data.get("video_settings", {})
        api_url = video_settings.get("rtspUrl")

        # Prioritize local LAN stream if an IP is available.
        if lan_ip:
            return construct_rtsp_url(lan_ip)

        # Fall back to the cloud-provided URL if it's a valid RTSP link.
        if api_url and api_url.startswith("rtsp://"):
            return api_url

        _LOGGER.warning("Could not determine a valid RTSP URL for camera %s", self.name)
=======
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image from the camera."""
        if self.device_data.get("status") != "online":
            _LOGGER.debug("Skipping snapshot for offline camera: %s", self.name)
            return None

        url = await self._camera_service.generate_snapshot(self._device_serial)
        if not url:
            msg = f"Failed to get snapshot URL for {self.name}"
            _LOGGER.error(msg)
            self.coordinator.add_status_message(self._device_serial, msg)
            return None

        try:
            session = async_get_clientsession(self.hass)
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.read()
        except aiohttp.ClientError as e:
            msg = f"Error fetching snapshot for {self.name}: {e}"
            _LOGGER.error(msg)
            self.coordinator.add_status_message(self._device_serial, msg)
            return None

    async def stream_source(self) -> str | None:
        """Return the source of the stream, if enabled."""
        if self.is_streaming:
            return self.device_data.get("rtsp_url")
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
<<<<<<< HEAD
        attrs: dict[str, Any] = {}
        if self._disabled_reason:
            attrs["disabled_reason"] = self._disabled_reason
            return attrs

        video_settings = self._device_data.get("video_settings", {})
        if not video_settings.get("rtspServerEnabled"):
            attrs["stream_status"] = "Disabled in Meraki Dashboard"
            self.coordinator.add_status_message(
                self._device_serial,
                "RTSP stream is disabled in the Meraki dashboard.",
            )
        elif not video_settings.get("rtspUrl") and not self._device_data.get("lanIp"):
            attrs["stream_status"] = "Stream URL not available."
            self.coordinator.add_status_message(
                self._device_serial,
                "RTSP stream URL is not available.",
=======
        attrs = {}
        video_settings = self.device_data.get("video_settings", {})
        if not video_settings.get("rtspServerEnabled", False):
            attrs["stream_status"] = "Disabled in Meraki Dashboard"
            self.coordinator.add_status_message(
                self._device_serial, "RTSP stream is disabled in the Meraki dashboard."
            )
        elif not self.device_data.get("rtsp_url"):
            attrs["stream_status"] = (
                "Stream URL not available. This may be because the camera does not"
                " support cloud archival."
            )
            self.coordinator.add_status_message(
                self._device_serial,
                "RTSP stream URL is not available. The camera might not support cloud"
                " archival.",
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
            )
        else:
            attrs["stream_status"] = "Enabled"
        return attrs

    @property
<<<<<<< HEAD
=======
    def supported_features(self) -> CameraEntityFeature:
        """Return supported features."""
        return CameraEntityFeature.STREAM

    @property
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
    def is_streaming(self) -> bool:
        """
        Return true if the camera is streaming.

<<<<<<< HEAD
        This requires the rtspServerEnabled setting to be true and for either a
        valid rtsp:// URL or a LAN IP to be available.
        """
        video_settings = self._device_data.get("video_settings", {})
        if not video_settings.get("rtspServerEnabled"):
            return False

        # A stream is available if we have a LAN IP or a valid cloud-provided URL.
        has_lan_ip = self._device_data.get("lanIp") is not None
        cloud_url = video_settings.get("rtspUrl")
        has_valid_cloud_url = (
            cloud_url is not None
            and isinstance(cloud_url, str)
            and cloud_url.startswith("rtsp://")
        )

        return has_lan_ip or has_valid_cloud_url

    async def _async_set_stream_state(self, enabled: bool) -> None:
        """
        Optimistically update the stream state and make the API call.

        Args:
            enabled: Whether to enable or disable the stream.

        """
        device_in_coordinator = next(
            (
                device
                for device in self.coordinator.data.get("devices", [])
                if device.get("serial") == self._device_serial
            ),
            None,
        )

        if not device_in_coordinator:
            _LOGGER.error(
                "Could not find device %s in coordinator data to update",
                self._device_serial,
            )
            return

        # Optimistically update the shared data
        if "video_settings" not in device_in_coordinator:
            device_in_coordinator["video_settings"] = {}
        device_in_coordinator["video_settings"]["rtspServerEnabled"] = enabled

        # Also optimistically update the URL if we can
        lan_ip = device_in_coordinator.get("lanIp")
        if enabled and lan_ip:
            device_in_coordinator["video_settings"]["rtspUrl"] = construct_rtsp_url(
                lan_ip,
            )
        elif not enabled:
            # Clear the URL when disabled
            if "video_settings" in device_in_coordinator:
                device_in_coordinator["video_settings"]["rtspUrl"] = None

        # Notify all listeners of the optimistic change
        self.coordinator.async_update_listeners()

        # Register a cooldown to prevent overwriting the optimistic state
        self.coordinator.register_pending_update(self.unique_id)

        # Make the API call
        try:
            await self._camera_service.async_set_rtsp_stream_enabled(
                self._device_serial,
                enabled,
            )
        except Exception as e:
            _LOGGER.error(
                "Failed to update RTSP stream for %s: %s",
                self._device_serial,
                e,
            )
            # Revert optimistic update on failure
            device_in_coordinator["video_settings"]["rtspServerEnabled"] = not enabled
            self.coordinator.async_update_listeners()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the camera stream."""
        await self._async_set_stream_state(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the camera stream."""
        await self._async_set_stream_state(False)
=======
        This requires both the rtspServerEnabled setting to be true and a
        valid rtsp:// URL to be available.
        """
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
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
