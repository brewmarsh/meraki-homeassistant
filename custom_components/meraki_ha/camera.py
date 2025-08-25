"""Support for Meraki cameras."""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from homeassistant.components.camera import (
    Camera,
    CameraEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    CONF_AUTO_ENABLE_RTSP,
    CONF_USE_LAN_IP_FOR_RTSP,
    DATA_CLIENT,
)
from .core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from urllib.parse import urlparse
from .helpers.entity_helpers import format_entity_name
from .core.utils.naming_utils import format_device_name


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki camera entities from a config entry."""
    meraki_device_coordinator = hass.data[DOMAIN][config_entry.entry_id].get(
        "coordinator"
    )

    if meraki_device_coordinator and meraki_device_coordinator.data:
        entities = [
            MerakiCamera(
                meraki_device_coordinator,
                device,
            )
            for device in meraki_device_coordinator.data.get("devices", [])
            if device.get("productType") == "camera"
        ]

        if config_entry.options.get(CONF_AUTO_ENABLE_RTSP, False):

            async def _enable_rtsp_in_background():
                """Enable RTSP for cameras in the background."""
                client = hass.data[DOMAIN][config_entry.entry_id][DATA_CLIENT]
                cameras_to_enable = []
                for entity in entities:
                    is_enabled = entity._device.get("video_settings", {}).get(
                        "externalRtspEnabled"
                    )
                    is_mv2 = str(entity._attr_model).startswith("MV2")
                    if not is_enabled and not is_mv2:
                        cameras_to_enable.append(entity)

                if cameras_to_enable:
                    _LOGGER.info(
                        "Found %d cameras to auto-enable RTSP for.",
                        len(cameras_to_enable),
                    )
                    for entity in cameras_to_enable:
                        try:
                            _LOGGER.info(
                                "Auto-enabling RTSP for camera %s",
                                entity._device["serial"],
                            )
                            await client.camera.update_camera_video_settings(
                                serial=entity._device["serial"],
                                externalRtspEnabled=True,
                            )
                            # Wait a moment before enabling the next one to avoid overwhelming the API
                            await asyncio.sleep(1)
                        except Exception as e:
                            _LOGGER.error(
                                "Error enabling RTSP for camera %s: %s",
                                entity._device["serial"],
                                e,
                            )
                    # After enabling, refresh the coordinator to get the updated data
                    await meraki_device_coordinator.async_request_refresh()

            hass.async_create_task(_enable_rtsp_in_background())

        async_add_entities(entities, True)


class MerakiCamera(CoordinatorEntity[MerakiDataCoordinator], Camera):
    """Representation of a Meraki camera."""

    _attr_brand = "Cisco Meraki"
    _attr_is_streaming = False
    _attr_supported_features = CameraEntityFeature(0)

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Dict[str, Any],
    ) -> None:
        """Initialize the camera."""
        super().__init__(coordinator)
        Camera.__init__(self)  # Initialize the Camera class properly
        self._device = device
        self._auto_enable_rtsp = self.coordinator.config_entry.options.get(
            CONF_AUTO_ENABLE_RTSP, False
        )
        self._use_lan_ip_for_rtsp = self.coordinator.config_entry.options.get(
            CONF_USE_LAN_IP_FOR_RTSP,
            self.coordinator.config_entry.data.get(CONF_USE_LAN_IP_FOR_RTSP, False),
        )
        self._attr_unique_id = f"{self._device['serial']}-camera"
        self._attr_name = format_entity_name(
            format_device_name(self._device, self.coordinator.config_entry.options),
            "",
        )
        self._attr_model = device.get("model")
        # Initialize camera-specific attributes
        self._rtsp_url: Optional[str] = None
        self._webrtc_provider = None
        self._legacy_webrtc_provider = None
        self.access_tokens: List[str] = []
        self._supports_native_async_webrtc = False
        self._supports_native_sync_webrtc = False
        self._cache: Dict[Any, Any] = {}
        self._create_stream_lock = asyncio.Lock()
        self.stream = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    async def stream_source(self) -> Optional[str]:
        """Return the source of the stream."""
        return self._rtsp_url

    async def async_camera_image(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> Optional[bytes]:
        """Return a still image from the camera."""
        return None

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()

    async def _enable_rtsp(self) -> None:
        """Enable the RTSP stream for the camera."""
        if str(self._attr_model).startswith("MV2"):
            _LOGGER.warning(
                "RTSP streaming is not supported on MV2 models. Ignoring request to enable for %s.",
                self._device["serial"],
            )
            return

        client = self.coordinator.hass.data[DOMAIN][
            self.coordinator.config_entry.entry_id
        ][DATA_CLIENT]
        try:
            await self.hass.async_add_executor_job(
                lambda: client._dashboard.camera.updateDeviceCameraVideoSettings(
                    serial=self._device["serial"],
                    externalRtspEnabled=True,
                )
            )
        except Exception as e:
            _LOGGER.error(
                "Failed to enable RTSP for camera %s: %s", self._device["serial"], e
            )

    @property
    def is_streaming(self) -> bool:
        """Return true if the camera is streaming."""
        return self._rtsp_url is not None

    @property
    def entity_picture(self) -> Optional[str]:
        """Return the entity picture to use in the frontend, if any."""
        if not self.access_tokens:
            return None
        return super().entity_picture

    @property
    def state_attributes(self) -> Optional[Dict[str, Any]]:
        """Return the state attributes."""
        attrs = {}
        if self.is_streaming and self.access_tokens:
            attrs["access_token"] = self.access_tokens[-1]
        return attrs

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device["serial"] == self._device["serial"]:
                self._device = device
                video_settings = device.get("video_settings", {})

                # Update RTSP URL and streaming capabilities
                if video_settings.get("externalRtspEnabled") and not str(
                    self._attr_model
                ).startswith("MV2"):
                    public_rtsp_url = video_settings.get("rtspUrl")
                    if self._use_lan_ip_for_rtsp:
                        lan_ip = self._device.get("lanIp")
                        if lan_ip:
                            parsed_url = urlparse(public_rtsp_url)
                            port = parsed_url.port
                            self._rtsp_url = f"rtsp://{lan_ip}:{port}"
                        else:
                            self._rtsp_url = public_rtsp_url
                    else:
                        self._rtsp_url = public_rtsp_url
                    self._attr_supported_features |= CameraEntityFeature.STREAM
                    self._attr_is_streaming = True
                else:
                    self._rtsp_url = None
                    self._attr_supported_features &= ~CameraEntityFeature.STREAM
                    self._attr_is_streaming = False
                # Make sure HA updates the entity state with new feature flags
                self._attr_supported_features = self.supported_features
                self.async_write_ha_state()
                return

    async def async_stream(self) -> Optional[dict]:
        """Return streaming information."""
        if not self._rtsp_url:
            return {}

        stream_source = await self.stream_source()
        if not stream_source:
            return {}

        return {
            "stream_source": stream_source,
            "use_stream_source": True,
        }
