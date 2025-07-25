"""Data processor for the Meraki Home Assistant integration.

This module provides functions for processing data fetched from the Meraki API.
"""

import logging
from typing import Any, Dict, List, Optional

_LOGGER = logging.getLogger(__name__)


def process_firmware_upgrades(
    devices: List[Dict[str, Any]],
    firmware_upgrade_data_raw: Optional[List[Dict[str, Any]]],
    org_id: str,
) -> None:
    """Process firmware upgrade data and merge it into the device list."""
    firmware_info_map = {}
    if not isinstance(firmware_upgrade_data_raw, list):
        _LOGGER.warning(
            f"firmware_upgrade_data_raw is not a list (type: {type(firmware_upgrade_data_raw).__name__}), "
            f"cannot process firmware status for devices. Value: {str(firmware_upgrade_data_raw)[:200]}"
        )
    elif not firmware_upgrade_data_raw:
        _LOGGER.debug(
            f"firmware_upgrade_data_raw is an empty list. "
            f"No specific upgrade information available for org {org_id}."
        )
    else:
        for upgrade_item in firmware_upgrade_data_raw:
            if not isinstance(upgrade_item, dict):
                _LOGGER.warning(
                    f"Skipping non-dictionary item in firmware_upgrade_data_raw list: {str(upgrade_item)[:200]}"
                )
                continue
            item_serial = upgrade_item.get("serial")
            if not item_serial:
                continue
            is_item_up_to_date = False
            latest_item_version = "N/A"
            next_upgrade_info = upgrade_item.get("nextUpgrade")
            if isinstance(next_upgrade_info, dict):
                to_version_info = next_upgrade_info.get("toVersion")
                if isinstance(to_version_info, dict):
                    latest_item_version_val = to_version_info.get("version", "N/A")
                    if latest_item_version_val:
                        latest_item_version = latest_item_version_val
                    is_item_up_to_date = False
                else:
                    if to_version_info is not None:
                        _LOGGER.warning(
                            "Firmware upgrade item for serial %s has 'toVersion' but it's not a dictionary: %s. Cannot determine scheduled version.",
                            item_serial,
                            str(to_version_info)[:100],
                        )
                    item_status = str(upgrade_item.get("status", "")).lower()
                    if item_status == "up-to-date":
                        is_item_up_to_date = True
                    elif item_status == "has-newer-stable-version":
                        is_item_up_to_date = False
                        available_versions = upgrade_item.get("availableVersions")
                        if isinstance(available_versions, list) and available_versions:
                            if isinstance(available_versions[0], dict):
                                latest_item_version_val = available_versions[0].get(
                                    "version", "N/A"
                                )
                                if latest_item_version_val:
                                    latest_item_version = latest_item_version_val
                            else:
                                _LOGGER.warning(
                                    "First item in 'availableVersions' for serial %s is not a dict: %s. Cannot determine latest available version.",
                                    item_serial,
                                    str(available_versions[0])[:100],
                                )
                        elif available_versions is not None:
                            _LOGGER.warning(
                                "'availableVersions' for serial %s is not a non-empty list: %s. Cannot determine latest available version.",
                                item_serial,
                                str(available_versions)[:100],
                            )
            elif next_upgrade_info is not None:
                _LOGGER.warning(
                    "Firmware upgrade item for serial %s has 'nextUpgrade' but it's not a dictionary: %s.",
                    item_serial,
                    str(next_upgrade_info)[:100],
                )
                item_status = str(upgrade_item.get("status", "")).lower()
                if item_status == "up-to-date":
                    is_item_up_to_date = True
                elif item_status == "has-newer-stable-version":
                    is_item_up_to_date = False
                    available_versions = upgrade_item.get("availableVersions")
                    if isinstance(available_versions, list) and available_versions:
                        if isinstance(available_versions[0], dict):
                            latest_item_version = available_versions[0].get("version", "N/A")
                        else:
                            _LOGGER.warning(
                                "First item in 'availableVersions' (no nextUpgrade path) for serial %s is not a dict: %s.",
                                item_serial,
                                str(available_versions[0])[:100],
                            )
                    elif available_versions is not None:
                        _LOGGER.warning(
                            "'availableVersions' (no nextUpgrade path) for serial %s is not a non-empty list: %s.",
                            item_serial,
                            str(available_versions)[:100],
                        )
            else:
                item_status = str(upgrade_item.get("status", "")).lower()
                if item_status == "up-to-date":
                    is_item_up_to_date = True
                elif upgrade_item.get("latestVersion"):
                    latest_item_version_val = upgrade_item.get("latestVersion")
                    if latest_item_version_val:
                        latest_item_version = latest_item_version_val
                elif item_status == "has-newer-stable-version":
                    is_item_up_to_date = False
                    available_versions = upgrade_item.get("availableVersions")
                    if isinstance(available_versions, list) and available_versions:
                        latest_item_version = available_versions[0].get("version", "N/A")
            firmware_info_map[item_serial] = {
                "api_reported_up_to_date": is_item_up_to_date,
                "api_latest_version": latest_item_version,
                "api_status": upgrade_item.get("status", "").lower(),
            }
    for device in devices:
        device_serial = device.get("serial")
        current_device_firmware = device.get("firmware")
        is_up_to_date_bool = False
        latest_known_version = current_device_firmware if current_device_firmware else "N/A"
        if not isinstance(firmware_upgrade_data_raw, list):
            is_up_to_date_bool = False
        elif not firmware_upgrade_data_raw:
            is_up_to_date_bool = True
        elif device_serial and device_serial in firmware_info_map:
            info = firmware_info_map[device_serial]
            api_latest_version = info["api_latest_version"]
            api_reported_up_to_date = info["api_reported_up_to_date"]
            api_status = info["api_status"]
            if api_status == "up-to-date":
                is_up_to_date_bool = True
                latest_known_version = current_device_firmware if current_device_firmware else "N/A"
            elif api_latest_version and api_latest_version != "N/A":
                latest_known_version = api_latest_version
                if current_device_firmware and current_device_firmware == latest_known_version:
                    is_up_to_date_bool = True
                else:
                    is_up_to_date_bool = False
            elif api_reported_up_to_date:
                is_up_to_date_bool = True
                latest_known_version = current_device_firmware if current_device_firmware else "N/A"
            else:
                is_up_to_date_bool = False
                if api_latest_version and api_latest_version != "N/A":
                    latest_known_version = api_latest_version
            if current_device_firmware and current_device_firmware == latest_known_version:
                is_up_to_date_bool = True
        else:
            if current_device_firmware:
                is_up_to_date_bool = True
                latest_known_version = current_device_firmware
            else:
                is_up_to_date_bool = False
                latest_known_version = "N/A"
        device["firmware_up_to_date"] = is_up_to_date_bool
        device["latest_firmware_version"] = latest_known_version
