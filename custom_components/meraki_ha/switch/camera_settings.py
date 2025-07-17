# custom_components/meraki_ha/switch/camera_settings.py
"""Switch entities for controlling Meraki Camera settings."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback # Added HomeAssistant
from homeassistant.helpers.entity import EntityDescription, EntityCategory # Corrected import path
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
    """Base class for Meraki Camera Setting Switches.

    This base class handles common logic for camera setting switches, including
    interaction with the Meraki API client and data coordinator. Derived classes
    should define their specific `EntityDescription`. The `name` property is
    explicitly defined in derived classes to combine the device name with the
    entity-specific name from `EntityDescription`.
    """

    _attr_has_entity_name = True # Ensures HA uses device name as part of the friendly name
    entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any], # Using device_data similar to sensors
        switch_type: str,
        attribute_to_check: str,
    ) -> None:
        """Initialize the base camera setting switch.

        Args:
            coordinator: The data update coordinator.
            meraki_client: The Meraki API client for making API calls.
            device_data: Initial data dictionary for the device this switch belongs to.
            switch_type: A string to make the unique_id distinct (e.g., "sense_enabled").
            attribute_to_check: The string path (dot-separated for nested) of the attribute
                                in the device data that reflects the switch's state
                                (e.g., "senseEnabled" or "audioDetection.enabled").
        """
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._device_serial: str = device_data["serial"]

        # attribute_to_check is used to find the state value in coordinator data.
        # e.g., "senseEnabled" or "audioDetection.enabled"
        self._attribute_to_check = attribute_to_check
        # _attribute_path is used for easy traversal of nested dictionaries.
        self._attribute_path = attribute_to_check.split('.')

        self._attr_unique_id = f"{self._device_serial}_{switch_type}_switch"

        # Device Info to link to the physical camera device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)}
        )

        # Set initial state
        self._update_internal_state()
        # _LOGGER.debug(
        #     "%s initialized for %s (Serial: %s)",
        #     self.__class__.__name__,
        #     device_data.get("name", self._device_serial),
        #     self._device_serial,
        # ) # Removed

    # The explicit 'name' property is removed.
    # With _attr_has_entity_name = True and self.entity_description.name set,
    # Home Assistant will automatically generate the name as "Device Name Entity Description Name".
    # Note: The `name` property is defined in the derived classes as it combines
    # the device name (from coordinator) and the entity_description.name.
    # `_attr_has_entity_name = True` assists HA in this process for UI display.

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this switch's device from the coordinator.

        The coordinator's data is expected to have camera-specific settings
        (like 'senseEnabled' and 'audioDetection') already merged into the device entry.
        """
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        _LOGGER.debug( # This log occurs if the device is no longer in the coordinator's list
            "Device data for serial '%s' not found in coordinator for switch '%s'. Entity will likely be unavailable.",
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
        """Update the `_attr_is_on` state of the switch based on coordinator data.

        Reads the state from `current_device_data` using `self._attribute_path`.
        Handles cases where the attribute or its parent dictionary might be missing.
        """
        current_device_data = self._get_current_device_data()
        if current_device_data:
            # Traverse the attribute path to get the raw value
            raw_value_container: dict[str, Any] | None = current_device_data
            valid_path = True
            for key_part in self._attribute_path[:-1]: # Navigate to parent dict
                if isinstance(raw_value_container, dict):
                    raw_value_container = raw_value_container.get(key_part)
                else:
                    valid_path = False
                    break

            raw_value = None
            if valid_path and isinstance(raw_value_container, dict):
                raw_value = raw_value_container.get(self._attribute_path[-1])
            elif valid_path and len(self._attribute_path) == 1: # For top-level attributes like "senseEnabled"
                 raw_value = current_device_data.get(self._attribute_path[0])


            if raw_value is None:
                self._attr_is_on = False
                # _LOGGER.debug(
                #     "Attribute '%s' not found or its path was invalid for %s in coordinator data. Defaulting to off.",
                #     self._attribute_to_check,
                #     self.unique_id,
                # ) # Removed
            else:
                self._attr_is_on = bool(raw_value)
        else:
            self._attr_is_on = False
            # _LOGGER.debug(
            #     "Device data for %s not found in coordinator. Defaulting to off and unavailable.",
            #     self.unique_id,
            # ) # Removed

    async def _update_camera_setting(self, value: bool) -> None:
        """Update the specific camera setting (sense or audio) via the Meraki API.

        Constructs keyword arguments for `meraki_client.update_camera_sense_settings`
        based on `self._attribute_path` and calls the API. Refreshes coordinator on success.

        Args:
            value: The new boolean state to set for the camera setting.
        """
        # _LOGGER.info(...) # Removed placeholder log, debug log below is sufficient

        # Prepare keyword arguments for the API client method based on the attribute path
        kwargs_for_api = {}
        if self._attribute_path == ["senseEnabled"]:
            kwargs_for_api["sense_enabled"] = value
        elif self._attribute_path == ["audioDetection", "enabled"]:
            kwargs_for_api["audio_detection_enabled"] = value
        else:
            _LOGGER.error(
                "Unsupported attribute path for API call: %s", self._attribute_path
            )
            return

        try:
            # _LOGGER.debug(
            #     "Calling update_camera_sense_settings for %s with args: %s",
            #     self._device_serial,
            #     kwargs_for_api,
            # ) # Removed
            await self._meraki_client.update_camera_sense_settings(
                serial=self._device_serial, **kwargs_for_api
            )

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
        """Return True if entity is available and its specific data is present."""
        if not super().available:  # Checks coordinator's last_update_success
            return False

        current_device_data = self._get_current_device_data()
        if not current_device_data:
            return False # Device not in coordinator data

        # Check for presence of the specific attribute this switch relies on
        if self._attribute_path == ["senseEnabled"]:
            if "senseEnabled" not in current_device_data:
                # _LOGGER.debug("Switch %s unavailable, senseEnabled missing", self.unique_id) # Removed
                return False
        elif self._attribute_path == ["audioDetection", "enabled"]:
            audio_data = current_device_data.get("audioDetection")
            if not isinstance(audio_data, dict) or "enabled" not in audio_data:
                # _LOGGER.debug("Switch %s unavailable, audioDetection.enabled missing/malformed", self.unique_id) # Removed
                return False
        elif self._attribute_path == ["externalRtspEnabled"]:
            if "externalRtspEnabled" not in current_device_data:
                # _LOGGER.debug("Switch %s unavailable, externalRtspEnabled missing from coordinator data", self.unique_id) # Removed
                return False
        else:
            _LOGGER.warning("Switch %s has unhandled _attribute_path for availability check: %s", self.unique_id, self._attribute_path)
            return False # Should not happen with defined switches

        return True


class MerakiCameraSenseSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the MV Sense (Computer Vision) state of a Meraki Camera.

    Uses `EntityDescription` for its specific name ("MV Sense").
    The `name` property combines the device name with "MV Sense".
    """

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
        self.entity_description = EntityDescription(key="sense_enabled", name="MV Sense")

    @property
    def name(self) -> str:
        """Return the explicit name of the switch."""
        device_data = self._get_current_device_data()
        device_name = device_data.get("name", "Camera") if device_data else "Camera"
        return f"{device_name} {self.entity_description.name}"


class MerakiCameraAudioDetectionSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the Audio Detection state of a Meraki Camera.

    Uses `EntityDescription` for its specific name ("Audio Detection").
    The `name` property combines the device name with "Audio Detection".
    """

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
        self.entity_description = EntityDescription(key="audio_detection", name="Audio Detection")

    @property
    def name(self) -> str:
        """Return the explicit name of the switch."""
        device_data = self._get_current_device_data()
        device_name = device_data.get("name", "Camera") if device_data else "Camera"
        return f"{device_name} {self.entity_description.name}"


class MerakiCameraRTSPSwitch(MerakiCameraSettingSwitchBase):
    """Switch to control the RTSP Server state of a Meraki Camera.

    Uses `EntityDescription` for its specific name ("RTSP Server").
    The `name` property combines the device name with "RTSP Server".
    This switch also exposes the RTSP URL as a state attribute when enabled.
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        meraki_client: MerakiAPIClient,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the Camera RTSP Server switch."""
        super().__init__(
            coordinator,
            meraki_client,
            device_data,
            switch_type="external_rtsp_enabled",  # UPDATED for unique_id consistency
            attribute_to_check="externalRtspEnabled",  # UPDATED Key in API/coordinator data
        )
        self.entity_description = EntityDescription(
            key="external_rtsp_enabled", name="RTSP Server"  # UPDATED key for HA bookkeeping
        )
        # self._attr_extra_state_attributes = {} # Removed

    @property
    def name(self) -> str:
        """Return the explicit name of the switch."""
        device_data = self._get_current_device_data()
        device_name = device_data.get("name", "Camera") if device_data else "Camera"
        return f"{device_name} {self.entity_description.name}"

    async def _update_camera_setting(self, value: bool) -> None:
        """Update the RTSP server setting via the Meraki API.

        Args:
            value: The new boolean state to set for the RTSP server.
        """
        try:
            # _LOGGER.debug(
            #     "Calling update_camera_video_settings for %s with rtsp_server_enabled=%s",
            #     self._device_serial,
            #     value,
            # ) # Removed
            await self._meraki_client.update_camera_video_settings(
                serial=self._device_serial, rtsp_server_enabled=value
            )

            # After a successful API call, request the coordinator to refresh its data.
            # This assumes the coordinator will be updated to fetch video settings.
            await self.coordinator.async_request_refresh()
            # Update local state immediately for responsiveness
            self._attr_is_on = value
            self.async_write_ha_state()

        except Exception as e:
            _LOGGER.error(
                "Failed to update RTSP server setting for %s to %s: %s",
                self._device_serial,
                value,
                e,
            )
            # State will be reconciled by the coordinator's next update.

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
        # Base class _handle_coordinator_update calls self.async_write_ha_state()


# async_setup_entry will be defined in __init__.py for the switch platform
# and will iterate over camera devices to add these switches.
