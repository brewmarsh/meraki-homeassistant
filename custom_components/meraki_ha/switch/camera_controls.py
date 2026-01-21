"""Switch entities for controlling Meraki camera settings."""

from __future__ import annotations

import logging


from ..coordinator import MerakiDataUpdateCoordinator
from ..core.api.client import MerakiAPIClient
from .camera_settings import MerakiCameraSettingSwitchBase
from ..types import MerakiDevice



_LOGGER = logging.getLogger(__name__)


class AnalyticsSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control analytics on a Meraki camera."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: MerakiDevice,
    ) -> None:
        """
        Initialize the analytics switch.

        Args:
        ----
            coordinator: The data update coordinator.
            meraki_client: The Meraki API client.
            device_data: The device data.

        """
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "sense_enabled",
            "sense_settings.analyticsEnabled",
        )
        self._attr_name = f"[Camera] {device_data.name} Analytics"
        self._attr_icon = "mdi:chart-bar"

    async def _async_update_setting(self, is_on: bool) -> None:
        """
        Update the setting via the Meraki API.

        Args:
        ----
            is_on: Whether the setting is on or off.

        """
        serial = self._device_data.serial
        try:
            await self.client.camera.update_camera_sense_settings(
                serial=serial,
                sense_enabled=is_on,
            )
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to update camera setting %s for %s: %s",
                self._key,
                serial,
                e,
            )
