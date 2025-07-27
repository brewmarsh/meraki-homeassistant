"""Switch platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import (
    DOMAIN,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DATA_COORDINATORS,
    DATA_SSID_DEVICES_COORDINATOR,
)
from ..core.api.client import MerakiAPIClient
from ..core.coordinators.network import MerakiNetworkCoordinator
from .meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
)
from .camera_profiles import (
    MerakiCameraSenseSwitch,
    MerakiCameraAudioDetectionSwitch,
)
from .camera_schedules import MerakiCameraRTSPSwitch

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki switch entities from a config entry."""
    try:
        entry_data = hass.data[DOMAIN][config_entry.entry_id]
        meraki_client: MerakiAPIClient = entry_data[DATA_CLIENT]

        # Get the main data coordinator for physical device switches (like camera settings)
        device_coordinator = entry_data["device_coordinator"]
        network_coordinator: MerakiNetworkCoordinator = entry_data.get(
            "network_coordinator"
        )
    except KeyError as e:
        _LOGGER.error(
            "Switch platform: Essential data not found in hass.data for entry %s. Error: %s",
            config_entry.entry_id,
            e,
        )
        return False

    new_entities: list = []

    # Setup Camera Setting Switches
    if (
        device_coordinator
        and device_coordinator.data
        and "devices" in device_coordinator.data
    ):
        for device_info in device_coordinator.data["devices"]:
            if not isinstance(device_info, dict):
                continue

            serial = device_info.get("serial")
            product_type = str(device_info.get("productType", "")).lower()
            model = str(device_info.get("model", "")).upper()

            if serial and (product_type == "camera" or model.startswith("MV")):
                # _LOGGER.debug("Found camera %s (%s), adding setting switches.", device_info.get('name', serial), serial) # Removed
                new_entities.extend(
                    [
                        MerakiCameraSenseSwitch(
                            device_coordinator, meraki_client, device_info
                        ),
                        MerakiCameraAudioDetectionSwitch(
                            device_coordinator, meraki_client, device_info
                        ),
                        MerakiCameraRTSPSwitch(
                            device_coordinator, meraki_client, device_info
                        ),
                    ]
                )
    else:
        _LOGGER.info(
            "No camera devices found or main coordinator data missing for camera switches."
        )

    # Setup SSID Switches
    if network_coordinator and network_coordinator.data:
        # _LOGGER.debug("SSID Coordinator data available, setting up SSID switches. %s SSIDs found.", len(network_coordinator.data)) # Removed
        for ssid_unique_id, ssid_data in network_coordinator.data.items():
            if not isinstance(ssid_data, dict):
                continue

            # _LOGGER.debug("Setting up switches for SSID: %s (Data: %s)", ssid_data.get('name', ssid_unique_id), ssid_data) # Removed
            new_entities.extend(
                [
                    MerakiSSIDEnabledSwitch(
                        network_coordinator,
                        meraki_client,
                        config_entry,
                        ssid_unique_id,
                        ssid_data,
                    ),
                    MerakiSSIDBroadcastSwitch(
                        network_coordinator,
                        meraki_client,
                        config_entry,
                        ssid_unique_id,
                        ssid_data,
                    ),
                ]
            )
    else:
        _LOGGER.info(
            "Network Coordinator data not available or no SSIDs found for setting up SSID switches."
        )

    if new_entities:
        async_add_entities(new_entities)

    return True
