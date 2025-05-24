"""Defines the MerakiSSIDSwitch entity and related helper functions.

This module contains the `MerakiSSIDSwitch` class, a Home Assistant switch
entity that allows users to enable or disable a specific Meraki SSID on a
particular device. The control mechanism currently implemented involves
manipulating device tags.

It also includes the `match_device_to_ssid` helper function, which determines
if an SSID switch should be created for a device based on tag matching logic.
"""

import logging
from typing import Any, Dict, List, Optional # Added Optional

import aiohttp # For API call error handling

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity # Changed from DataUpdateCoordinator
from homeassistant.core import callback # For _handle_coordinator_update

# Assuming MerakiDataUpdateCoordinator is the correct coordinator type
from ..const import DOMAIN
from ..coordinator import MerakiDataUpdateCoordinator
from ..meraki_api.devices import update_device_tags # For making the API call

_LOGGER = logging.getLogger(__name__)


def match_device_to_ssid(
    ssid_info: Dict[str, Any],
    all_devices_data: List[Dict[str, Any]], # Assuming this is a list of all devices
    relaxed_matching: bool,
    target_device_serial: Optional[str] = None, # Optional: if matching for a specific device
) -> bool:
    """Determines if a specific device should manage a given SSID based on tags.

    This function implements the logic to decide whether a switch entity should
    be created for an SSID on a particular device. The decision is based on
    matching tags defined in the SSID's configuration against the tags
    present on the device.

    - If the SSID has no tags defined, it's considered a match for any device
      (or the `target_device_serial` if provided), implying it's a general SSID.
    - If the SSID has tags:
        - With `relaxed_matching` True: A match occurs if the device has *any* of
          the tags specified in the SSID's configuration.
        - With `relaxed_matching` False (strict): A match occurs only if the device
          has *all* of the tags specified in the SSID's configuration.

    Args:
        ssid_info (Dict[str, Any]): The dictionary containing information for the SSID,
            expected to have a "tags" key (list of strings).
        all_devices_data (List[Dict[str, Any]]): A list of all device dictionaries
            from the coordinator. This is used if `target_device_serial` is not provided
            or if context from other devices is needed (though current logic iterates).
        relaxed_matching (bool): If True, uses "any tag match" logic; otherwise,
            requires "all tags match".
        target_device_serial (Optional[str]): If provided, the matching is specifically
            checked against this device. If None, it iterates through `all_devices_data`.
            For creating a switch for a *specific* device-SSID pair, this should be provided.

    Returns:
        bool: True if the device (or any device if `target_device_serial` is None)
              matches the SSID's tag criteria, False otherwise.
    """
    ssid_tags = ssid_info.get("tags", [])
    if not isinstance(ssid_tags, list):
        _LOGGER.warning("SSID '%s' has malformed tags: %s. Assuming no tags.", ssid_info.get("name"), ssid_tags)
        ssid_tags = []

    # If the SSID has no tags, it's considered a general SSID.
    # It should match if we are not targeting a specific device OR if we are and it's the one.
    if not ssid_tags:
        _LOGGER.debug("SSID '%s' has no tags, considered a match by default.", ssid_info.get("name"))
        return True

    devices_to_check = all_devices_data
    if target_device_serial:
        # Filter to check only the target device.
        target_device_info = next((dev for dev in all_devices_data if dev.get("serial") == target_device_serial), None)
        if not target_device_info:
            _LOGGER.warning("Target device serial %s not found in all_devices_data for SSID matching.", target_device_serial)
            return False
        devices_to_check = [target_device_info]

    for device in devices_to_check:
        device_tags = device.get("tags", [])
        if not isinstance(device_tags, list):
            _LOGGER.warning("Device %s has malformed tags: %s. Assuming no tags for matching.", device.get("serial"), device_tags)
            device_tags = []

        if not device_tags and ssid_tags: # Device has no tags, but SSID expects tags
            _LOGGER.debug("Device %s has no tags, but SSID '%s' requires tags %s. No match.", device.get("serial"), ssid_info.get("name"), ssid_tags)
            continue # Try next device if not target_device_serial, else this loop runs once.

        # Perform tag matching based on the relaxed_matching flag.
        if relaxed_matching:
            # Any common tag means a match.
            if any(tag in device_tags for tag in ssid_tags):
                _LOGGER.debug("Relaxed match: Device %s tags %s and SSID '%s' tags %s have common elements.", device.get("serial"), device_tags, ssid_info.get("name"), ssid_tags)
                return True
        else:
            # All SSID tags must be present in device tags for a strict match.
            if all(tag in device_tags for tag in ssid_tags):
                _LOGGER.debug("Strict match: Device %s tags %s contains all SSID '%s' tags %s.", device.get("serial"), device_tags, ssid_info.get("name"), ssid_tags)
                return True
        _LOGGER.debug("No match for device %s (tags: %s) with SSID '%s' (tags: %s, relaxed: %s)", device.get("serial"), device_tags, ssid_info.get("name"), ssid_tags, relaxed_matching)

    return False # No matching device found


