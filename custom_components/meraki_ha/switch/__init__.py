"""Switch platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.switch import SwitchEntity

from ..const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki switch entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Add discovered entities
    discovered_entities = entry_data.get("entities", [])

    switch_entities = [e for e in discovered_entities if isinstance(e, SwitchEntity)]

    # The other switches are not created by the discovery service, so we need to create them here
    coordinator = entry_data["coordinator"]
    meraki_client = entry_data["client"]

    # Setup Camera Setting Switches
    if coordinator and coordinator.data and "devices" in coordinator.data:
        for device_info in coordinator.data["devices"]:
            if not isinstance(device_info, dict):
                continue

            serial = device_info.get("serial")
            product_type = str(device_info.get("productType", "")).lower()
            model = str(device_info.get("model", "")).upper()

            if serial and (product_type == "camera" or model.startswith("MV")):
                from .camera_profiles import (
                    MerakiCameraSenseSwitch,
                    MerakiCameraAudioDetectionSwitch,
                )
                from .camera_schedules import MerakiCameraRTSPSwitch
                switch_entities.extend(
                    [
                        MerakiCameraSenseSwitch(
                            coordinator, meraki_client, device_info
                        ),
                        MerakiCameraAudioDetectionSwitch(
                            coordinator, meraki_client, device_info
                        ),
                    ]
                )
                if not model.startswith("MV2"):
                    switch_entities.append(
                        MerakiCameraRTSPSwitch(coordinator, meraki_client, device_info),
                    )

    # Setup SSID Switches
    if coordinator and coordinator.data and "ssids" in coordinator.data:
        for ssid_data in coordinator.data["ssids"]:
            if not isinstance(ssid_data, dict):
                continue

            if "networkId" not in ssid_data or "number" not in ssid_data:
                continue
            from .meraki_ssid_device_switch import (
                MerakiSSIDEnabledSwitch,
                MerakiSSIDBroadcastSwitch,
            )
            switch_entities.extend(
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

    # Setup Client Blocker Switches (for wireless clients)
    ssid_firewall_coordinators = entry_data.get("ssid_firewall_coordinators", {})

    if coordinator and coordinator.data and "clients" in coordinator.data:
        # Create a lookup to find an SSID's number by its name for a given network
        ssid_lookup = {
            (ssid["networkId"], ssid["name"]): ssid["number"]
            for ssid in coordinator.data.get("ssids", [])
        }

        for client_data in coordinator.data["clients"]:
            if not isinstance(client_data, dict) or "mac" not in client_data:
                continue

            network_id = client_data.get("networkId")
            ssid_name = client_data.get("ssid")

            # Only create blocker switches for wireless clients on a known SSID
            if network_id and ssid_name:
                ssid_number = ssid_lookup.get((network_id, ssid_name))
                if ssid_number is not None:
                    coordinator_key = f"{network_id}_{ssid_number}"
                    firewall_coordinator = ssid_firewall_coordinators.get(
                        coordinator_key
                    )

                    if firewall_coordinator:
                        from .meraki_client_blocker import MerakiClientBlockerSwitch
                        switch_entities.append(
                            MerakiClientBlockerSwitch(
                                firewall_coordinator,
                                config_entry,
                                client_data,
                            )
                        )

    if switch_entities:
        async_add_entities(switch_entities)

    return True
