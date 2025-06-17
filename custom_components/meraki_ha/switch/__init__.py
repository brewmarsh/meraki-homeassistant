# custom_components/meraki_ha/switch/__init__.py
"""Switch platform for Meraki to control SSID and Camera settings."""

import logging
from typing import Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import (
    DOMAIN,
    DATA_CLIENT,
    DATA_COORDINATOR, # Main coordinator for physical devices
    DATA_SSID_DEVICES_COORDINATOR, # SSID coordinator
)
from ..meraki_api import MerakiAPIClient
from ..coordinators import MerakiDataUpdateCoordinator # Main coordinator type
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator

# Import SSID switch classes (original functionality)
from .meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
)

# Import Camera switch classes (new functionality)
from .camera_settings import (
    MerakiCameraSenseSwitch,
    MerakiCameraAudioDetectionSwitch,
    MerakiCameraRTSPSwitch,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki switches from a config entry."""
    _LOGGER.info("Meraki HA: Setting up switch platform.")
    entities_to_add = []

    # Get the entry specific data store
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    meraki_api_client: MerakiAPIClient = entry_data.get(DATA_CLIENT)

    if not meraki_api_client:
        _LOGGER.error("Meraki API client not found. Cannot set up switches.")
        return False

    # --- SSID Switch Setup (existing functionality) ---
    coordinators_map = entry_data.get("coordinators")
    ssid_coordinator: Optional[SSIDDeviceCoordinator] = None
    if coordinators_map:
        ssid_coordinator = coordinators_map.get(DATA_SSID_DEVICES_COORDINATOR)

    if ssid_coordinator and ssid_coordinator.data:
        _LOGGER.debug("Setting up SSID switches.")
        for ssid_unique_id, ssid_data in ssid_coordinator.data.items():
            try: # Added try-except for individual SSID switch creation
                entities_to_add.append(
                    MerakiSSIDEnabledSwitch(
                        ssid_coordinator, meraki_api_client, config_entry, ssid_unique_id, ssid_data
                    )
                )
                entities_to_add.append(
                    MerakiSSIDBroadcastSwitch(
                        ssid_coordinator, meraki_api_client, config_entry, ssid_unique_id, ssid_data
                    )
                )
            except Exception as e_ssid:
                _LOGGER.error("Error creating SSID switches for %s: %s", ssid_unique_id, e_ssid, exc_info=True)
    else:
        _LOGGER.info("SSID coordinator not available or no data; skipping SSID switch setup.")

    # --- Camera Switch Setup (new functionality) ---
    main_coordinator: Optional[MerakiDataUpdateCoordinator] = entry_data.get(DATA_COORDINATOR)

    if main_coordinator and main_coordinator.data:
        physical_devices = main_coordinator.data.get("devices", [])
        _LOGGER.debug("Found %d physical devices for camera switch setup.", len(physical_devices))
        for device_info in physical_devices:
            serial = device_info.get("serial")
            product_type = device_info.get("productType", "").lower()
            model = device_info.get("model", "").upper()

            if not serial:
                _LOGGER.warning("Skipping device with missing serial for camera switch setup.")
                continue

            # Check if the device is a camera
            if product_type == "camera" or model.startswith("MV"):
                _LOGGER.debug("Setting up camera switches for device: %s", device_info.get("name", serial))
                try:
                    entities_to_add.append(
                        MerakiCameraSenseSwitch(
                            main_coordinator, meraki_api_client, device_info
                        )
                    )
                    entities_to_add.append(
                        MerakiCameraAudioDetectionSwitch(
                            main_coordinator, meraki_api_client, device_info
                        )
                    )
                    entities_to_add.append(
                        MerakiCameraRTSPSwitch(
                            main_coordinator, meraki_api_client, device_info
                        )
                    )
                except Exception as e_cam:
                    _LOGGER.error(
                        "Error creating camera switches for %s: %s",
                        device_info.get("name", serial),
                        e_cam,
                        exc_info=True # Added exc_info for better diagnostics
                    )
    else:
        _LOGGER.info("Main coordinator not available or no data; skipping camera switch setup.")

    if entities_to_add:
        _LOGGER.info("Adding %d Meraki switch entities.", len(entities_to_add))
        async_add_entities(entities_to_add, update_before_add=True)
    else:
        _LOGGER.info("No Meraki switch entities to add.")
    return True


__all__ = ["async_setup_entry"]
