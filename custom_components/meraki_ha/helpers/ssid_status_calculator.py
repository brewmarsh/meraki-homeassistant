"""
Helper module to calculate the operational status of Meraki SSIDs.

This module provides the `SsidStatusCalculator` class, containing static
methods to determine an SSID's operational status (e.g., online, offline,
partially_online). This status is based on the state and tags of associated
Meraki wireless access points (MR series devices).
"""

import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)


class SsidStatusCalculator:
    """
    Calculates the operational status of Meraki SSIDs.

    This class uses static methods to evaluate SSID status by correlating
    SSID configurations (especially tags) with the current state and tags
    of relevant Meraki wireless access points (APs).
    """

    @classmethod
    def calculate_ssid_status(
        cls,
        ssids: list[dict[str, Any]] | None,
        # Device list; tags are expected within each device dict.
        devices: list[dict[str, Any]] | None,
        # The `device_tags` parameter (previously a separate dict) has been
        # removed.
    ) -> list[dict[str, Any]]:
        """
        Calculate the operational status of each SSID provided.

        The status of an SSID is determined by the state of the wireless access
        points (APs) that are tagged to broadcast it. The logic is permissive:
        if an SSID has tags, an AP needs to match only one of those tags.
        If an SSID has no tags, any AP is considered a match.

        The rules are:
        - 'disabled': If the SSID itself is administratively disabled.
        - 'no_matching_devices': If no APs are tagged to broadcast this SSID.
        - 'online': If all APs matching this SSID (by tag) are online.
        - 'partially_online': If some, but not all, matching APs are online.
        - 'offline': If all APs matching this SSID are offline.
        - 'unknown_device_data_missing': If `devices` is None.

        Args:
        ----
            ssids: A list of SSID dictionaries.
            devices: A list of Meraki device dictionaries.

        Returns
        -------
            A list of SSID dictionaries, each updated with new keys:
            'matching_devices_online' (count), 'matching_devices_total' (count),
            and 'status' (string). Returns an empty list if `ssids` is None.

        """
        if not ssids:  # Handles None or empty list for ssids.
            return []

        if devices is None:
            _LOGGER.warning("Device data is None; SSID statuses cannot be determined.")
            for ssid in ssids:
                if isinstance(ssid, dict):
                    ssid["status"] = "unknown_device_data_missing"
            return ssids

        updated_ssids_list: list[dict[str, Any]] = []
        for ssid_info in ssids:
            if not isinstance(ssid_info, dict):
                _LOGGER.warning("Skipping non-dictionary SSID item: %s", ssid_info)
                continue

            cls._process_single_ssid(ssid_info, devices)
            updated_ssids_list.append(ssid_info)

        return updated_ssids_list

    @classmethod
    def _process_single_ssid(
        cls, ssid_info: dict[str, Any], devices: list[dict[str, Any]]
    ) -> None:
        """Process status calculation for a single SSID."""
        ssid_configured_tags: list[str] = ssid_info.get("tags", [])

        online_count, total_count = cls._count_matching_devices(
            ssid_configured_tags, devices
        )

        ssid_info["matching_devices_online"] = online_count
        ssid_info["matching_devices_total"] = total_count
        ssid_info["status"] = cls._determine_ssid_status(
            ssid_info, online_count, total_count
        )

    @classmethod
    def _count_matching_devices(
        cls, ssid_tags: list[str], devices: list[dict[str, Any]]
    ) -> tuple[int, int]:
        """Count total and online devices matching the SSID tags."""
        online_count = 0
        total_count = 0

        for device_info in devices:
            if not isinstance(device_info, dict):
                _LOGGER.warning("Skipping non-dictionary device item: %s", device_info)
                continue

            if not cls._is_valid_ap(device_info):
                continue

            # Check if device matches SSID tags
            device_tags: list[str] = device_info.get("tags", [])
            if cls._does_device_match_ssid_tags(ssid_tags, device_tags):
                total_count += 1
                if cls._is_device_online(device_info):
                    online_count += 1

        return online_count, total_count

    @staticmethod
    def _is_valid_ap(device_info: dict[str, Any]) -> bool:
        """Check if the device is a valid wireless access point."""
        device_model: str | None = device_info.get("model")
        return bool(device_model and device_model.upper().startswith("MR"))

    @staticmethod
    def _is_device_online(device_info: dict[str, Any]) -> bool:
        """Check if the device status is online."""
        device_status_raw = device_info.get("status")
        if isinstance(device_status_raw, str):
            return device_status_raw.lower() == "online"
        return False

    @staticmethod
    def _determine_ssid_status(
        ssid_info: dict[str, Any], online_count: int, total_count: int
    ) -> str:
        """Determine the final status string for the SSID."""
        if not ssid_info.get("enabled", False):
            return "disabled"

        if not ssid_info.get("networkId"):
            _LOGGER.warning(
                "SSID '%s' is missing networkId; setting status to 'unknown'.",
                ssid_info.get("name", "Unknown SSID"),
            )
            return "unknown"

        if total_count == 0:
            return "no_matching_devices"

        if online_count == total_count:
            return "online"

        if online_count > 0:
            return "partially_online"

        return "offline"

    @staticmethod
    def _does_device_match_ssid_tags(
        ssid_tags: list[str],  # Tags defined on the SSID configuration.
        device_actual_tags: list[str],  # Tags physically on the device.
    ) -> bool:
        """
        Determine if a device's tags match an SSID's tags.

        The logic is permissive (relaxed):
        - If an SSID has no `ssid_tags`, any device is a match.
        - If an SSID has `ssid_tags`, a device matches if it shares at least
          one tag with the SSID.
        - If an SSID has `ssid_tags` but the device has no
          `device_actual_tags`, it's not a match.

        Args:
        ----
            ssid_tags: A list of tags from the SSID's configuration.
            device_actual_tags: A list of tags on the device.

        Returns
        -------
            True if the device's tags meet the SSID's tag requirements.

        """
        # If an SSID has no tags, it should be broadcast by all APs.
        # Any device is a match from a tag perspective.
        if not ssid_tags:
            return True

        # If the SSID requires tags, but the device has none,
        # it cannot fulfill the requirement.
        if not device_actual_tags:
            return False

        # Normalize tags to lowercase for case-insensitive comparison.
        ssid_tags_lower = {tag.lower() for tag in ssid_tags}
        device_tags_lower = {tag.lower() for tag in device_actual_tags}

        # Permissive (Relaxed) mode: Returns True if there's any overlap.
        return not ssid_tags_lower.isdisjoint(device_tags_lower)
