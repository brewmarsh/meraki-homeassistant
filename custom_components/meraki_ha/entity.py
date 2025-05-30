"""Base entity class for Meraki Home Assistant integration.

This module defines `MerakiEntity`, a base class for all Meraki
entities in Home Assistant. It provides common properties and methods,
such as device information linking and coordinator management,
building upon Home Assistant's `CoordinatorEntity`.
"""
import logging
from typing import Any, Dict, Optional  # Added Optional, Any (List removed)

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
# used
from .coordinators import MerakiDataUpdateCoordinator
from .const import DOMAIN
from .coordinators.meraki_device_types import map_meraki_model_to_device_type

_LOGGER = logging.getLogger(__name__)


class MerakiEntity(CoordinatorEntity[MerakiDataUpdateCoordinator]):
    """Base class for Meraki entities in Home Assistant.

    This class provides common functionality for entities associated with
    Meraki devices or services, such as linking to the correct device in the
    Home Assistant device registry and handling coordinator data.

    Attributes:
        _device_info_data: Raw dictionary data for the associated Meraki
                           device.
        _ssid_info_data: (Optional) Raw dictionary data for an
                         associated SSID.
    """

    # Define _attr_has_entity_name = True if your entity should inherit
    # the device name by default and then you can omit self._attr_name
    # in specific entities if they use the device name.
    # _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        # Meraki device this entity might be directly related to
        device_data: Dict[str, Any],
        # Optional SSID data if entity is SSID-specific
        ssid_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the Meraki base entity.

        Args:
            coordinator: The data update coordinator for this entity.
            device_data: A dictionary containing information about the
                         primary Meraki device this entity is related to
                         (e.g., an AP, switch). Expected to have 'serial',
                         'name', 'model', 'firmware'.
            ssid_data: (Optional) A dictionary containing information
                       about a specific SSID if this entity is related to
                       an SSID. Expected to have 'name' and 'number' if
                       provided.
        """
        super().__init__(coordinator)
        self._device_info_data: Dict[str, Any] = device_data
        self._ssid_info_data: Optional[Dict[str, Any]] = ssid_data

        # Common attributes derived from device_data
        self._device_serial: Optional[str] = self._device_info_data.get("serial")
        self._device_name: Optional[str] = self._device_info_data.get("name")
        # Fallback to serial if name is missing for display name consistency
        if not self._device_name and self._device_serial:
            self._device_name = self._device_serial

        self._device_model: Optional[str] = self._device_info_data.get("model")
        self._device_firmware: Optional[str] = (
            self._device_info_data.get("firmware")
        )

        # Common attributes derived from ssid_data (if provided)
        self._ssid_name: Optional[str] = None
        # SSID number is typically an int
        self._ssid_number: Optional[int] = None
        if self._ssid_info_data:
            self._ssid_name = self._ssid_info_data.get("name")
            self._ssid_number = self._ssid_info_data.get("number")
        
        # The _device_index and _ssid_index attributes from the original code
        # are problematic:
        # 1. They assume `coordinator.data` has a specific structure
        #    ("devices" list, then "ssids" sublist).
        # 2. Storing indices is fragile; if the list order changes, the
        #    index is wrong.
        # It's better to look up the device/SSID data by a stable ID (like
        # serial or SSID number) directly from `self.coordinator.data` when
        # needed, or for `CoordinatorEntity` to handle providing the
        # relevant part of the data to the entity.
        # For now, removing these index attributes as they are not robust.
        # If specific data is needed from the coordinator, it should be
        # accessed via self.coordinator.data using appropriate keys/filters
        # inside properties or update methods.

    # The _find_device_index and _find_ssid_index methods are removed as
    # they are no longer used due to the removal of _device_index and
    # _ssid_index. Data should be accessed from self.coordinator.data
    # using stable identifiers.

    @property
    def device_info(self) -> Optional[DeviceInfo]:
        """Return device information for linking this entity to the registry.

        This information is used by Home Assistant to correctly group
        entities and display device details in the UI. If the entity is
        specifically for an SSID, it links to the SSID "device".
        Otherwise, it links to the physical Meraki device.
        """
        # Should always have a serial for a device-based entity
        if not self._device_serial:
            _LOGGER.warning(
                "Meraki entity created without a device serial: %s",
                self.entity_id if self.hass else "Unknown ID",
            )
            return None

        # If this entity is related to a specific SSID, it should be
        # parented by the SSID "device" which in turn is parented by the
        # physical device (AP).
        # The SSID "device" identifier might be "{network_id}_{ssid_number}".
        # The physical device (AP) identifier is (DOMAIN, self._device_serial).
        
        # If this entity represents an SSID itself or a property of an SSID:
        if self._ssid_info_data and self._ssid_number is not None:
            network_id = self._device_info_data.get("networkId")  # AP's networkId
            if network_id:
                # This entity is part of an SSID "device"
                return DeviceInfo(
                    identifiers={(DOMAIN, f"{network_id}_{self._ssid_number}")},
                    # Name might be already set by the SSID "device" registration
                    # Or, if this entity is the SSID "device" itself:
                    # name=str(self._ssid_name or f"SSID {self._ssid_number}"),
                    # model="SSID",
                    # Links SSID device to physical AP
                    # via_device=(DOMAIN, self._device_serial),
                )
            else:
                _LOGGER.warning(
                    "SSID entity for %s is missing networkId from its parent AP data.",
                    self._ssid_name or self._ssid_number,
                )
                # Fall through to physical device if SSID linking fails, and use formatted_device_name for the AP.

        # Get the raw device name (name from API or serial)
        # self._device_name is already pre-calculated in __init__ to be name or serial
        device_name_raw = self._device_name or "Unknown Meraki Device" 

        # Get device_name_format from the coordinator
        device_name_format_option = self.coordinator.device_name_format

        device_type_mapped = map_meraki_model_to_device_type(self._device_model or "")

        _LOGGER.debug(
            "MERAKI_DEBUG_ENTITY: Device Info for %s: Raw Name='%s', Model='%s', FormatOption='%s', MappedType='%s'",
            self._device_serial,
            device_name_raw,
            self._device_model,
            device_name_format_option,
            device_type_mapped,
        )

        formatted_device_name = device_name_raw
        if device_name_format_option == "prefix" and device_type_mapped != "Unknown":
            formatted_device_name = f"[{device_type_mapped}] {device_name_raw}"
        elif device_name_format_option == "suffix" and device_type_mapped != "Unknown":
            formatted_device_name = f"{device_name_raw} [{device_type_mapped}]"
        
        _LOGGER.debug(
            "MERAKI_DEBUG_ENTITY: Device Info for %s: Final Formatted Name='%s'",
            self._device_serial,
            formatted_device_name,
        )

        # Default: This entity is directly related to the physical Meraki device
        device_info_to_return = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=str(formatted_device_name),
            manufacturer="Cisco Meraki",
            model=str(self._device_model or "Unknown"),
            sw_version=str(self._device_firmware or ""),
        )
        _LOGGER.debug(
            "MERAKI_DEBUG_ENTITY: Device Info for %s: Returning DeviceInfo object: %s",
            self._device_serial,
            str(device_info_to_return), 
        )
        return device_info_to_return

    # Example of how an entity might access its specific data from the
    # coordinator:
    # @property
    # def available(self) -> bool:
    #     """Return True if entity is available."""
    #     if not self.coordinator.last_update_success:
    #         return False
    #     # Find this device's specific data in coordinator.data
    #     # This logic depends heavily on the structure of coordinator.data
    #     # For example:
    #     if self.coordinator.data and "devices" in self.coordinator.data:
    #         for dev_data in self.coordinator.data["devices"]:
    #             if dev_data.get("serial") == self._device_serial:
    #                 # Check device status, e.g.,
    #                 # dev_data.get("status") == "online"
    #                 return dev_data.get("status") == "online"  # Example
    #     return False  # Default to not available if data missing
