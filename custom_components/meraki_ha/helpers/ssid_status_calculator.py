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
        points (APs) that are tagged to broadcast it. The rules are:
        - 'disabled': If the SSID itself is administratively disabled.
        - 'no_matching_devices': If no APs are tagged to broadcast this SSID.
        - 'online': If all APs tagged for this SSID are online.
        - 'partially_online': If some, but not all, APs tagged for this SSID are online.
        - 'offline': If all APs tagged for this SSID are offline (or in an unknown state).
        - 'unknown_device_data_missing': If the `devices` list is None, preventing status calculation.

        Args:
            ssids: A list of SSID dictionaries. Each dictionary is expected to contain:
                   - 'id' (any, optional): SSID identifier.
                   - 'number' (any, optional): SSID number.
                   - 'name' (str, optional): SSID name.
                   - 'enabled' (bool): Whether the SSID is enabled.
                   - 'tags' (List[str], optional): A list of string tags.
            devices: A list of Meraki device dictionaries. Each dictionary for an AP
                     (model starting with "MR") is expected to contain:
                     - 'serial' (str, optional): Device serial number.
                     - 'status' (str, optional): Device status (e.g., "online").
                     - 'model' (str): Device model.
                     - 'tags' (List[str], optional): A list of string tags on the device.

        Returns:
            A list of SSID dictionaries, each updated with new keys:
            'matching_devices_online' (count), 'matching_devices_total' (count),
            and 'status' (string). Returns an empty list if the input `ssids`
            is None or empty, or if inputs are not lists.
        """
        if not isinstance(ssids, list):
            _LOGGER.error("Invalid input: 'ssids' is not a list (type: %s). Returning empty list.", type(ssids).__name__)
            return []
        if not ssids:
            _LOGGER.debug("SSID data is empty in calculate_ssid_status; returning empty list.")
            return []

        if not isinstance(devices, list) and devices is not None: # Allow devices to be None, but not other non-list types
            _LOGGER.error("Invalid input: 'devices' is not a list (type: %s) and not None. SSID statuses cannot be determined accurately.", type(devices).__name__)
            # Mark all SSIDs as unknown_device_data_missing, similar to when devices is None
            processed_ssids_on_error = []
            for ssid_info_item in ssids:
                if isinstance(ssid_info_item, dict):
                    ssid_info_item["status"] = "unknown_device_data_missing"
                    processed_ssids_on_error.append(ssid_info_item)
                # else: skip non-dict ssid items if ssids list itself was malformed with non-dicts
            return processed_ssids_on_error

        if devices is None:
            _LOGGER.warning(
                "Device data is None in calculate_ssid_status. SSID statuses cannot be determined accurately. "
                "Marking SSIDs as 'unknown_device_data_missing'."
            )
            # Ensure all items in ssids are dicts before adding status key
            processed_ssids_on_none_devices = []
            for ssid_info_item in ssids:
                if isinstance(ssid_info_item, dict):
                    ssid_info_item["status"] = "unknown_device_data_missing"
                    processed_ssids_on_none_devices.append(ssid_info_item)
                else:
                    _LOGGER.warning("Skipping non-dictionary item in ssids list when devices is None: %s", ssid_info_item)
            return processed_ssids_on_none_devices

        _LOGGER.debug(
            "Calculating SSID status for %d SSIDs using %d devices.",
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
            if not isinstance(is_enabled, bool):
                _LOGGER.warning("SSID '%s' (ID: %s) 'enabled' flag is not a boolean (type: %s, value: %s). Defaulting to False.",
                                ssid_name, ssid_id, type(is_enabled).__name__, is_enabled)
                is_enabled = False

            # Tags defined on the SSID configuration.
            raw_ssid_tags = ssid_info.get("tags", [])
            if not isinstance(raw_ssid_tags, list):
                _LOGGER.warning("SSID '%s' (ID: %s) 'tags' attribute is not a list (type: %s). Treating as empty tags list.",
                                ssid_name, ssid_id, type(raw_ssid_tags).__name__)
                ssid_configured_tags: List[str] = []
            else:
                ssid_configured_tags = [str(tag) for tag in raw_ssid_tags if isinstance(tag, str)]
                if len(ssid_configured_tags) != len(raw_ssid_tags):
                    _LOGGER.warning("SSID '%s' (ID: %s) had non-string items in its 'tags' list. Filtered to: %s",
                                    ssid_name, ssid_id, ssid_configured_tags)

            _LOGGER.debug(
                "Processing SSID: Name='%s' (ID: %s, Number: %s), Enabled: %s, Configured Tags: %s",
                ssid_name,
                ssid_id,
                ssid_number,
                is_enabled,
                ssid_configured_tags,
            )

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
                    raw_device_tags = device_info.get("tags", [])
                    if not isinstance(raw_device_tags, list):
                        _LOGGER.warning("Device AP (Serial: %s) 'tags' attribute is not a list (type: %s). Treating as empty tags list.",
                                        device_serial, type(raw_device_tags).__name__)
                        current_device_tags: List[str] = []
                    else:
                        current_device_tags = [str(tag) for tag in raw_device_tags if isinstance(tag, str)]
                        if len(current_device_tags) != len(raw_device_tags):
                            _LOGGER.warning("Device AP (Serial: %s) had non-string items in its 'tags' list. Filtered to: %s",
                                            device_serial, current_device_tags)

                    _LOGGER.debug(
                        "  Checking Wireless AP: Serial=%s, Status='%s', Model='%s', AP Tags=%s",
                        device_serial,
                        device_status,
                        device_model,
                        current_device_tags,
                    )

                    if SsidStatusCalculator._does_device_match_ssid_tags(
                        ssid_configured_tags,  # Tags from SSID config.
                        current_device_tags,  # Tags from the AP device itself.
                    ):
                        matching_devices_total_count += 1
                        if device_status == "online":
                            matching_devices_online_count += 1
                        _LOGGER.debug(
                            "    AP (Serial: %s) matches SSID tag criteria.",
                            device_serial,
                        )
                    else:
                        _LOGGER.debug(
                            "    AP (Serial: %s) does not match SSID tag criteria.",
                            device_serial,
                        )
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
            else:  # matching_devices_total_count > 0 but matching_devices_online_count == 0
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

        An AP matches if it shares at least one tag with the SSID.
        If the SSID has no tags, any AP is considered a match.

        Args:
            ssid_tags: A list of string tags associated with the SSID from its configuration.
                       Expected type: List[str].
            device_actual_tags: A list of string tags currently on the device.
                                Expected type: List[str].

        Returns:
            True if the device's tags meet the SSID's tag requirements, False otherwise.
            Returns False if input types are invalid.
        """
        if not isinstance(ssid_tags, list):
            _LOGGER.warning("Invalid input: 'ssid_tags' is not a list (type: %s). Cannot perform tag match.", type(ssid_tags).__name__)
            return False
        if not isinstance(device_actual_tags, list):
            _LOGGER.warning("Invalid input: 'device_actual_tags' is not a list (type: %s). Cannot perform tag match.", type(device_actual_tags).__name__)
            return False

        if not ssid_tags: # Handles empty list for ssid_tags
            return True

        if not device_actual_tags: # Handles empty list for device_actual_tags (if ssid_tags is not empty)
            return False

        # Normalize tags to lowercase for case-insensitive comparison.
        try:
            ssid_tags_lower = set()
            for tag in ssid_tags:
                if isinstance(tag, str):
                    ssid_tags_lower.add(tag.lower())
                else:
                    _LOGGER.warning("Non-string tag found in ssid_tags: %s (type: %s). Skipping.", tag, type(tag).__name__)

            device_tags_lower = set()
            for tag in device_actual_tags:
                if isinstance(tag, str):
                    device_tags_lower.add(tag.lower())
                else:
                    _LOGGER.warning("Non-string tag found in device_actual_tags: %s (type: %s). Skipping.", tag, type(tag).__name__)

            if not ssid_tags_lower: # If, after filtering, ssid_tags_lower is empty (e.g. original ssid_tags had only non-strings)
                return True # Behaves like original "if not ssid_tags"

            if not device_tags_lower and ssid_tags_lower : # If device tags became empty after filtering, and ssid tags are not empty
                 return False


        except AttributeError: # Should be largely caught by isinstance checks above
            _LOGGER.exception("AttributeError during tag processing in _does_device_match_ssid_tags. This is unexpected with type checks.")
            return False # Safety net

        # Relaxed mode: Returns True if there's any overlap (intersection)
        # between the SSID's configured tags and the device's actual tags.
        # `isdisjoint()` returns True if the sets have NO common elements.
        return not ssid_tags_lower.isdisjoint(device_tags_lower)
