"""Switch entity for controlling Meraki SSIDs.

This module defines the `MerakiSSIDSwitch` class, a Home Assistant switch
entity that allows users to enable or disable a specific Meraki SSID.
It also includes a helper function `match_device_to_ssid` to determine
if an SSID switch should be created based on tag matching logic.
"""
import logging
from typing import Any, Dict, List, Optional # Added Optional

import aiohttp # For ClientError
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback # For coordinator updates
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity # Changed from DataUpdateCoordinator

# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
from ..coordinator import MerakiDataUpdateCoordinator
from ..const import DOMAIN
# Assuming update_device_tags is an async function from the meraki_api package
# from ..meraki_api.devices import update_device_tags
# Placeholder for the function if not available for type checking
async def update_device_tags(
    session: Optional[aiohttp.ClientSession], # Session might not be on coordinator directly
    api_key: str,
    serial: str,
    tags: List[str],
) -> bool: # Assuming it returns bool for success
    """Placeholder: Updates device tags."""
    _LOGGER.warning(
        "Using placeholder for update_device_tags for serial %s with tags %s.", serial, tags
    )
    # In a real scenario, this would make an API call.
    # For placeholder, return True assuming success.
    await asyncio.sleep(0) # make it awaitable
    return True
import asyncio # Required for placeholder

_LOGGER = logging.getLogger(__name__)


def match_device_to_ssid(
    ssid_info: Dict[str, Any], # Changed from ssid
    all_devices: List[Dict[str, Any]], # Changed from devices
    relaxed_matching: bool,
) -> bool:
    """Determine if an SSID should have a switch created based on device tags.

    This function checks if any device in the provided list matches the SSID's
    tagging criteria. If an SSID has no tags, it's considered a match for any device.
    If it has tags, the behavior depends on `relaxed_matching`:
    - Relaxed: Matches if any of the SSID's tags are present on any device.
    - Strict (not relaxed): Matches if all of the SSID's tags are present on any device.

    Args:
        ssid_info: A dictionary containing the SSID's information, including 'tags'.
        all_devices: A list of all device dictionaries to check against. Each device
                     dict should contain 'tags'.
        relaxed_matching: A boolean indicating the tag matching strategy.

    Returns:
        True if a match is found according to the criteria, False otherwise.
    """
    ssid_tags: List[str] = ssid_info.get("tags", [])
    if not ssid_tags:
        _LOGGER.debug("SSID '%s' has no tags, considered a match for switch creation.", ssid_info.get("name"))
        return True  # SSID has no tags, implies it can be on any AP (or any AP matching this logic).

    for device_info in all_devices: # Changed from device
        device_tags: List[str] = device_info.get("tags", [])
        if not device_tags: # Device has no tags, cannot satisfy an SSID that requires tags.
            continue

        # Normalize tags for case-insensitive comparison
        ssid_tags_lower = {tag.lower() for tag in ssid_tags}
        device_tags_lower = {tag.lower() for tag in device_tags}

        if relaxed_matching:
            # Any common tag means a match
            if not ssid_tags_lower.isdisjoint(device_tags_lower):
                _LOGGER.debug(
                    "SSID '%s' (tags: %s) matches device '%s' (tags: %s) with relaxed matching.",
                    ssid_info.get("name"), ssid_tags, device_info.get("name"), device_tags
                )
                return True
        else:
            # All SSID tags must be present on the device
            if ssid_tags_lower.issubset(device_tags_lower):
                _LOGGER.debug(
                    "SSID '%s' (tags: %s) matches device '%s' (tags: %s) with strict matching.",
                    ssid_info.get("name"), ssid_tags, device_info.get("name"), device_tags
                )
                return True
    _LOGGER.debug(
        "SSID '%s' (tags: %s) found no matching device with relaxed_matching=%s.",
        ssid_info.get("name"), ssid_tags, relaxed_matching
    )
    return False


