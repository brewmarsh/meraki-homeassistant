"""Switch entities for controlling Meraki camera settings."""

from __future__ import annotations

import logging
from typing import Any

<<<<<<< HEAD
from ..core.api.client import MerakiAPIClient
from ..core.utils.naming_utils import format_device_name
from ..helpers.entity_helpers import format_entity_name
from ..meraki_data_coordinator import MerakiDataCoordinator
=======
from ..coordinator import MerakiDataUpdateCoordinator
from ..core.api.client import MerakiAPIClient
from ..core.utils.naming_utils import format_entity_name
>>>>>>> origin/beta
from .camera_settings import MerakiCameraSettingSwitchBase

_LOGGER = logging.getLogger(__name__)


class AnalyticsSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control analytics on a Meraki camera."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
=======
        coordinator: MerakiDataUpdateCoordinator,
>>>>>>> origin/beta
        meraki_client: MerakiAPIClient,
        device_data: dict[str, Any],
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
            "sense.analyticsEnabled",
        )
<<<<<<< HEAD
        config_options = (
            coordinator.config_entry.options if coordinator.config_entry else {}
        )
        self._attr_name = format_entity_name(
            format_device_name(device_data, config_options),
            "Analytics",
        )
=======
        self._attr_name = f"[Camera] {device_data['name']} Analytics"
>>>>>>> origin/beta
        self._attr_icon = "mdi:chart-bar"

    async def _async_update_setting(self, is_on: bool) -> None:
        """
        Update the setting via the Meraki API.

        Args:
        ----
            is_on: Whether the setting is on or off.

        """
        try:
            await self.client.camera.update_camera_sense_settings(
                serial=self._device_data["serial"],
                sense_enabled=is_on,
            )
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to update camera setting %s for %s: %s",
                self._key,
                self._device_data["serial"],
                e,
            )
