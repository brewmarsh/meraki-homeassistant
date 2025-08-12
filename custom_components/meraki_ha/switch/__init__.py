"""Switch platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import (
    DOMAIN,
    DATA_CLIENT,
)
from ..core.api.client import MerakiAPIClient
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
        coordinator = entry_data["coordinator"]

    except KeyError as e:
        _LOGGER.error(
            "Switch platform: Essential data not found in hass.data for entry %s. Error: %s",
            config_entry.entry_id,
            e,
        )
        return False

    new_entities: list = []

    # Setup Camera Setting Switches
    if coordinator and coordinator.data and "devices" in coordinator.data:
        for device_info in coordinator.data["devices"]:
            if not isinstance(device_info, dict):
                continue

            serial = device_info.get("serial")
            product_type = str(device_info.get("productType", "")).lower()
            model = str(device_info.get("model", "")).upper()

            if serial and (product_type == "camera" or model.startswith("MV")):
                new_entities.extend(
                    [
                        MerakiCameraSenseSwitch(
                            coordinator, meraki_client, device_info
                        ),
                        MerakiCameraAudioDetectionSwitch(
                            coordinator, meraki_client, device_info
                        ),
                        MerakiCameraRTSPSwitch(coordinator, meraki_client, device_info),
                    ]
                )
    else:
        _LOGGER.info(
            "No camera devices found or main coordinator data missing for camera switches."
        )

    # Setup SSID Switches
    if coordinator and coordinator.data and "ssids" in coordinator.data:
        for ssid_data in coordinator.data["ssids"]:
            if not isinstance(ssid_data, dict):
                continue

            if "networkId" not in ssid_data or "number" not in ssid_data:
                continue
            new_entities.extend(
                [
                    MerakiSSIDEnabledSwitch(
                        coordinator,
                        meraki_client,
                        config_entry,
                        ssid_data,
                    ),
                    MerakiSSIDBroadcastSwitch(
                        coordinator,
                        meraki_client,
                        config_entry,
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
