"""Helper to calculate the status of Meraki SSIDs based on device tags."""

import logging

_LOGGER = logging.getLogger(__name__)


class SsidStatusCalculator:
    """Calculates the operational status of Meraki SSIDs."""

    @staticmethod
    def calculate_ssid_status(ssids, devices, device_tags, relaxed_tag_match):
        """
        Calculates the status of each SSID based on the operational status
        and tag matching of associated wireless access point devices.
        """
        _LOGGER.debug(
            f"calculate_ssid_status called with: ssids={ssids}, devices={devices}, device_tags={device_tags}, relaxed_tag_match={relaxed_tag_match}"
        )
        if ssids is None:
            _LOGGER.error("SSID data is None in calculate_ssid_status")
            return []
        if devices is None:
            _LOGGER.error("Device data is None in calculate_ssid_status")
            return ssids  # Or an empty list, depending on desired behavior
        if device_tags is None:
            _LOGGER.warning("Device tags data is None in calculate_ssid_status")
            device_tags = {}  # Initialize to an empty dictionary to avoid errors

        updated_ssids = []
        for ssid in ssids:
            ssid_id = ssid.get("id")
            ssid_name = ssid.get("name")
            enabled = ssid.get("enabled")
            tags = ssid.get("tags", [])
            _LOGGER.debug(
                f"Processing SSID: ID={ssid_id}, Name='{ssid_name}', Enabled={enabled}, Tags={tags}"
            )

            matching_devices_online = 0
            matching_devices_total = 0

            for device in devices:
                device_serial = device.get("serial")
                device_status = device.get("status")
                device_model = device.get("model", "")
                device_tags_list = device_tags.get(device_serial, [])
                _LOGGER.debug(
                    f"  Checking device: Serial={device_serial}, Status='{device_status}', Model='{device_model}', Tags={device_tags_list}"
                )

                # Only consider Meraki Wireless Access Points (model starts with "MR")
                if device_model.startswith("MR"):
                    if SsidStatusCalculator._does_device_match_ssid(
                        tags, device_tags_list, relaxed_tag_match
                    ):
                        matching_devices_total += 1
                        if device_status == "online":
                            matching_devices_online += 1
                        _LOGGER.debug("    Wireless AP matches SSID criteria.")
                    else:
                        _LOGGER.debug("    Wireless AP does not match SSID criteria.")
                else:
                    _LOGGER.debug(
                        f"    Device is not a Wireless AP (model: {device_model}), skipping for SSID status."
                    )

            ssid["matching_devices_online"] = matching_devices_online
            ssid["matching_devices_total"] = matching_devices_total

            if enabled:
                if (
                    matching_devices_total > 0
                    and matching_devices_online == matching_devices_total
                ):
                    ssid["status"] = "online"
                elif matching_devices_total > 0 and matching_devices_online > 0:
                    ssid["status"] = "partially_online"
                elif matching_devices_total > 0:
                    ssid["status"] = "offline"
                else:
                    ssid["status"] = "no_matching_devices"
            else:
                ssid["status"] = "disabled"

            updated_ssids.append(ssid)

        _LOGGER.debug(f"calculate_ssid_status returning: {updated_ssids}")
        return updated_ssids

    @staticmethod
    def _does_device_match_ssid(ssid_tags, device_tags, relaxed_tag_match):
        """Checks if a device's tags match an SSID's tags."""
        if not ssid_tags:
            return True
        if not device_tags:
            return False if not relaxed_tag_match else True

        if relaxed_tag_match:
            return any(tag in device_tags for tag in ssid_tags)
        else:
            return all(tag in device_tags for tag in ssid_tags)
