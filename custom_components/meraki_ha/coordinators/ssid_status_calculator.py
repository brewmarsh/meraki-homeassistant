"""SSID Status Calculator for the meraki_ha integration."""

from typing import Any, Dict, List


class SsidStatusCalculator:
    """Class to calculate the enabled status of SSIDs based on device tags."""

    @staticmethod
    def calculate_ssid_status(
        ssids: List[Dict[str, Any]],
        devices: List[Dict[str, Any]],
        device_tags: Dict[str, List[str]],
        relaxed_tag_match: bool,
    ) -> List[Dict[str, Any]]:
        """Calculate the enabled status of SSIDs."""

        for ssid in ssids:
            ssid_name = ssid["name"]
            ssid["enabled"] = False  # Default to disabled

            for device in devices:
                device_tags_list = device_tags.get(device["serial"], [])
                if relaxed_tag_match:
                    if any(ssid_name in tag for tag in device_tags_list):
                        ssid["enabled"] = True
                        break  # SSID enabled if found on any device
                else:
                    if f"ssid_{ssid_name}_enabled" in device_tags_list:
                        ssid["enabled"] = True
                        break  # SSID enabled if found on any device

        return ssids
