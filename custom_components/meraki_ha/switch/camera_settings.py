"""Base classes for Meraki camera switch entities."""

from typing import Any, Dict
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..core.api.client import MerakiAPIClient
from ..core.coordinators.device import MerakiDeviceCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSettingSwitchBase(CoordinatorEntity[MerakiDeviceCoordinator], SwitchEntity):
    """Base class for a Meraki Camera Setting Switch."""

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
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

    @property
    def is_on(self) -> bool:
        """Return the current state of the switch."""
        # The state is derived from the coordinator's data
        # This assumes the data is structured like: {'video_settings': {'senseEnabled': True}}
        # or {'audio_settings': {'audioDetection': {'enabled': True}}}
        # The state is now derived from the coordinator's data
        for device in self.coordinator.data.get("devices", []):
            if device.get("serial") == self._device_data["serial"]:
                keys = self._api_field.split('.')
                value = device
                for key in keys:
                    if isinstance(value, dict):
                        value = value.get(key)
                    else:
                        return False
                return bool(value)
        return False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the setting on."""
        await self._async_update_setting(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the setting off."""
        await self._async_update_setting(False)

    async def _async_update_setting(self, is_on: bool) -> None:
        """Update the setting via the Meraki API."""
        try:
            # Construct the payload based on the nested API field
            payload = {}
            keys = self._api_field.split('.')
            current_level = payload
            for i, key in enumerate(keys):
                if i == len(keys) - 1:
                    current_level[key] = is_on
                else:
                    current_level[key] = {}
                    current_level = current_level[key]

            if "sense" in self._api_field:
                await self.client.camera.update_camera_sense_settings(
                    serial=self._device_data["serial"], **payload
                )
            else:
                await self.client.camera.update_camera_video_settings(
                    serial=self._device_data["serial"], **payload
                )
            # Optimistically update the state
            # This assumes the API call will succeed
            if self.is_on != is_on:
                # To be implemented: update local state if necessary
                pass
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(
                "Failed to update camera setting %s for %s: %s",
                self._key,
                self._device_data["serial"],
                e,
            )

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {("meraki_ha", self._device_data["serial"])},
            "name": self._device_data["name"],
            "manufacturer": "Cisco Meraki",
            "model": self._device_data["model"],
        }
