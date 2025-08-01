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
from .core.coordinators.device import MerakiDeviceCoordinator
from .const import DOMAIN

# map_meraki_model_to_device_type is now used via format_device_name
# from .coordinators.meraki_device_types import map_meraki_model_to_device_type
from .helpers.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)


class MerakiEntity(CoordinatorEntity[MerakiDeviceCoordinator]):
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
    _attr_has_entity_name = True
    entity_category = None

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
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

        _LOGGER.debug(
            "MerakiEntity: Initializing for device S/N: %s, Name: %s",
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
        # This means the entity represents a sensor or switch *for an SSID itself* (e.g., SSID availability, SSID client count).
        # In this case, _ssid_info_data will be populated (it's the SSID's own data dict from the coordinator),
        # and _ssid_number will be derived from it.
        # The `device_info` should then point to the "SSID Device" in Home Assistant's device registry.
        # This "SSID Device" is a logical representation, expected to be registered by `MerakiNetworkCoordinator`
        # with an identifier like (DOMAIN, f"{network_id}_{ssid_number}").
        # This "SSID Device" is, in turn, typically linked via `via_device` to its parent "Network Device".
        # Resulting hierarchy for an SSID-specific sensor: Sensor Entity -> SSID Device -> Network Device -> Config Entry.
        if (
            self._ssid_info_data and self._ssid_number is not None
        ):  # Indicates this entity is for an SSID.
            # For SSID entities, `_device_info_data` (passed during __init__) is actually the SSID's own data dictionary.
            # We need 'networkId' from this dict to form the unique identifier for the SSID "device".
            network_id = self._device_info_data.get("networkId")

            if network_id:
                # Construct the unique identifier for the SSID "device".
                ssid_device_identifier = (DOMAIN, f"{network_id}_{self._ssid_number}")
                # This entity (e.g., SSID Availability Sensor, SSID Client Count Sensor)
                # will be associated with this specific SSID "device".
                return DeviceInfo(
                    identifiers={ssid_device_identifier},
                    # Note: The name, model, etc., for the SSID "device" itself are typically set
                    # when the SSID "device" is first registered (e.g., in SSIDDeviceCoordinator).
                    # Here, we are just linking this *entity* to that existing (or to-be-created) SSID "device".
                    # The `via_device` attribute, linking the SSID "device" to its parent Network "device",
                    # is also handled during the SSID "device's" registration.
                )
            else:
                # This is an edge case: if we have SSID info but it lacks a 'networkId',
                # we cannot reliably link it to an SSID "device".
                _LOGGER.warning(
                    "SSID-specific entity for SSID '%s' (Number: %s) is missing 'networkId' "
                    "in its data, cannot link to SSID device. Falling back to physical device linkage if possible.",
                    self._ssid_name or "Unknown",
                    self._ssid_number,
                )
                # Fall-through to physical device linking logic below if network_id is missing.
                # This might lead to incorrect association in the UI, or failure if _device_serial is also missing.

        # Scenario 2: Entity is related to a physical Meraki device (AP, Switch, Gateway),
        # OR it's an SSID entity that failed the above linking (e.g., missing network_id).
        # For physical devices, `_device_serial` (derived from `_device_info_data` in `__init__`) is the key.
        # The entity will be linked directly to this physical device in Home Assistant.
        # Resulting hierarchy for a physical device sensor: Sensor Entity -> Physical Device -> Config Entry.

        # Check for `_device_serial`. This is essential for physical device identification.
        # If an SSID entity fell through from Scenario 1 (due to missing network_id) AND also lacks a `_device_serial`
        # (because `_device_info_data` was SSID data which doesn't have 'serial'), then it cannot be properly linked.
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
        _LOGGER.debug(
            "MerakiEntity: device_info resolving for physical device context: S/N %s",
            self._device_serial,
        )
        # Get the raw device name (name from API or serial as fallback).
        # `self._device_name` is pre-calculated in `__init__` to be the API name or serial.
        device_name_raw = self._device_name or "Unknown Meraki Device"

        # Retrieve device name formatting option from config entry options via coordinator.
        # This allows users to choose how device names are displayed (e.g., with type prefix/suffix).
        device_name_format_option = (
            self.coordinator.device_name_format
        )  # Property on main coordinator

        # Use the new helper function to format the device name
        formatted_device_name = format_device_name(
            device_name_raw=device_name_raw,
            device_model=self._device_model or "",
            device_name_format_option=device_name_format_option,
            is_org_device=False,  # This is for physical devices
        )

        _LOGGER.debug(
            "MerakiEntity: Device Info for S/N %s: Raw Name='%s', Model='%s', FormatOption='%s', Final Formatted Name='%s'",
            self._device_serial,
            device_name_raw,
            self._device_model or "",
            device_name_format_option,
            formatted_device_name,
        )

        # Construct DeviceInfo for a physical Meraki device.
        # This entity will be linked to the device identified by its serial number.
        device_info_to_return = DeviceInfo(
            identifiers={
                (DOMAIN, self._device_serial)
            },  # Unique identifier for the physical device.
            name=str(formatted_device_name),  # User-friendly name with formatting.
            manufacturer="Cisco Meraki",
            model=str(self._device_model or "Unknown"),
            sw_version=str(self._device_firmware or ""),
        )
        # Removed verbose logging of the full DeviceInfo object
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
