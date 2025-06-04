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
                         For entities that are directly related to an SSID (e.g., an SSID
                         availability sensor), this `device_data` parameter might actually be
                         the SSID's own information dictionary (the same as `ssid_data`).
                         This is because the SSID itself is treated as the "device"
                         for that specific entity.
            ssid_data: (Optional) A dictionary containing information
                       about a specific SSID if this entity is related to
                       an SSID. Expected to have 'name' and 'number' if
                       provided. If this entity is for the SSID itself, this dictionary
                       will contain all relevant info for that SSID, including 'networkId'
                       and 'number' which are crucial for forming its unique identifier.
        """
        super().__init__(coordinator)
        # Stores the primary device information. For a physical device entity (like an AP sensor),
        # this is the AP's data. For an SSID-specific entity (like SSID availability),
        # this will typically be the SSID's own data dictionary, as the SSID is the "device"
        # this entity pertains to.
        self._device_info_data: Dict[str, Any] = device_data

        # Stores SSID-specific information if the entity is related to an SSID.
        # If the entity is for an SSID itself (e.g. SSID availability sensor),
        # this will be the same as _device_info_data.
        self._ssid_info_data: Optional[Dict[str, Any]] = ssid_data

        # Common attributes derived from device_data.
        # For an SSID-specific entity where device_data is the SSID's own data,
        # _device_serial, _device_name, _device_model might be None or less relevant
        # if these fields ('serial', 'model') are not standard for an SSID's data structure.
        # The actual linking to the HA device registry for SSID entities relies on
        # networkId and ssid_number from _ssid_info_data (or _device_info_data if they are same).
        self._device_serial: Optional[str] = self._device_info_data.get("serial")
        self._device_name: Optional[str] = self._device_info_data.get("name")
        # Fallback to serial if name is missing for display name consistency
        if not self._device_name and self._device_serial:
            self._device_name = self._device_serial

        self._device_model: Optional[str] = self._device_info_data.get("model")
        self._device_firmware: Optional[str] = self._device_info_data.get("firmware")

        # Common attributes derived from ssid_data (if provided)
        self._ssid_name: Optional[str] = None
        # SSID number is typically an int
        self._ssid_number: Optional[int] = None
        if self._ssid_info_data:
            self._ssid_name = self._ssid_info_data.get("name")
            self._ssid_number = self._ssid_info_data.get("number")

        _LOGGER.error(
            "MERAKI_ENTITY_INIT: Initializing for device S/N: %s, Name: %s",
            self._device_serial,
            self._device_name,
        )
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
        # Scenario 1: Entity is related to a specific SSID.
        # This means the entity represents a sensor or switch for an SSID itself.
        # In this case, _ssid_info_data will be populated (it's the SSID's own data dict),
        # and _ssid_number will be derived from it.
        # The `device_info` should then point to the "SSID Device" in Home Assistant.
        # This "SSID Device" is expected to be registered by SSIDDeviceCoordinator
        # with an identifier like (DOMAIN, f"{network_id}_{ssid_number}").
        # This "SSID Device" is, in turn, linked via `via_device` to its "Network Device".
        # Resulting hierarchy: Sensor Entity -> SSID Device -> Network Device -> Config Entry.
        if self._ssid_info_data and self._ssid_number is not None:
            # For SSID entities, _device_info_data and _ssid_info_data might be the same dict.
            # We need 'networkId' from this dict to form the identifier for the SSID device.
            network_id = self._device_info_data.get("networkId")

            if network_id:
                # Identifier for the SSID "device" in Home Assistant.
                ssid_device_identifier = (DOMAIN, f"{network_id}_{self._ssid_number}")
                # This entity (e.g., SSID Availability Sensor) will be associated with this SSID device.
                return DeviceInfo(
                    identifiers={ssid_device_identifier},
                    # The name, model, etc., for the SSID "device" itself are set during its
                    # registration in SSIDDeviceCoordinator. We don't need to redefine them here,
                    # just link to it using its identifier.
                    # The via_device for the SSID "device" (linking it to the Network device)
                    # is also handled during its registration in SSIDDeviceCoordinator.
                )
            else:
                # This case should ideally not happen if ssid_info_data is correctly populated.
                _LOGGER.warning(
                    "SSID-specific entity for SSID '%s' (Number: %s) is missing 'networkId' "
                    "in its data, cannot link to SSID device. Falling back to physical device linkage if possible.",
                    self._ssid_name or "Unknown", self._ssid_number
                )
                # Fall-through to physical device linking logic below if network_id is missing.
                # This might lead to incorrect association in the UI.

        # Scenario 2: Entity is related to a physical Meraki device (AP, Switch, Gateway).
        # This means _device_serial should be present (derived from _device_info_data).
        # The entity will be linked directly to this physical device in Home Assistant.
        # Resulting hierarchy: Sensor Entity -> Physical Device -> Config Entry.

        # Check for device_serial, which is essential for physical device identification.
        # If an SSID entity fell through due to missing network_id but also lacks a serial
        # (because _device_info_data was actually SSID data without a 'serial' field),
        # then it cannot be properly linked.
        if not self._device_serial:
            _LOGGER.warning(
                "Meraki entity cannot determine device_info: "
                "Missing serial for physical device context, or missing networkId for SSID context. "
                "Entity ID if available: %s",
                self.entity_id if self.hass else "Unknown Entity ID",
            )
            return None

        # If we've reached here, it's either a physical device entity,
        # or an SSID entity that failed to link to an SSID device and is attempting fallback.
        _LOGGER.debug( # Changed from error to debug as this path is normal for physical devices
            "MERAKI_DEVICE_NAMING_DEBUG: device_info resolving for physical device context: S/N %s",
            self._device_serial
        )
        # Get the raw device name (name from API or serial)
        # self._device_name is already pre-calculated in __init__ to be name or
        # serial
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

        # Default: This entity is directly related to the physical Meraki
        # device
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
