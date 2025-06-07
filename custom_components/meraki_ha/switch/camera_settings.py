# custom_components/meraki_ha/switch/camera_settings.py
"""Switch entities for controlling Meraki Camera settings."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback # Added HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback # Added AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo


from ..const import DOMAIN, DATA_CLIENT # DATA_CLIENT for API
from ..meraki_api import MerakiAPIClient
from ..coordinators import MerakiDataUpdateCoordinator # Using main coordinator for device data

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSettingSwitchBase(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SwitchEntity
):
    """Base class for Meraki Camera Setting Switches."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any], # Using device_data similar to sensors
        switch_type: str,
        attribute_to_check: str, # e.g., "senseEnabled" or "audioDetection.enabled" (will need parsing)
    ) -> None:
        """Initialize the base camera setting switch."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._device_serial: str = device_data["serial"]

        # This attribute determines which key in the (future) API data dict corresponds to this switch's state.
        self._attribute_to_check = attribute_to_check
        # For "audioDetection.enabled", we'll need to navigate a nested dict
        self._attribute_path = attribute_to_check.split('.')

        self._attr_unique_id = f"{self._device_serial}_{switch_type}_switch"

        # Device Info to link to the physical camera device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)}
        )

        # Set initial state
        self._update_internal_state()
        _LOGGER.debug(
            "%s initialized for %s (Serial: %s)",
            self.__class__.__name__,
            device_data.get("name", self._device_serial),
            self._device_serial,
        )

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        # Overridden by specific switch classes if _attr_has_entity_name = True doesn't suffice
        # For now, relying on Home Assistant's automatic naming with _attr_has_entity_name = True
        # and the device name.
        # If a more specific name is needed, it can be set in the derived classes.
        # Example: return f"{self._get_device_name()} {self._switch_type_display_name}"
        # Default name will be like "Device Name Entity Name"
        # We will set self.entity_description.name in derived classes for better control
        return super().name if hasattr(super(), 'name') else "Camera Switch"


    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this switch's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    # Placeholder: In the future, this should merge/fetch specific camera sense API data
                    # For now, we assume the relevant keys might be part of the main device data
                    # or will be fetched separately and merged by the coordinator.
                    return dev_data
        _LOGGER.debug(
            "Device data for serial '%s' not found in coordinator for switch '%s'.",
            self._device_serial,
            self.unique_id,
        )
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch based on coordinator data."""
        current_device_data = self._get_current_device_data()
        if current_device_data:
            # Navigate the attribute path for potentially nested keys
            value = current_device_data
            try:
                for key in self._attribute_path:
                    value = value[key]
                self._attr_is_on = bool(value)
            except (KeyError, TypeError):
                _LOGGER.warning(
                    "Could not find attribute %s for %s, assuming off.",
                    self._attribute_to_check,
                    self.unique_id
                )
                self._attr_is_on = False # Default if path is invalid or key missing
        else:
            self._attr_is_on = False
            _LOGGER.warning(
                "Could not find device data for %s in coordinator, switch state set to False",
                self.unique_id,
            )
        # Placeholder until actual API data is available
        # For now, let's assume the coordinator *might* hold this data directly on the device entry
        # or that this method will be more sophisticated when API calls are integrated.
        # self._attr_is_on = current_device_data.get(self._attribute_to_check, False)


    async def _update_camera_setting(self, value: bool) -> None:
        """Update the specific camera setting via API."""
        _LOGGER.info(
            "Placeholder: Attempting to set %s for device %s to %s",
            self._attribute_to_check,
            self._device_serial,
            value,
        )
        # This is where the actual Meraki API call will be made.
        # Example:
        # payload = { self._attribute_to_check: value } # Simplified; actual payload might be nested
        # await self._meraki_client.camera.updateDeviceCameraSense(serial=self._device_serial, **payload)

        # For "audioDetection.enabled", the payload would be:
        # payload = {"audioDetection": {"enabled": value}}

        payload = {}
        if len(self._attribute_path) == 1:
            payload = {self._attribute_path[0]: value}
        elif len(self._attribute_path) == 2: # e.g. audioDetection.enabled
            payload = {self._attribute_path[0]: {self._attribute_path[1]: value}}
        else:
            _LOGGER.error("Unsupported attribute path depth for API call: %s", self._attribute_to_check)
            return

        try:
            # Placeholder for actual API call
            _LOGGER.debug(
                "Simulating API call for %s with payload: %s", self._device_serial, payload
            )
            # Simulate API call success:
            # await self._meraki_client.devices.updateDeviceCameraSense( # Fictional method
            # serial=self._device_serial, **payload
            # )

            # After a successful API call, request the coordinator to refresh its data.
            await self.coordinator.async_request_refresh()
            # Update local state immediately for responsiveness, coordinator will confirm later
            self._attr_is_on = value
            self.async_write_ha_state()

        except Exception as e:
            _LOGGER.error(
                "Failed to update camera setting %s for %s to %s: %s",
                self._attribute_to_check,
                self._device_serial,
                value,
                e,
            )
            # Optionally, revert state or wait for coordinator
            # For now, we let the coordinator handle eventual consistency.

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._update_camera_setting(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._update_camera_setting(False)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not super().available: # Checks coordinator.last_update_success
            return False
        # Check if the specific device data is available
        return self._get_current_device_data() is not None


class MerakiCameraSenseSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the Sense Enabled state of a Meraki Camera."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the Camera Sense switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "sense_enabled", # switch_type for unique_id
            "senseEnabled",    # attribute_to_check in API data
        )
        # For more specific naming if needed:
        # self.entity_description = EntityDescription(key="sense_enabled", name="Sense Enabled")


class MerakiCameraAudioDetectionSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the Audio Detection state of a Meraki Camera."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the Camera Audio Detection switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            "audio_detection", # switch_type for unique_id
            "audioDetection.enabled", # attribute_to_check (nested)
        )
        # For more specific naming if needed:
        # self.entity_description = EntityDescription(key="audio_detection", name="Audio Detection")

# async_setup_entry will be defined in __init__.py for the switch platform
# and will iterate over camera devices to add these switches.
