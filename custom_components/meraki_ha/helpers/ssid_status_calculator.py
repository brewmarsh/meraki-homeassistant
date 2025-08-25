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
            return []

        if devices is None:
            _LOGGER.warning(
                "Device data is None in calculate_ssid_status. SSID statuses cannot be determined accurately. "
                "Marking SSIDs as 'unknown_device_data_missing'."
            )
            for ssid in ssids:
                ssid["status"] = "unknown_device_data_missing"
            return ssids

        updated_ssids_list: List[Dict[str, Any]] = []
        for ssid_info in ssids:
            if not isinstance(ssid_info, dict):
                _LOGGER.warning("Skipping non-dictionary SSID item: %s", ssid_info)
                continue

            is_enabled = ssid_info.get("enabled", False)
            ssid_configured_tags: List[str] = ssid_info.get("tags", [])
            network_id = ssid_info.get("networkId")

            matching_devices_online_count = 0
            matching_devices_total_count = 0

            for device_info in devices:
                if not isinstance(device_info, dict):
                    _LOGGER.warning(
                        "Skipping non-dictionary device item: %s", device_info
                    )
                    continue

                device_model: Optional[str] = device_info.get("model")
                if device_model and device_model.upper().startswith("MR"):
                    device_status_raw = device_info.get("status")
                    device_status: str = "unknown"
                    if isinstance(device_status_raw, str):
                        device_status = device_status_raw.lower()
                    current_device_tags: List[str] = device_info.get("tags", [])

                    if SsidStatusCalculator._does_device_match_ssid_tags(
                        ssid_configured_tags,
                        current_device_tags,
                    ):
                        matching_devices_total_count += 1
                        if device_status == "online":
                            matching_devices_online_count += 1

            ssid_info["matching_devices_online"] = matching_devices_online_count
            ssid_info["matching_devices_total"] = matching_devices_total_count

            if not is_enabled:
                ssid_info["status"] = "disabled"
            elif not network_id:
                _LOGGER.warning(
                    f"SSID '{ssid_info.get('name', 'Unknown SSID')}' is missing networkId, cannot determine status accurately. Setting to 'unknown'."
                )
                ssid_info["status"] = "unknown"
            elif matching_devices_total_count == 0:
                ssid_info["status"] = "no_matching_devices"
            elif matching_devices_online_count == matching_devices_total_count:
                ssid_info["status"] = "online"
            elif matching_devices_online_count > 0:
                ssid_info["status"] = "partially_online"
            else:
                ssid_info["status"] = "offline"

            # Per-SSID status log removed
            updated_ssids_list.append(ssid_info)

        # Overall completion log removed
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
