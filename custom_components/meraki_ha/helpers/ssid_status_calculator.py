"""Helper module to calculate the operational status of Meraki SSIDs.

This module provides the `SsidStatusCalculator` class, containing static
methods to determine an SSID's operational status (e.g., online, offline,
partially_online). This status is based on the state and tags of associated
Meraki wireless access points (MR series devices).
"""
import logging
from typing import Any, Dict, List, Optional

_LOGGER = logging.getLogger(__name__)


class SsidStatusCalculator:
    """Calculates the operational status of Meraki SSIDs.

    This class uses static methods to evaluate SSID status by correlating
    SSID configurations (especially tags) with the current state and tags
    of relevant Meraki wireless access points (APs).
    """

    @staticmethod
    def calculate_ssid_status(
        ssids: Optional[List[Dict[str, Any]]],
        devices: Optional[List[Dict[str, Any]]], # Device list; tags are expected within each device dict.
        # The `device_tags` parameter (previously a separate dict) has been removed.
        relaxed_tag_match: bool,
    ) -> List[Dict[str, Any]]:
        """Calculate the operational status of each SSID provided.

        The status of an SSID is determined by the state of the wireless access
        points (APs) that are tagged to broadcast it. The rules are:
        - 'disabled': If the SSID itself is administratively disabled.
        - 'no_matching_devices': If no APs are tagged to broadcast this SSID.
        - 'online': If all APs tagged for this SSID are online.
        - 'partially_online': If some, but not all, APs tagged for this SSID are online.
        - 'offline': If all APs tagged for this SSID are offline (or in an unknown state).
        - 'unknown_device_data_missing': If the `devices` list is None, preventing status calculation.

        Args:
            ssids: A list of SSID dictionaries. Each dictionary should contain
                   at least 'id', 'name', 'enabled', and optionally 'tags' (a list of strings).
            devices: A list of Meraki device dictionaries. Each dictionary for an AP
                     should contain 'serial', 'status' (e.g., "online"), 'model',
                     and 'tags' (a list of strings).
            relaxed_tag_match: A boolean. If True, an AP matches if it shares
                               any tag with the SSID. If False (strict mode), an AP
                               matches only if it has all tags listed on the SSID.

        Returns:
            A list of SSID dictionaries, each updated with new keys:
            'matching_devices_online' (count), 'matching_devices_total' (count),
            and 'status' (string). Returns an empty list if the input `ssids`
            is None or empty.
        """
        if not ssids: # Handles None or empty list for ssids.
            _LOGGER.debug(
                "SSID data is None or empty in calculate_ssid_status; returning empty list."
            )
            return []

        if devices is None: # Handles case where device data is missing.
            _LOGGER.warning(
                "Device data is None in calculate_ssid_status. SSID statuses cannot be determined accurately. "
                "Marking SSIDs as 'unknown_device_data_missing'."
            )
            for ssid in ssids:
                ssid["status"] = "unknown_device_data_missing" # Add status field.
            return ssids
        
        # Comment about device_tags being None is removed as parameter is gone.

        _LOGGER.debug(
            "Calculating SSID status for %d SSIDs using %d devices. Relaxed tag match: %s.",
            len(ssids),
            len(devices),
            relaxed_tag_match,
        )

        updated_ssids_list: List[Dict[str, Any]] = []
        for ssid_info in ssids:
            if not isinstance(ssid_info, dict):
                _LOGGER.warning("Skipping non-dictionary SSID item: %s", ssid_info)
                continue

            ssid_id = ssid_info.get("id")
            ssid_number = ssid_info.get("number")
            ssid_name = ssid_info.get("name", f"Unnamed SSID ({ssid_id or ssid_number})")
            is_enabled = ssid_info.get("enabled", False)
            # Tags defined on the SSID configuration.
            ssid_configured_tags: List[str] = ssid_info.get("tags", [])

            _LOGGER.debug(
                "Processing SSID: Name='%s' (ID: %s, Number: %s), Enabled: %s, Configured Tags: %s",
                ssid_name, ssid_id, ssid_number, is_enabled, ssid_configured_tags,
            )

            matching_devices_online_count = 0
            matching_devices_total_count = 0

            for device_info in devices:
                if not isinstance(device_info, dict):
                    _LOGGER.warning("Skipping non-dictionary device item: %s", device_info)
                    continue

                device_model: str = device_info.get("model", "")
                # Consider only Meraki Wireless Access Points (MR series) for SSID status.
                if device_model.upper().startswith("MR"):
                    device_serial: Optional[str] = device_info.get("serial")
                    device_status: str = device_info.get("status", "unknown").lower()
                    # Device tags are now expected to be directly within the device_info dictionary.
                    current_device_tags: List[str] = device_info.get("tags", [])

                    _LOGGER.debug(
                        "  Checking Wireless AP: Serial=%s, Status='%s', Model='%s', AP Tags=%s",
                        device_serial, device_status, device_model, current_device_tags,
                    )

                    if SsidStatusCalculator._does_device_match_ssid_tags(
                        ssid_configured_tags, # Tags from SSID config.
                        current_device_tags,  # Tags from the AP device itself.
                        relaxed_tag_match,
                    ):
                        matching_devices_total_count += 1
                        if device_status == "online":
                            matching_devices_online_count += 1
                        _LOGGER.debug("    AP (Serial: %s) matches SSID tag criteria.", device_serial)
                    else:
                        _LOGGER.debug("    AP (Serial: %s) does not match SSID tag criteria.", device_serial)
                # else: # Devices not starting with "MR" are ignored for SSID calculation.
                    # _LOGGER.debug("    Device (Serial: %s, Model: %s) is not an MR AP; skipping.",
                    # device_info.get("serial"), device_model)

            ssid_info["matching_devices_online"] = matching_devices_online_count
            ssid_info["matching_devices_total"] = matching_devices_total_count

            if not is_enabled:
                ssid_info["status"] = "disabled"
            elif matching_devices_total_count == 0:
                ssid_info["status"] = "no_matching_devices"
            elif matching_devices_online_count == matching_devices_total_count:
                ssid_info["status"] = "online"
            elif matching_devices_online_count > 0:
                ssid_info["status"] = "partially_online"
            else: # matching_devices_total_count > 0 but matching_devices_online_count == 0
                ssid_info["status"] = "offline"

            _LOGGER.debug(
                "  SSID '%s' (ID: %s) final status: '%s' (Online APs: %d / Total Matching APs: %d)",
                ssid_name, ssid_id, ssid_info["status"],
                matching_devices_online_count, matching_devices_total_count,
            )
            updated_ssids_list.append(ssid_info)

        _LOGGER.debug(
            "SSID status calculation complete. Processed and updated %d SSIDs.",
            len(updated_ssids_list),
        )
        return updated_ssids_list

    @staticmethod
    def _does_device_match_ssid_tags(
        ssid_tags: List[str],       # Tags defined on the SSID configuration.
        device_actual_tags: List[str], # Tags physically on the device.
        relaxed_tag_match: bool,
    ) -> bool:
        """Determine if a device's tags match an SSID's tags based on the matching strategy.

        Args:
            ssid_tags: A list of tags associated with the SSID from its configuration.
            device_actual_tags: A list of tags currently on the device.
            relaxed_tag_match: If True, the device matches if it shares at least one tag
                               with the SSID. If False (strict mode), the device matches
                               only if it possesses all tags listed in the SSID's configuration.

        Returns:
            True if the device's tags meet the SSID's tag requirements, False otherwise.
        """
        # If an SSID has no tags defined in its configuration, it implies it should be
        # broadcast by all APs (that are capable, e.g. in the same network, though network
        # association is handled elsewhere). So, any device is a match from a tag perspective.
        if not ssid_tags:
            return True

        # If the SSID configuration requires specific tags, but the device itself has no tags,
        # it cannot fulfill the requirement, regardless of matching mode (strict or relaxed).
        if not device_actual_tags:
            return False

        # Normalize tags to lowercase for case-insensitive comparison. This ensures that
        # "Office" and "office" are treated as the same tag.
        ssid_tags_lower = {tag.lower() for tag in ssid_tags}
        device_tags_lower = {tag.lower() for tag in device_actual_tags}

        if relaxed_tag_match:
            # Relaxed mode: Returns True if there's any overlap (intersection)
            # between the SSID's configured tags and the device's actual tags.
            # `isdisjoint()` returns True if the sets have NO common elements.
            return not ssid_tags_lower.isdisjoint(device_tags_lower)
        else:
            # Strict mode: Returns True only if all tags specified in the SSID's
            # configuration are present on the device. This means the set of
            # SSID tags must be a subset of (or equal to) the device's tags.
            return ssid_tags_lower.issubset(device_tags_lower)