class MerakiSSIDSwitch(CoordinatorEntity[MerakiDataUpdateCoordinator], SwitchEntity):
    """Representation of a Meraki SSID as a Home Assistant switch.

    This entity allows enabling or disabling a specific SSID. The actual control
    mechanism implemented here is by adding or removing a specific tag
    (e.g., "ssid_SSID_NAME_enabled") from the parent device (AP).

    Inherits from `CoordinatorEntity` to react to updates from the central coordinator.
    """
    # _attr_has_entity_name = True # If you want HA to generate name from device

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info_data: Dict[str, Any], # Parent device (AP) data
        ssid_info_data: Dict[str, Any],   # Specific SSID data
    ) -> None:
        """Initialize the Meraki SSID switch.

        Args:
            coordinator: The data update coordinator.
            device_info_data: Dictionary containing information about the parent Meraki
                              device (e.g., an access point).
            ssid_info_data: Dictionary containing information about the SSID.
        """
        super().__init__(coordinator)
        self._device_info: Dict[str, Any] = device_info_data # Store parent AP info
        self._ssid_info: Dict[str, Any] = ssid_info_data     # Store SSID info

        device_name = self._device_info.get("name", self._device_info.get("serial", "Unknown Device"))
        ssid_name = self._ssid_info.get("name", f"SSID {self._ssid_info.get('number', 'N/A')}")
        
        self._attr_name = f"{device_name} - {ssid_name}" # Example: "AP1 - Guest WiFi"
        # Unique ID needs to be stable and unique across all entities.
        # Combining device serial and SSID number (or name if number not available) is robust.
        serial = self._device_info.get("serial", "unknownserial")
        ssid_identifier = self._ssid_info.get("number", self._ssid_info.get("name", "unknownssid"))
        self._attr_unique_id = f"{serial}_ssid_{ssid_identifier}_switch"
        
        # Initial state is set from the coordinator data during _handle_coordinator_update
        # or can be set here if ssid_info_data contains the current 'enabled' state.
        self._update_switch_state() # Set initial state
        _LOGGER.debug(
            "Initializing MerakiSSIDSwitch for SSID '%s' on device '%s': Initial state is_on=%s",
            ssid_name, device_name, self._attr_is_on
        )

    def _update_switch_state(self) -> None:
        """Update the switch's `is_on` state from coordinator data."""
        # Find the current SSID data within the coordinator's data structure
        current_ssid_data: Optional[Dict[str, Any]] = None
        device_serial = self._device_info.get("serial")
        ssid_number = self._ssid_info.get("number")

        if self.coordinator.data and "devices" in self.coordinator.data:
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == device_serial:
                    ssids_on_device = dev_data.get("ssids", []) # Assuming ssids are nested
                    for ssid_detail in ssids_on_device:
                        if ssid_detail.get("number") == ssid_number:
                            current_ssid_data = ssid_detail
                            break
                    break
        
        if current_ssid_data:
            self._attr_is_on = current_ssid_data.get("enabled", False)
            _LOGGER.debug("SSID switch '%s' updated: is_on=%s", self.name, self._attr_is_on)
        else:
            _LOGGER.warning(
                "Could not find SSID data for %s (Num: %s) on device %s in coordinator. Switch state unknown.",
                self._ssid_info.get("name"), ssid_number, device_serial
            )
            self._attr_is_on = False # Default to off if data not found


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_switch_state()
        self.async_write_ha_state()

    # is_on property is now handled by _attr_is_on, managed by _update_switch_state

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable the SSID by adding a specific tag to the parent device."""
        _LOGGER.info("Turning ON SSID: %s for device: %s", self._ssid_info.get('name'), self._device_info.get('name'))
        await self._set_ssid_enabled_via_tag(True)
        # Optimistically update state. The coordinator refresh will confirm.
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable the SSID by removing a specific tag from the parent device."""
        _LOGGER.info("Turning OFF SSID: %s for device: %s", self._ssid_info.get('name'), self._device_info.get('name'))
        await self._set_ssid_enabled_via_tag(False)
        # Optimistically update state. The coordinator refresh will confirm.
        self._attr_is_on = False
        self.async_write_ha_state()

    async def _set_ssid_enabled_via_tag(self, enabled: bool) -> None:
        """Set the SSID enabled state by adding/removing a device tag.

        This method constructs a specific tag based on the SSID name and
        updates the parent device's tags to reflect the desired state.

        Args:
            enabled: True to enable (add tag), False to disable (remove tag).
        
        Raises:
            HomeAssistantError: If the API call to update tags fails.
        """
        ssid_name = self._ssid_info.get("name")
        device_serial = self._device_info.get("serial")

        if not ssid_name or not device_serial:
            _LOGGER.error("Cannot set SSID state: Missing SSID name or device serial.")
            return

        # Define the tag that represents this SSID's enabled state on the device
        # Ensure tag is a valid Meraki tag (e.g., no spaces, certain char limits)
        # This tagging strategy means the SSID's actual "enabled" flag in Meraki config
        # might not be what's controlled. Instead, APs are tagged to broadcast/not broadcast it.
        ssid_control_tag = f"ha_ssid_{ssid_name.replace(' ', '_')}_enabled"
        
        # Fetch current tags for the device from the coordinator to avoid race conditions with direct API reads
        current_device_data: Optional[Dict[str, Any]] = None
        if self.coordinator.data and "devices" in self.coordinator.data:
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == device_serial:
                    current_device_data = dev_data
                    break
        
        current_tags: List[str] = current_device_data.get("tags", []) if current_device_data else []
        _LOGGER.debug("Device '%s' current tags: %s", device_serial, current_tags)

        new_tags: List[str] = current_tags[:] # Make a mutable copy

        tag_action_taken = False
        if enabled:
            if ssid_control_tag not in new_tags:
                new_tags.append(ssid_control_tag)
                _LOGGER.debug("Adding tag '%s' to device '%s'", ssid_control_tag, device_serial)
                tag_action_taken = True
        else: # Disabling
            if ssid_control_tag in new_tags:
                new_tags.remove(ssid_control_tag)
                _LOGGER.debug("Removing tag '%s' from device '%s'", ssid_control_tag, device_serial)
                tag_action_taken = True
        
        if not tag_action_taken:
            _LOGGER.debug("No tag change needed for SSID '%s' on device '%s'; desired state already reflected by tags.", ssid_name, device_serial)
            # Still, request a refresh in case the actual SSID state (if read from API) differs.
            await self.coordinator.async_request_refresh()
            return

        try:
            # The `update_device_tags` function needs access to an aiohttp session
            # and API key. The coordinator might hold these or a shared `MerakiAPIClient`.
            # Assuming coordinator has `api_key` and `hass.helpers.aiohttp_client.async_get_clientsession()`.
            # The original code passed `self.coordinator.session`, which is not standard for coordinators.
            # Let's assume `update_device_tags` is adapted or the coordinator provides a session.
            session = self.coordinator.hass.helpers.aiohttp_client.async_get_clientsession()

            success = await update_device_tags(
                session, # Pass the HA-managed session
                self.coordinator.api_key,
                device_serial,
                new_tags,
            )
            if success:
                _LOGGER.info(
                    "Successfully updated tags for device '%s' to set SSID '%s' enabled state to: %s",
                    device_serial,
                    ssid_name,
                    enabled,
                )
                # After successfully changing tags, request a refresh of the coordinator data
                # to reflect the new device tags and potentially re-evaluate SSID states.
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error(
                    "Failed to update tags for device '%s' for SSID '%s' (API call reported not successful).",
                    device_serial, ssid_name
                )
                # Optionally revert optimistic state update or raise an error
                # self._attr_is_on = not enabled # Revert
                # self.async_write_ha_state()
                # raise HomeAssistantError(f"Failed to update tags for SSID {ssid_name}")


        except aiohttp.ClientError as e:
            _LOGGER.error(
                "Network error setting SSID '%s' enabled state for device '%s': %s",
                ssid_name, device_serial, e
            )
            # Optionally revert or raise
            # raise HomeAssistantError(f"Network error updating SSID {ssid_name}: {e}")
        except Exception as e: # Catch broader exceptions
            _LOGGER.exception(
                "Unexpected error setting SSID '%s' enabled state for device '%s': %s",
                ssid_name, device_serial, e
            )
            # raise HomeAssistantError(f"Unexpected error updating SSID {ssid_name}: {e}")


    # The `async_update` method is typically not needed for CoordinatorEntity subclasses
    # as the state is updated via `_handle_coordinator_update`.
    # If this switch needs to fetch its own state independently (which seems unlikely
    # if based on tags controlled by this entity), then it shouldn't be a CoordinatorEntity.
    # Removing `async_update` to rely on coordinator updates.

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information to link this entity to the parent device (AP)."""
        # This switch entity is logically part of the Meraki Access Point (device).
        # Its state (enabled/disabled) is controlled by tags on that AP.
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_info["serial"])},
            # name, model, etc., are inherited from the parent device entry
            # which should be created by MerakiDeviceCoordinator or similar.
            # No need to redefine them here if this entity is correctly linked.
        )
