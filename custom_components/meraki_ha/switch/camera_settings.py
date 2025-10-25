"""Base classes for Meraki camera switch entities."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator

from ..core.api.client import MerakiAPIClient
from ..types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSettingSwitchBase(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SwitchEntity
):
    """Base class for a Meraki Camera Setting Switch."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: dict[str, Any],
        key: str,
        api_field: str,
    ) -> None:
        """Initialize a camera setting switch."""
        super().__init__(coordinator)
        self.client = meraki_client
        self._device_data = device_data
        self._key = key
        self._api_field = api_field
        self._attr_unique_id = f"{self._device_data['serial']}_{self._key}"
        self._attr_is_on = False
        self._update_state()  # Set initial state

    def _get_value_from_device(self, device: MerakiDevice | None) -> bool:
        """Drill down into the device dictionary to get the state value."""
        if device is None:
            return False
        keys = self._api_field.split(".")
        value: Any = device
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return False
        return bool(value)

    def _update_state(self) -> None:
        """Update the internal state of the switch."""
        device = self.coordinator.get_device(self._device_data["serial"])
        if device is not None:
            self._device_data = device
            self._attr_is_on = self._get_value_from_device(device)
        else:
            self._attr_is_on = False

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return the current state of the switch."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the setting on."""
        await self._async_update_setting(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the setting off."""
        await self._async_update_setting(False)

    async def _async_update_setting(self, is_on: bool) -> None:
        """Update the setting via the Meraki API."""
        try:
            if self._key == "sense_enabled":
                await self.client.camera.update_camera_sense_settings(
                    serial=self._device_data["serial"], sense_enabled=is_on
                )
            elif self._key == "audio_detection":
                parts = self._api_field.split(".")
                payload = {parts[0]: {parts[1]: {parts[2]: is_on}}}
                await self.client.camera.update_camera_video_settings(
                    serial=self._device_data["serial"], **payload
                )
            else:
                field_name = (
                    "externalRtspEnabled"
                    if "externalRtspEnabled" in self._api_field
                    else self._api_field
                )
                video_settings = await self.client.camera.update_camera_video_settings(
                    serial=self._device_data["serial"], **{field_name: is_on}
                )
                if video_settings is not None:
                    # Update coordinator data with the new video settings
                    for i, device in enumerate(
                        self.coordinator.data.get("devices", [])
                    ):
                        if device.get("serial") == self._device_data["serial"]:
                            self.coordinator.data["devices"][i][
                                "video_settings"
                            ] = video_settings
                            break
                    self.coordinator.async_update_listeners()

            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to update camera setting %s for %s: %s",
                self._key,
                self._device_data["serial"],
                e,
            )

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {("meraki_ha", self._device_data["serial"])},
            "name": self._device_data["name"],
            "manufacturer": "Cisco Meraki",
            "model": self._device_data["model"],
        }
