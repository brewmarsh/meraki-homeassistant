"""Helper module to calculate the operational status of Meraki SSIDs.

This module provides the `SsidStatusCalculator` class, which determines an SSID's
status (e.g., online, offline, partially_online) based on the status and tags
of associated Meraki wireless access points (MR series devices).
"""
import logging
from typing import Any, Dict, List, Optional # Added Optional and Any

_LOGGER = logging.getLogger(__name__)


class SsidStatusCalculator:
    """Calculates the operational status of Meraki SSIDs.

    This class contains static methods to evaluate SSID status by correlating
    SSID configurations with the state of relevant Meraki access points.
    """

    @staticmethod
    def calculate_ssid_status(
        ssids: Optional[List[Dict[str, Any]]],
        devices: Optional[List[Dict[str, Any]]],
        device_tags: Optional[Dict[str, List[str]]], # device_serial -> list of tags
        relaxed_tag_match: bool,
    ) -> List[Dict[str, Any]]:
        """Calculate the status of each SSID.

        The status is determined by checking associated wireless access points (APs).
        An SSID is 'online' if all matching APs are online.
        It's 'partially_online' if some matching APs are online.
        It's 'offline' if all matching APs are offline.
        It's 'no_matching_devices' if no APs match its tags.
        It's 'disabled' if the SSID itself is not enabled.

        Args:
            ssids: A list of SSID dictionaries. Each SSID dict should have 'id',
                   'name', 'enabled', and optionally 'tags'.
            devices: A list of Meraki device dictionaries. Each device dict should
                     have 'serial', 'status', 'model', and potentially 'tags'
                     (though tags are passed separately in `device_tags`).
            device_tags: A dictionary mapping device serial numbers to a list of
                         their assigned tags.
            relaxed_tag_match: A boolean indicating whether to use relaxed tag
                               matching (any common tag) or strict tag matching
                               (all SSID tags must be on device).

        Returns:
            A list of SSID dictionaries, each updated with new keys:
            'matching_devices_online', 'matching_devices_total', and 'status'.
            Returns an empty list if input `ssids` is None or empty.
        """
        # If there are no SSIDs to process, return an empty list immediately.
        if not ssids: # Handles None or empty list for ssids
            _LOGGER.debug("SSID data is None or empty in calculate_ssid_status, returning empty list.")
            return []
        # If device data is missing, we cannot accurately determine SSID status based on devices.
        # Log a warning and return the original SSIDs, possibly with an 'unknown' status.
        if devices is None: # devices can be empty list, but None is problematic
            _LOGGER.warning("Device data is None in calculate_ssid_status, returning original SSIDs without status.")
            # Iterate through the SSIDs and assign a default status indicating missing device data.
            for ssid in ssids:
                ssid["status"] = "unknown_device_data_missing"
            return ssids
        # If device_tags is None (e.g., an error fetching tags), default to an empty dictionary.
        # This assumes devices have no tags, which might affect matching logic.
        if device_tags is None:
            _LOGGER.warning("Device tags data is None in calculate_ssid_status. Assuming no devices have tags.")
            device_tags = {}  # Treat as no tags for any device

        _LOGGER.debug(
            "Calculating SSID status for %d SSIDs, %d devices, relaxed_match: %s",
            len(ssids), # Total number of SSIDs to process.
            len(devices), # Total number of devices to consider for matching.
            relaxed_tag_match, # The tag matching strategy being used.
        )

        updated_ssids_list: List[Dict[str, Any]] = [] # List to store SSIDs with updated status.
        # Iterate over each SSID to calculate its status.
        for ssid_info in ssids: # Use a more descriptive variable name
            # Basic validation: ensure the SSID item is a dictionary.
            if not isinstance(ssid_info, dict):
                _LOGGER.warning("Skipping non-dictionary SSID item: %s", ssid_info)
                continue # Skip to the next SSID if data is malformed.

            # Extract relevant information from the SSID dictionary.
            # Provide defaults or generate identifiers if essential keys are missing.
            ssid_id = ssid_info.get("id") # Meraki's unique ID for the SSID, if available.
            ssid_number = ssid_info.get("number") # The SSID number (0-14 for MR devices).
            ssid_name = ssid_info.get("name", f"Unnamed SSID {ssid_number or ssid_id}") # SSID name, fallback if missing.
            is_enabled = ssid_info.get("enabled", False) # SSID's configured administrative state.
            ssid_explicit_tags: List[str] = ssid_info.get("tags", []) # Tags assigned to this SSID for AP matching.

            _LOGGER.debug(
                "Processing SSID: Name='%s' (ID: %s, Num: %s), Enabled=%s, Tags=%s",
                ssid_name, # Name of the current SSID being processed.
                ssid_id,   # Meraki ID of the SSID.
                ssid_number, # Number of the SSID.
                is_enabled, # Whether the SSID is administratively enabled.
                ssid_explicit_tags, # Tags configured on the SSID.
            )

            # Counters for APs that match this SSID's tag criteria.
            matching_devices_online_count = 0 # Number of matching APs currently online.
            matching_devices_total_count = 0  # Total number of APs matching the tags.

            # Iterate through all available devices to find matching wireless APs.
            for device_info in devices:
                # Basic validation for device item.
                if not isinstance(device_info, dict):
                    _LOGGER.warning("Skipping non-dictionary device item: %s", device_info)
                    continue # Skip if data is malformed.

                # Extract device details.
                device_serial: Optional[str] = device_info.get("serial")
                device_model: str = device_info.get("model", "") # Device model (e.g., "MR52").
                # Device status (e.g., "online", "offline"). Normalize to lowercase for consistent comparison.
                device_status: str = device_info.get("status", "unknown").lower()


                # We are only interested in Meraki Wireless Access Points (APs) for SSID status.
                # Their models typically start with "MR".
                if device_model.upper().startswith("MR"):
                    # Get the tags for the current device from the `device_tags` dictionary.
                    # Default to an empty list if the device has no tags or serial is missing.
                    current_device_tags: List[str] = device_tags.get(device_serial, []) if device_serial else []
                    _LOGGER.debug(
                        "  Checking Wireless AP: Serial=%s, Status='%s', Model='%s', Tags=%s",
                        device_serial,       # Serial of the AP.
                        device_status,       # Current status (e.g., "online").
                        device_model,        # Model of the AP.
                        current_device_tags, # Tags on this AP.
                    )
                    # Check if this AP's tags match the SSID's tags based on the matching strategy.
                    if SsidStatusCalculator._does_device_match_ssid_tags(
                        ssid_explicit_tags, current_device_tags, relaxed_tag_match
                    ):
                        matching_devices_total_count += 1 # Increment total count of APs that should broadcast this SSID.
                        # If the matching AP is online, increment the online counter.
                        if device_status == "online":
                            matching_devices_online_count += 1
                        _LOGGER.debug("    Wireless AP matches SSID tag criteria.")
                    else:
                        _LOGGER.debug("    Wireless AP does not match SSID tag criteria.")
                else:
                    # Log if a device is not an MR model, as it won't be considered for SSID status.
                    _LOGGER.debug(
                        "    Device (Serial: %s, Model: %s) is not a Wireless AP, skipping for SSID status.",
                        device_serial,
                        device_model,
                    )
            # After checking all devices, store the counts in the SSID's dictionary.
            ssid_info["matching_devices_online"] = matching_devices_online_count
            ssid_info["matching_devices_total"] = matching_devices_total_count

            # Determine the final status string for the SSID based on its 'enabled' state and matching APs.
            if not is_enabled:
                # If the SSID is administratively disabled in Meraki config.
                ssid_info["status"] = "disabled"
            elif matching_devices_total_count == 0:
                # If no APs are tagged to broadcast this SSID.
                ssid_info["status"] = "no_matching_devices"
            elif matching_devices_online_count == matching_devices_total_count:
                # All APs tagged for this SSID are online.
                ssid_info["status"] = "online"
            elif matching_devices_online_count > 0:
                # Some, but not all, APs tagged for this SSID are online.
                ssid_info["status"] = "partially_online"
            else: # This means matching_devices_total_count > 0 but matching_devices_online_count == 0
                # All APs tagged for this SSID are offline or in an unknown state.
                ssid_info["status"] = "offline"

            _LOGGER.debug("  SSID '%s' final status: %s (Online: %d, Total: %d)",
                          ssid_name, ssid_info["status"], matching_devices_online_count, matching_devices_total_count)
            updated_ssids_list.append(ssid_info) # Add the updated SSID info to the list.

        _LOGGER.debug("SSID status calculation complete. Updated SSIDs: %d", len(updated_ssids_list))
        return updated_ssids_list # Return the list of SSIDs with their calculated statuses.

    @staticmethod
    def _does_device_match_ssid_tags( # Renamed for clarity
        ssid_tags: List[str], device_actual_tags: List[str], relaxed_tag_match: bool
    ) -> bool:
        """Check if a device's tags match an SSID's tags based on matching mode.

        Args:
            ssid_tags: A list of tags associated with the SSID.
            device_actual_tags: A list of tags associated with the device.
            relaxed_tag_match: If True, requires any common tag. If False,
                               requires all SSID tags to be present on the device.

        Returns:
            True if the device matches the SSID's tag criteria, False otherwise.
        """
        # If the SSID has no tags defined, it is considered a "broadcast everywhere" SSID.
        # Therefore, any device (AP) is considered a match for broadcasting it.
        if not ssid_tags:
            return True

        # If the SSID requires tags, but the device itself has no tags, it cannot match.
        # This applies to both strict and relaxed modes because there are no device tags
        # to satisfy either "all SSID tags" or "any SSID tags".
        if not device_actual_tags:
            return False

        # Normalize tags to lowercase for case-insensitive comparison.
        # This prevents mismatches due to inconsistent casing (e.g., "Guest" vs "guest").
        ssid_tags_lower = {tag.lower() for tag in ssid_tags}
        device_tags_lower = {tag.lower() for tag in device_actual_tags}

        if relaxed_tag_match:
            # Relaxed mode: True if there is at least one common tag between SSID and device.
            # `isdisjoint` returns True if the sets have no elements in common.
            # So, `not isdisjoint` means there is at least one common element.
            return not ssid_tags_lower.isdisjoint(device_tags_lower)
        else:
            # Strict mode: True if all tags defined on the SSID are present on the device.
            # This means the set of SSID tags must be a subset of the device's tags.
            return ssid_tags_lower.issubset(device_tags_lower)
