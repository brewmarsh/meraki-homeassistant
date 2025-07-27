"""Switch entities for controlling Meraki Camera schedules."""

import logging
from typing import Any, Dict

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityDescription

from ..core.api.client import MerakiAPIClient
from ..core.coordinators.device import MerakiDeviceCoordinator
from .camera_settings import MerakiCameraSettingSwitchBase

_LOGGER = logging.getLogger(__name__)


class MerakiCameraRTSPSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the RTSP Server state of a Meraki Camera."""

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the Camera RTSP Server switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            switch_type="external_rtsp_enabled",
            attribute_to_check="externalRtspEnabled",
        )
        self.entity_description = EntityDescription(
            key="external_rtsp_enabled",
            name="RTSP Server",
        )

    @property
    def name(self) -> str:
        """Return the explicit name of the switch."""
        device_data = self._get_current_device_data()
        device_name = device_data.get("name", "Camera") if device_data else "Camera"
        return f"{device_name} {self.entity_description.name}"

    async def _update_camera_setting(self, value: bool) -> None:
        """Update the RTSP server setting via the Meraki API."""
        try:
            await self._meraki_client.update_camera_video_settings(
                serial=self._device_serial, rtsp_server_enabled=value
            )
            await self.coordinator.async_request_refresh()
            self._attr_is_on = value
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error(
                "Failed to update RTSP server setting for %s to %s: %s",
                self._device_serial,
                value,
                e,
            )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (enable RTSP Server)."""
        await self._update_camera_setting(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (disable RTSP Server)."""
        await self._update_camera_setting(False)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        super()._handle_coordinator_update()
