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
        # Device list; tags are expected within each device dict.
        devices: Optional[List[Dict[str, Any]]],
        # The `device_tags` parameter (previously a separate dict) has been
        # removed.
    ) -> List[Dict[str, Any]]:
        """Calculate the operational status of each SSID provided.

        The status of an SSID is determined by the state of the wireless access
        points (APs) that are tagged to broadcast it. The logic is permissive:
        if an SSID has tags, an AP needs to match only one of those tags.
        If an SSID has no tags, any AP is considered a match.

        The rules are:
        - 'disabled': If the SSID itself is administratively disabled.
        - 'no_matching_devices': If no APs are tagged to broadcast this SSID (or match its tags).
        - 'online': If all APs matching this SSID (by tag) are online.
        - 'partially_online': If some, but not all, APs matching this SSID are online.
        - 'offline': If all APs matching this SSID are offline (or in an unknown state).
        - 'unknown_device_data_missing': If the `devices` list is None, preventing status calculation.

        Args:
            ssids: A list of SSID dictionaries. Each dictionary should contain
                   at least 'id', 'name', 'enabled', and optionally 'tags' (a list of strings).
            devices: A list of Meraki device dictionaries. Each dictionary for an AP
                     should contain 'serial', 'status' (e.g., "online"), 'model',
                     and 'tags' (a list of strings).

        Returns:
            A list of SSID dictionaries, each updated with new keys:
            'matching_devices_online' (count), 'matching_devices_total' (count),
            and 'status' (string). Returns an empty list if the input `ssids`
            is None or empty.
        """
        if not ssids:  # Handles None or empty list for ssids.
            _LOGGER.debug(
                "SSID data is None or empty in calculate_ssid_status; returning empty list."
            )
            return []

        if devices is None:  # Handles case where device data is missing.
            _LOGGER.warning(
                "Device data is None in calculate_ssid_status. SSID statuses cannot be determined accurately. "
                "Marking SSIDs as 'unknown_device_data_missing'."
            )
            for ssid in ssids:
                # Add status field.
                ssid["status"] = "unknown_device_data_missing"
            return ssids

        # Comment about device_tags being None is removed as parameter is gone.

        _LOGGER.debug(
            "Calculating SSID status for %d SSIDs using %d devices. Tag matching is permissive (relaxed).",
            len(ssids),
            len(devices),
        )

        updated_ssids_list: List[Dict[str, Any]] = []
        for ssid_info in ssids:
            if not isinstance(ssid_info, dict):
                _LOGGER.warning("Skipping non-dictionary SSID item: %s", ssid_info)
                continue

            ssid_id = ssid_info.get("id")
            ssid_number = ssid_info.get("number")
            ssid_name = ssid_info.get(
                "name", f"Unnamed SSID ({ssid_id or ssid_number})"
            )
            is_enabled = ssid_info.get("enabled", False)
            # Tags defined on the SSID configuration.
            ssid_configured_tags: List[str] = ssid_info.get("tags", [])

            # _LOGGER.debug(
            #     "Processing SSID: Name='%s' (ID: %s, Number: %s), Enabled: %s, Configured Tags: %s",
            #     ssid_name,
            #     ssid_id,
            #     ssid_number,
            #     is_enabled,
            #     ssid_configured_tags,
            # ) # Removed: too verbose, one per SSID

            matching_devices_online_count = 0
            matching_devices_total_count = 0

            for device_info in devices:
                if not isinstance(device_info, dict):
                    _LOGGER.warning(
                        "Skipping non-dictionary device item: %s", device_info
                    )
                    continue

                device_model: str = device_info.get("model", "")
                # Consider only Meraki Wireless Access Points (MR series) for
                # SSID status.
                if device_model.upper().startswith("MR"):
                    device_serial: Optional[str] = device_info.get("serial")
                    device_status_raw = device_info.get("status")
                    device_status: str = "unknown"  # Default status
                    if isinstance(device_status_raw, str):
                        device_status = device_status_raw.lower()
                    # If device_status_raw was None (or not a string), device_status remains "unknown"
                    # Device tags are now expected to be directly within the
                    # device_info dictionary.
                    current_device_tags: List[str] = device_info.get("tags", [])

                    # _LOGGER.debug(
                    #     "  Checking Wireless AP: Serial=%s, Status='%s', Model='%s', AP Tags=%s",
                    #     device_serial,
                    #     device_status,
                    #     device_model,
                    #     current_device_tags,
                    # ) # Removed: too verbose, one per AP per SSID

                    if SsidStatusCalculator._does_device_match_ssid_tags(
                        ssid_configured_tags,  # Tags from SSID config.
                        current_device_tags,  # Tags from the AP device itself.
                    ):
                        matching_devices_total_count += 1
                        if device_status == "online":
                            matching_devices_online_count += 1
                        # _LOGGER.debug(
                        #     "    AP (Serial: %s) matches SSID tag criteria.",
                        #     device_serial,
                        # ) # Removed: too verbose
                    # else: # No need for an explicit log when no match, also too verbose
                        # _LOGGER.debug(
                        #     "    AP (Serial: %s) does not match SSID tag criteria.",
                        #     device_serial,
                        # )
                # else: # Devices not starting with "MR" are ignored for SSID calculation.
                # _LOGGER.debug("    Device (Serial: %s, Model: %s) is not an MR AP; skipping.",
                # device_info.get("serial"), device_model)

            ssid_info["matching_devices_online"] = matching_devices_online_count
            ssid_info["matching_devices_total"] = matching_devices_total_count

            # Determine the final operational status of the SSID based on its enabled state
            # and the counts of matching online/total Access Points.
            if not is_enabled:
                # If the SSID is administratively disabled in Meraki dashboard.
                ssid_info["status"] = "disabled"
            elif matching_devices_total_count == 0:
                # If no APs (MR devices) are found that match this SSID's tag criteria.
                # This implies the SSID is configured but not broadcast by any relevant APs.
                ssid_info["status"] = "no_matching_devices"
            elif matching_devices_online_count == matching_devices_total_count:
                # All APs that should be broadcasting this SSID are currently online.
                ssid_info["status"] = "online"
            elif matching_devices_online_count > 0:
                # Some, but not all, of the APs that should broadcast this SSID are online.
                # At least one AP is online, but others are offline/unresponsive.
                ssid_info["status"] = "partially_online"
            else:  # This implies matching_devices_total_count > 0 but matching_devices_online_count == 0
                # All APs that should be broadcasting this SSID are currently offline or in an unknown state.
                # The SSID is configured on APs, but none of them are reachable/online.
                ssid_info["status"] = "offline"

            _LOGGER.debug(
                "  SSID '%s' (ID: %s) final status: '%s' (Online APs: %d / Total Matching APs: %d)",
                ssid_name,
                ssid_id,
                ssid_info["status"],
                matching_devices_online_count,
                matching_devices_total_count,
            )
            updated_ssids_list.append(ssid_info)

        _LOGGER.debug(
            "SSID status calculation complete. Processed and updated %d SSIDs.",
            len(updated_ssids_list),
        )
        return updated_ssids_list

    @staticmethod
    def _does_device_match_ssid_tags(
        ssid_tags: List[str],  # Tags defined on the SSID configuration.
        device_actual_tags: List[str],  # Tags physically on the device.
    ) -> bool:
        """Determine if a device's tags match an SSID's tags.

        The logic is permissive (relaxed):
        - If an SSID has no `ssid_tags`, any device is considered a match.
        - If an SSID has `ssid_tags`, a device matches if it shares at least one tag with the SSID.
        - If an SSID has `ssid_tags` but the device has no `device_actual_tags`, it's not a match.

        Args:
            ssid_tags: A list of tags associated with the SSID from its configuration.
            device_actual_tags: A list of tags currently on the device.

        Returns:
            True if the device's tags meet the SSID's tag requirements, False otherwise.
        """
        # If an SSID has no tags defined in its configuration, it implies it should be
        # broadcast by all APs (that are capable, e.g. in the same network, though network
        # association is handled elsewhere). So, any device is a match from a
        # tag perspective.
        if not ssid_tags:
            return True

        # If the SSID configuration requires specific tags, but the device itself has no tags,
        # it cannot fulfill the requirement.
        if not device_actual_tags:
            return False

        # Normalize tags to lowercase for case-insensitive comparison. This ensures that
        # "Office" and "office" are treated as the same tag.
        ssid_tags_lower = {tag.lower() for tag in ssid_tags}
        device_tags_lower = {tag.lower() for tag in device_actual_tags}

        # Permissive (Relaxed) mode: Returns True if there's any overlap (intersection)
        # between the SSID's configured tags and the device's actual tags.
        # `isdisjoint()` returns True if the sets have NO common elements.
        return not ssid_tags_lower.isdisjoint(device_tags_lower)
