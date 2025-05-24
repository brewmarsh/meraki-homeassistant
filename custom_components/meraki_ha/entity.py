"""Provides a base entity class for the Meraki Home Assistant integration.

This module defines `MerakiEntity`, a base class derived from Home Assistant's
`CoordinatorEntity`. It's designed to provide common attributes and functionality
for other Meraki-specific entities (sensors, switches, etc.), such as linking
to the Meraki device in the Home Assistant device registry and simplifying access
to device and SSID information.
"""

import logging
from typing import Any, Dict, List, Optional # Added List, Optional

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Assuming MerakiDataUpdateCoordinator is the correct type.
from .coordinator import MerakiDataUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiEntity(CoordinatorEntity[MerakiDataUpdateCoordinator]):
    """Base class for all Meraki entities in Home Assistant.

    This class provides common properties and methods for entities associated
    with Meraki devices and, optionally, specific SSIDs on those devices.
    It handles the linkage to the Home Assistant device registry and stores
    essential identifying information.

    Attributes:
        coordinator (MerakiDataUpdateCoordinator): The data update coordinator for this entity.
        _device_info_dict (Dict[str, Any]): Raw information about the parent Meraki device.
        _ssid_info_dict (Optional[Dict[str, Any]]): Raw information about the specific SSID,
            if this entity is SSID-specific.
        _device_name (Optional[str]): Name of the Meraki device.
        _device_serial (Optional[str]): Serial number of the Meraki device.
        _device_model (Optional[str]): Model of the Meraki device.
        _device_firmware (Optional[str]): Firmware version of the Meraki device.
        _network_id (Optional[str]): Network ID the device belongs to.
        _ssid_name (Optional[str]): Name of the SSID (if applicable).
        _ssid_number (Optional[int]): Number of the SSID (if applicable).

        Note: The `_device_index` and `_ssid_index` attributes from the original
        code are removed as directly storing indices can be fragile if the
        coordinator's data list changes order. It's generally safer to look up
        device/SSID data by their unique identifiers (serial, SSID number) when needed.
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info_dict: Dict[str, Any],
        ssid_info_dict: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initializes the MerakiEntity.

        Args:
            coordinator (MerakiDataUpdateCoordinator): The data update coordinator.
            device_info_dict (Dict[str, Any]): A dictionary containing information
                about the parent Meraki device (e.g., from API). Expected keys
                include "name", "serial", "model", "firmware", "networkId".
            ssid_info_dict (Optional[Dict[str, Any]]): An optional dictionary
                containing information about a specific SSID if this entity
                pertains to one. Expected keys include "name", "number".
        """
        super().__init__(coordinator)
        self._device_info_dict = device_info_dict
        self._ssid_info_dict = ssid_info_dict

        # Extract common device properties.
        self._device_name = device_info_dict.get("name")
        self._device_serial = device_info_dict.get("serial")
        self._device_model = device_info_dict.get("model")
        self._device_firmware = device_info_dict.get("firmware")
        self._network_id = device_info_dict.get("networkId") # Useful for context

        # Extract SSID-specific properties if an SSID is associated.
        if ssid_info_dict:
            self._ssid_name = ssid_info_dict.get("name")
            self._ssid_number = ssid_info_dict.get("number")
            # Ensure SSID number is an int if present, for consistent lookups.
            if self._ssid_number is not None:
                try:
                    self._ssid_number = int(self._ssid_number)
                except ValueError:
                    _LOGGER.warning(
                        "SSID number '%s' for SSID '%s' on device %s is not a valid integer. Treating as None.",
                        ssid_info_dict.get("number"), self._ssid_name, self._device_serial
                    )
                    self._ssid_number = None
        else:
            self._ssid_name = None
            self._ssid_number = None

        _LOGGER.debug(
            "MerakiEntity initialized: Device Serial: %s, SSID Number: %s",
            self._device_serial,
            self._ssid_number if self._ssid_number is not None else "N/A",
        )

    # Removed _find_device_index and _find_ssid_index.
    # It's generally safer to look up data by identifiers (serial, SSID number)
    # directly from the coordinator's data in methods that need fresh data,
    # rather than relying on indices that might become stale.
    # Example helper to get current device data (can be used by subclasses):
    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Safely retrieves the latest data for this entity's device from the coordinator.

        Returns:
            Optional[Dict[str, Any]]: The device data dictionary if found, else None.
        """
        if self.coordinator.data and "devices" in self.coordinator.data:
            devices_list = self.coordinator.data["devices"]
            if isinstance(devices_list, list):
                for device_data in devices_list:
                    if isinstance(device_data, dict) and device_data.get("serial") == self._device_serial:
                        return device_data
        _LOGGER.debug("Device data for serial %s not found in coordinator data.", self._device_serial)
        return None

    # Example helper to get current SSID data (can be used by subclasses if SSID-specific):
    def _get_current_ssid_data(self) -> Optional[Dict[str, Any]]:
        """Safely retrieves the latest data for this entity's SSID from the coordinator.
        This assumes SSIDs are nested under their parent device in coordinator data.
        Adjust if SSIDs are stored differently (e.g., a flat list under `coordinator.data['ssids']`).

        Returns:
            Optional[Dict[str, Any]]: The SSID data dictionary if found, else None.
        """
        if not self._ssid_number is None: # Only proceed if this entity is SSID-specific
            parent_device_data = self._get_current_device_data()
            if parent_device_data:
                ssids_on_device = parent_device_data.get("ssids", []) # Assuming 'ssids' key holds list of SSIDs for a device
                if isinstance(ssids_on_device, list):
                    for ssid_data in ssids_on_device:
                        if isinstance(ssid_data, dict) and ssid_data.get("number") == self._ssid_number:
                            return ssid_data
        _LOGGER.debug(
            "SSID data for SSID number %s on device %s not found.",
            self._ssid_number, self._device_serial
        )
        return None


    @property
    def device_info(self) -> Optional[DeviceInfo]:
        """Return device information to link this entity to a Home Assistant device.

        This information is used by Home Assistant to group entities under a
        single device panel in the UI and device registry.
        """
        if not self._device_serial: # Cannot register without a unique serial
            return None

        return DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=self._device_name or self._device_serial, # Fallback to serial if name is None
            manufacturer="Cisco Meraki",
            model=self._device_model or "Unknown Model", # Fallback for model
            sw_version=self._device_firmware,
            # `via_device` can be used if this entity represents something connected to
            # another HA device (e.g., an SSID entity linked to its parent AP device).
            # If this MerakiEntity itself represents the main device, `via_device` is not needed here.
            # If this entity is for an SSID, and the AP (self._device_serial) is also a device,
            # this setup is correct. If an SSID entity should be "via" its network device,
            # that would require network_id to be a HA device identifier.
        )