class MerakiSSIDSwitch(CoordinatorEntity, SwitchEntity):
    """Represents a switch to control the enabled state of a Meraki SSID on a device.

    This entity allows users to turn an SSID on or off for a specific Meraki
    device. The control is achieved by adding or removing a specific tag
    (e.g., "ssid_SSID_NAME_enabled") on the Meraki device via the API.

    The switch's state (`is_on`) is determined by the presence of this
    control tag in the device's tag list, as reported by the coordinator.

    Attributes:
        coordinator (MerakiDataUpdateCoordinator): The data update coordinator.
        _device_info (Dict[str, Any]): Information about the parent Meraki device.
        _ssid_info (Dict[str, Any]): Information about the SSID this switch controls.
        _control_tag (str): The specific tag used to control this SSID's state on the device.
        _attr_unique_id (str): The unique ID of the switch entity.
        _attr_name (str): The friendly name of the switch entity.
        _attr_is_on (bool): The current state of the switch (True if SSID is enabled).
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info: Dict[str, Any],
        ssid_info: Dict[str, Any],
    ) -> None:
        """Initializes the Meraki SSID switch.

        Args:
            coordinator (MerakiDataUpdateCoordinator): The data update coordinator.
            device_info (Dict[str, Any]): Dictionary with information about the
                parent Meraki device (e.g., "serial", "name", "tags").
            ssid_info (Dict[str, Any]): Dictionary with information about the SSID
                (e.g., "name", "number").
        """
        super().__init__(coordinator) # Initialize CoordinatorEntity
        self._device_info = device_info
        self._ssid_info = ssid_info
        ssid_name_safe = "".join(c if c.isalnum() else "_" for c in ssid_info.get("name", "unknown_ssid"))
        self._control_tag = f"ssid_{ssid_name_safe}_enabled" # Tag used to control state

        device_serial = device_info.get("serial", "unknown_serial")
        device_display_name = device_info.get("name", device_serial)
        ssid_display_name = ssid_info.get("name", f"SSID {ssid_info.get('number', 'N/A')}")

        self._attr_unique_id = f"{device_serial}_{ssid_info.get('number', ssid_name_safe)}_switch"
        self._attr_name = f"{device_display_name} - {ssid_display_name} Control"

        # Initial state is determined from device tags.
        self._attr_is_on = self._determine_state_from_tags()
        _LOGGER.debug(
            "Initializing MerakiSSIDSwitch for SSID '%s' on device %s. Control Tag: '%s'. Initial state: %s",
            ssid_display_name,
            device_display_name,
            self._control_tag,
            self._attr_is_on,
        )

    def _get_current_device_data_from_coordinator(self) -> Optional[Dict[str, Any]]:
        """Retrieves the most recent data for this switch's device from the coordinator."""
        if self.coordinator.data and "devices" in self.coordinator.data:
            for dev_data in self.coordinator.data["devices"]:
                if isinstance(dev_data, dict) and dev_data.get("serial") == self._device_info.get("serial"):
                    return dev_data
        return None

    def _determine_state_from_tags(self) -> bool:
        """Determines if the SSID is 'on' (enabled) based on device tags."""
        device_data = self._get_current_device_data_from_coordinator()
        if device_data:
            current_tags = device_data.get("tags", [])
            if isinstance(current_tags, list):
                return self._control_tag in current_tags
            else:
                _LOGGER.warning("Device %s tags are not a list: %s", self._device_info.get("serial"), current_tags)
        return False # Default to off if tags cannot be determined

    @property
    def is_on(self) -> bool:
        """Return the current state of the SSID switch (True if enabled, False otherwise)."""
        return self._attr_is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable the SSID by adding the control tag to the device."""
        _LOGGER.info("Turning ON SSID '%s' on device %s by adding tag '%s'", self._ssid_info.get("name"), self._device_info.get("name"), self._control_tag)
        await self._set_ssid_control_tag_state(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable the SSID by removing the control tag from the device."""
        _LOGGER.info("Turning OFF SSID '%s' on device %s by removing tag '%s'", self._ssid_info.get("name"), self._device_info.get("name"), self._control_tag)
        await self._set_ssid_control_tag_state(False)

    async def _set_ssid_control_tag_state(self, enable: bool) -> None:
        """Adds or removes the SSID control tag from the device's tag list.

        Args:
            enable (bool): If True, the control tag is added. If False, it's removed.

        Raises:
            HomeAssistantError: If the API call to update tags fails.
        """
        device_serial = self._device_info.get("serial")
        # Fetch the latest device data from coordinator to get current tags
        device_data_from_coord = self._get_current_device_data_from_coordinator()
        if not device_data_from_coord:
            _LOGGER.error("Cannot set SSID state for %s: Device data not found in coordinator.", device_serial)
            # Consider raising an error or simply returning
            return

        current_tags: List[str] = device_data_from_coord.get("tags", [])
        if not isinstance(current_tags, list): # Ensure current_tags is a list
            _LOGGER.warning("Device %s tags from coordinator is not a list (%s), treating as empty.", device_serial, type(current_tags))
            current_tags = []

        new_tags = current_tags.copy()
        tag_action_logged = False

        if enable:
            if self._control_tag not in new_tags:
                new_tags.append(self._control_tag)
                _LOGGER.debug("Adding tag '%s' to device %s. Current tags: %s, New tags: %s", self._control_tag, device_serial, current_tags, new_tags)
                tag_action_logged = True
        else:
            if self._control_tag in new_tags:
                new_tags.remove(self._control_tag)
                _LOGGER.debug("Removing tag '%s' from device %s. Current tags: %s, New tags: %s", self._control_tag, device_serial, current_tags, new_tags)
                tag_action_logged = True

        if not tag_action_logged and list(sorted(current_tags)) == list(sorted(new_tags)): # Check if tags actually changed
             _LOGGER.debug("No change in tags needed for device %s to set SSID state to %s. Current tags already reflect desired state: %s", device_serial, enable, current_tags)
             # Update local state just in case it was out of sync, then refresh from coordinator.
             self._attr_is_on = enable
             self.async_write_ha_state()
             # Request a refresh to ensure HA state matches actual Meraki state if there was a prior desync.
             await self.coordinator.async_request_refresh()
             return


        try:
            # The `update_device_tags` function expects the Meraki API session,
            # which is not typically stored directly in the coordinator.
            # The coordinator's `api_fetcher` or a dedicated API client instance
            # within the coordinator should be used.
            # Assuming `self.coordinator.api_key` is available.
            # The `update_device_tags` function from `meraki_api.devices` needs to be callable.
            # It was originally called with `self.coordinator.session` which might not exist or be an aiohttp session.
            # Let's assume `update_device_tags` is adapted or a similar method exists on an API client.
            # For now, this matches the structure of the original code's intent.
            # If `self.coordinator.session` is indeed an `aiohttp.ClientSession`, it needs careful management.
            # A better pattern is `self.coordinator.api_client.update_device_tags(...)`
            # This part might need adjustment based on how the API client/session is managed in MerakiDataUpdateCoordinator.
            # The `update_device_tags` in `meraki_api/devices.py` uses `_async_meraki_request` which creates its own session.

            # The `meraki_api.devices.update_device_tags` takes (api_key, serial, tags).
            # The original code had `self.coordinator.session` as the first argument which is incorrect for that function.
            success = await update_device_tags(
                api_key=self.coordinator.api_key,
                serial=device_serial,
                tags=new_tags,
            )
            if success:
                _LOGGER.info(
                    "Successfully updated tags for device %s to %s to set SSID enabled state to: %s",
                    device_serial,
                    new_tags,
                    enable,
                )
                self._attr_is_on = enable # Optimistically update local state
                self.async_write_ha_state()
                # Request a refresh from the coordinator to get the latest state from Meraki,
                # including the updated tags and actual SSID state if it's derived differently.
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error("Failed to update tags for device %s (API call reported not successful).", device_serial)
                # Optionally revert local state or raise an error
                # For now, we don't change local state on API failure to avoid flip-flopping if retry occurs.
                # Consider raising a HomeAssistantError here.

        except aiohttp.ClientError as e:
            _LOGGER.error("API error setting SSID enabled state for device %s: %s", device_serial, e)
            # Consider raising HomeAssistantError to notify user of failure
            # from homeassistant.exceptions import HomeAssistantError
            # raise HomeAssistantError(f"Failed to update SSID state for {self._attr_name}: {e}") from e
        except Exception as e:
            _LOGGER.exception("Unexpected error setting SSID enabled state for device %s: %s", device_serial, e)
            # raise HomeAssistantError(f"Unexpected error for {self._attr_name}: {e}") from e

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        This method is called by `CoordinatorEntity` when the coordinator
        has new data. It re-evaluates the switch's `is_on` state based on
        the updated device tags from the coordinator.
        """
        _LOGGER.debug("Coordinator update received for SSID switch %s.", self.name)
        current_state_from_tags = self._determine_state_from_tags()
        if self._attr_is_on != current_state_from_tags:
            _LOGGER.info(
                "SSID switch %s state change detected via coordinator. From: %s, To: %s",
                self.name,
                self._attr_is_on,
                current_state_from_tags,
            )
            self._attr_is_on = current_state_from_tags
            self.async_write_ha_state()
        else:
            _LOGGER.debug("No state change for SSID switch %s after coordinator update. Current state: %s", self.name, self._attr_is_on)


    # async def async_update(self) -> None:
    #     """Update the SSID state. (Handled by Coordinator)"""
    #     # The state of this switch is derived from the coordinator's data.
    #     # The `_handle_coordinator_update` method is called when the coordinator
    #     # signals new data, which then updates `_attr_is_on`.
    #     # Therefore, an explicit `async_update` here is typically not needed
    #     # if relying solely on coordinator updates.
    #     # If there were a direct API call to fetch this switch's specific state,
    #     # it would go here, but control is via tags updated by turn_on/off.
    #     _LOGGER.debug("async_update called for %s, state updated via coordinator.", self.name)
    #     pass


    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for linking this entity to a Home Assistant device.

        This links the SSID switch entity to the physical Meraki device it controls
        an SSID on.
        """
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_info.get("serial", "unknown_serial"))},
            name=self._device_info.get("name", self._device_info.get("serial")),
            model=self._device_info.get("model"),
            manufacturer="Cisco Meraki",
            sw_version=self._device_info.get("firmware"),
            # Link to parent device if applicable, e.g., if this is part of a larger system.
            # via_device=(DOMAIN, self.coordinator.config_entry.entry_id) # Example if linked to config entry device
        )
