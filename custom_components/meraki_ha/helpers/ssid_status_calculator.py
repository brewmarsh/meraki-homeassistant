"""Provides the SsidStatusCalculator for the Meraki Home Assistant integration.

This module defines the `SsidStatusCalculator` class, which includes static
methods to determine the operational (enabled/disabled) status of Meraki SSIDs.
The calculation is based on matching SSID names with tags present on Meraki devices,
allowing for both strict and relaxed tag matching logic.
"""

import logging # Added logging
from typing import Any, Dict, List

_LOGGER = logging.getLogger(__name__)


class SsidStatusCalculator:
    """Calculates the enabled status of SSIDs based on device tags.

    This class provides a static method to iterate through a list of SSIDs
    and determine if each SSID should be considered "enabled". The logic
    relies on checking for specific tags on associated Meraki devices.
    An SSID is marked as enabled if at least one device that is supposed to
    broadcast it (based on tag matching) has the corresponding "enabled" tag.
    """

    @staticmethod
    def calculate_ssid_status(
        ssids: List[Dict[str, Any]],
        devices: List[Dict[str, Any]],
        device_tags_map: Dict[str, List[str]], # Renamed for clarity
        relaxed_tag_match: bool,
    ) -> List[Dict[str, Any]]:
        """Calculates and updates the 'enabled' status for a list of SSIDs.

        For each SSID, this method checks against all provided devices.
        An SSID is considered 'enabled' if:
        - Relaxed matching is True: Any tag on a device contains the SSID name.
        - Relaxed matching is False (strict): A device has a tag exactly matching
          `ssid_{SSID_NAME}_enabled`.

        The 'enabled' key in each SSID dictionary within the `ssids` list is
        updated in place.

        Args:
            ssids (List[Dict[str, Any]]): A list of SSID dictionaries. Each dict
                is expected to have at least a "name" key. This list is modified
                in place.
            devices (List[Dict[str, Any]]): A list of device dictionaries. Each dict
                is expected to have a "serial" key.
            device_tags_map (Dict[str, List[str]]): A dictionary mapping device serial
                numbers to a list of their tags.
            relaxed_tag_match (bool): If True, enables relaxed tag matching where
                the SSID name only needs to be a substring of a device tag.
                If False, requires a specific format (`ssid_{SSID_NAME}_enabled`)
                for the tag.

        Returns:
            List[Dict[str, Any]]: The input `ssids` list, with each SSID dictionary
                potentially updated with an "enabled" status (True or False).
        """
        if not isinstance(ssids, list) or not isinstance(devices, list) or not isinstance(device_tags_map, dict):
            _LOGGER.error(
                "Invalid input types for calculate_ssid_status. ssids: %s, devices: %s, device_tags_map: %s",
                type(ssids), type(devices), type(device_tags_map)
            )
            return ssids # Return original ssids list if inputs are malformed

        _LOGGER.debug(
            "Calculating SSID statuses. SSID count: %d, Device count: %d, Relaxed matching: %s",
            len(ssids), len(devices), relaxed_tag_match
        )

        for ssid_info in ssids:
            if not isinstance(ssid_info, dict) or "name" not in ssid_info:
                _LOGGER.warning("Skipping SSID with missing 'name' or not a dict: %s", ssid_info)
                ssid_info["enabled"] = False # Default to disabled if malformed
                continue

            ssid_name = ssid_info["name"]
            # Sanitize SSID name for tag creation if strict matching,
            # similar to how control tags are formed.
            ssid_name_safe_for_tag = "".join(c if c.isalnum() else "_" for c in ssid_name)
            strict_enabled_tag = f"ssid_{ssid_name_safe_for_tag}_enabled"

            # Default to disabled; will be set to True if matching criteria are met.
            ssid_info["enabled"] = False
            _LOGGER.debug("Processing SSID: '%s'. Initial status: disabled. Strict tag: '%s'", ssid_name, strict_enabled_tag)


            for device_info in devices:
                if not isinstance(device_info, dict) or "serial" not in device_info:
                    _LOGGER.warning("Skipping device with missing 'serial' or not a dict: %s", device_info)
                    continue

                device_serial = device_info["serial"]
                # Get the tags for the current device from the pre-fetched map.
                current_device_tags = device_tags_map.get(device_serial, [])
                if not isinstance(current_device_tags, list):
                    _LOGGER.warning("Tags for device %s are not a list: %s. Treating as no tags.", device_serial, current_device_tags)
                    current_device_tags = []


                if relaxed_tag_match:
                    # Relaxed: SSID name just needs to be part of any tag on the device.
                    if any(ssid_name in tag for tag in current_device_tags):
                        _LOGGER.info(
                            "SSID '%s' enabled on device %s (Relaxed match: found '%s' in tags %s)",
                            ssid_name, device_serial, ssid_name, current_device_tags
                        )
                        ssid_info["enabled"] = True
                        break  # SSID is enabled if found on any one device meeting criteria.
                else:
                    # Strict: Device must have the specific "ssid_{SSID_NAME}_enabled" tag.
                    if strict_enabled_tag in current_device_tags:
                        _LOGGER.info(
                            "SSID '%s' enabled on device %s (Strict match: found tag '%s' in tags %s)",
                            ssid_name, device_serial, strict_enabled_tag, current_device_tags
                        )
                        ssid_info["enabled"] = True
                        break  # SSID is enabled if found on any one device meeting criteria.
            
            if not ssid_info["enabled"]:
                 _LOGGER.debug("SSID '%s' remains disabled after checking all devices.", ssid_name)


        return ssids
