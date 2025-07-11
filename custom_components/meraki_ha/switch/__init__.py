"""Switch platform for Meraki."""
import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN, DATA_CLIENT, DATA_COORDINATORS # Use DATA_COORDINATORS
from ..meraki_api import MerakiAPIClient
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator
from .meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
)
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
    """Set up Meraki switch entities from a config entry."""
    _LOGGER.info("Setting up Meraki switch platform for entry %s", config_entry.entry_id)

    try:
        entry_data = hass.data[DOMAIN][config_entry.entry_id]
        meraki_client: MerakiAPIClient = entry_data[DATA_CLIENT]

        # Get the main data coordinator for physical device switches (like camera settings)
        main_coordinator = entry_data[DATA_COORDINATORS].get("main")
        if not main_coordinator:
            _LOGGER.error("Switch platform: Main coordinator not found for entry %s", config_entry.entry_id)
            return False

        # Get the SSID device coordinator for SSID switches
        ssid_coordinator: SSIDDeviceCoordinator = entry_data[DATA_COORDINATORS].get("ssid_devices")
        if not ssid_coordinator:
            _LOGGER.error("Switch platform: SSID Device coordinator not found for entry %s", config_entry.entry_id)
            # Depending on design, this might not be fatal if no SSIDs or if other switches exist
            # For now, let's allow proceeding if main_coordinator is there for camera switches.
    except KeyError as e:
        _LOGGER.error(
            "Switch platform: Essential data not found in hass.data for entry %s. Error: %s",
            config_entry.entry_id,
            e
        )
        return False

    new_entities: list = []

    # Setup Camera Setting Switches
    if main_coordinator and main_coordinator.data and "devices" in main_coordinator.data:
        for device_info in main_coordinator.data["devices"]:
            if not isinstance(device_info, dict):
                _LOGGER.warning("Skipping non-dictionary device_info in main_coordinator data for camera switches.")
                continue

            serial = device_info.get("serial")
            product_type = str(device_info.get("productType", "")).lower()
            model = str(device_info.get("model", "")).upper()

            if serial and (product_type == "camera" or model.startswith("MV")):
                _LOGGER.debug("Found camera %s (%s), adding setting switches.", device_info.get('name', serial), serial)
                new_entities.extend(
                    [
                        MerakiCameraSenseSwitch(main_coordinator, meraki_client, device_info),
                        MerakiCameraAudioDetectionSwitch(main_coordinator, meraki_client, device_info),
                        MerakiCameraRTSPSwitch(main_coordinator, meraki_client, device_info),
                    ]
                )
    else:
        _LOGGER.info("No camera devices found or main coordinator data missing for camera switches.")


    # Setup SSID Switches
    if ssid_coordinator and ssid_coordinator.data:
        _LOGGER.debug("SSID Coordinator data available, setting up SSID switches. %s SSIDs found.", len(ssid_coordinator.data))
        for ssid_unique_id, ssid_data in ssid_coordinator.data.items():
            if not isinstance(ssid_data, dict):
                _LOGGER.warning("Skipping non-dictionary ssid_data for SSID unique_id %s", ssid_unique_id)
                continue

            _LOGGER.debug("Setting up switches for SSID: %s (Data: %s)", ssid_data.get('name', ssid_unique_id), ssid_data)
            new_entities.extend(
                [
                    MerakiSSIDEnabledSwitch(
                        ssid_coordinator, meraki_client, config_entry, ssid_unique_id, ssid_data
                    ),
                    MerakiSSIDBroadcastSwitch(
                        ssid_coordinator, meraki_client, config_entry, ssid_unique_id, ssid_data
                    ),
                ]
            )
    else:
        _LOGGER.info("SSID Coordinator data not available or no SSIDs found for setting up SSID switches.")

    if new_entities:
        async_add_entities(new_entities)
        _LOGGER.info("Added %d Meraki switch entities.", len(new_entities))
    else:
        _LOGGER.info("No Meraki switch entities were added.")

    return True
