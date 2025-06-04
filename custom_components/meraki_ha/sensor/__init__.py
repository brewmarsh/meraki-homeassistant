"""Sensor platform for the Meraki Home Assistant integration.

This platform sets up various sensor entities for Meraki devices and SSIDs,
including device status, client counts, network information, and SSID-specific
details like availability and channel usage. It uses data coordinators to
fetch and manage data from the Meraki API.
"""

import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Assuming these consts correctly point to the keys used in hass.data for coordinators
from ..const import (
    DOMAIN,
    DATA_COORDINATOR,
    # DATA_COORDINATORS, # Unused
    DATA_SSID_DEVICES_COORDINATOR,
)

# Import coordinator types
from ..coordinators.base_coordinator import MerakiDataUpdateCoordinator
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator

# Import sensor entity classes for physical devices - These are now dynamically loaded via sensor_registry
# from .device_status import MerakiDeviceStatusSensor # Unused
# from .uplink_status import MerakiUplinkStatusSensor # Unused
# Import for connected clients sensor for physical APs
# from .connected_clients import MerakiDeviceConnectedClientsSensor # Unused

# Import new MX-specific sensors - These are now dynamically loaded via sensor_registry
# from .meraki_wan1_connectivity import MerakiWAN1ConnectivitySensor # Unused
# from .meraki_wan2_connectivity import MerakiWAN2ConnectivitySensor # Unused
# from .meraki_network_info import MerakiNetworkInfoSensor # Unused
# from .meraki_firmware_status import MerakiFirmwareStatusSensor # Unused

# Import from sensor_registry
from ..sensor_registry import (
    COMMON_DEVICE_SENSORS,
    get_sensors_for_device_type,
)

# Import sensor entity classes for SSIDs
# from .ssid_availability import MerakiSSIDAvailabilitySensor # Now created by factory
# from .ssid_channel import MerakiSSIDChannelSensor # Now created by factory
# from .ssid_client_count import MerakiSSIDClientCountSensor # Now created by factory

# Import the factory function for SSID sensors
from .ssid import create_ssid_sensors

# Import the new organization-level sensor
from .org_device_type_clients import MerakiOrgDeviceTypeClientsSensor


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki sensor entities from a config entry.

    This function is responsible for initializing and adding sensor entities
    for both physical Meraki devices (APs, switches, gateways) and Meraki
    SSIDs. It retrieves data from the main data coordinator and the SSID
    device coordinator, then creates sensor entities based on this data.

    Physical device sensors are determined by common sensors applicable to all
    devices and productType-specific sensors defined in the SENSOR_REGISTRY.

    SSID sensors (e.g., availability, channel, client count) are created
    using a factory function for each enabled SSID managed by the
    SSIDDeviceCoordinator.

    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry for this Meraki integration instance.
        async_add_entities: Callback function to add entities to Home Assistant.
    """
    _LOGGER.info("Meraki HA: Setting up sensor platform.")  # Adjusted
    entities = []
    _LOGGER.debug("Meraki HA: Initial entities list id: %s", id(entities))

    # Get the entry specific data store
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Get the main data coordinator for physical devices
    main_coordinator: MerakiDataUpdateCoordinator = entry_data.get(DATA_COORDINATOR)

    # --- Organization-level Sensor Setup ---
    if main_coordinator and main_coordinator.data:
        organization_id = main_coordinator.meraki_client.org_id
        # Attempt to get org_name, fallback to org_id if not available
        organization_name = getattr(main_coordinator.meraki_client, "org_name", organization_id)

        try:
            org_client_sensor = MerakiOrgDeviceTypeClientsSensor(
                coordinator=main_coordinator,
                organization_id=organization_id,
                organization_name=organization_name,
            )
            entities.append(org_client_sensor)
            _LOGGER.debug(
                "Meraki HA: Added MerakiOrgDeviceTypeClientsSensor for organization %s",
                organization_name,
            )
        except Exception as e:
            _LOGGER.error(
                "Meraki HA: Error adding MerakiOrgDeviceTypeClientsSensor for organization %s: %s",
                organization_name,
                e,
            )
    else:
        _LOGGER.warning(
            "Main coordinator not available or has no data; skipping organization-level sensors."
        )


    # --- Physical Device Sensor Setup ---
    # Iterate through physical devices fetched by the main_coordinator
    # and create sensors based on COMMON_DEVICE_SENSORS and productType-specific sensors.
    if main_coordinator and main_coordinator.data:
        physical_devices = main_coordinator.data.get("devices", [])
        _LOGGER.debug(
            "Meraki HA: Found %d physical devices for sensor setup.",
            len(physical_devices),
        )  # Adjusted
        for (
            device_info
        ) in physical_devices:  # For each physical Meraki device (AP, switch, gateway)
            serial = device_info.get("serial")
            if not serial:
                _LOGGER.warning(
                    f"Skipping device with missing serial: {device_info.get('name', 'Unknown Name')}"
                )
                continue

            _LOGGER.debug(
                "Meraki HA: Setting up physical device sensors for: %s",
                device_info.get("name", serial),
            )  # Adjusted

            # Add common sensors for all devices
            for sensor_class in COMMON_DEVICE_SENSORS:
                try:
                    entities.append(sensor_class(main_coordinator, device_info))
                    _LOGGER.debug(
                        "Meraki HA: Added common sensor %s for %s",
                        sensor_class.__name__,
                        device_info.get("name", serial),
                    )
                except Exception as e:
                    _LOGGER.error(
                        "Meraki HA: Error adding common sensor %s for %s: %s",
                        sensor_class.__name__,
                        device_info.get("name", serial),
                        e,
                    )

            # Add productType-specific sensors
            product_type = device_info.get("productType")
            _LOGGER.debug(  # Keep this important logging
                "Meraki HA: Processing device for sensor setup. Serial: %s, Model: %s, Name: %s, ProductType from data: %s",
                serial,  # Ensure 'serial' is defined in this scope from device_info.get("serial")
                device_info.get("model"),
                device_info.get("name"),
                product_type,
            )

            if product_type:
                sensors_for_type = get_sensors_for_device_type(product_type)
                if not sensors_for_type:
                    _LOGGER.debug(
                        "Meraki HA: No specific sensor classes defined in registry for productType '%s' for device %s",
                        product_type,
                        device_info.get("name", serial),
                    )
                for sensor_class in sensors_for_type:
                    try:
                        entities.append(sensor_class(main_coordinator, device_info))
                        _LOGGER.debug(
                            "Meraki HA: Added sensor %s for %s (productType: %s)",
                            sensor_class.__name__,
                            device_info.get("name", serial),
                            product_type,
                        )
                    except Exception as e:
                        _LOGGER.error(
                            "Meraki HA: Error adding sensor %s for %s (productType: %s): %s",
                            sensor_class.__name__,
                            device_info.get("name", serial),
                            product_type,
                            e,
                        )
            else:
                _LOGGER.debug(
                    "Meraki HA: No productType found for device %s, skipping productType-specific sensors.",
                    device_info.get("name", serial),
                )

    else:
        _LOGGER.warning(
            "Main coordinator not available or has no data; skipping physical device sensors."
        )
    _LOGGER.debug(
        "Meraki HA: Entities list id AFTER physical devices loop: %s. Current len: %d",
        id(entities),
        len(entities),
    )

    # Get the SSID device coordinator
    # This coordinator manages SSIDs as logical "devices" in Home Assistant.
    # Ensure DATA_SSID_DEVICES_COORDINATOR is the correct key used during coordinator setup in __init__.py of the component
    ssid_coordinator: SSIDDeviceCoordinator = entry_data.get(
        DATA_SSID_DEVICES_COORDINATOR
    )

    # --- SSID "Device" Sensor Setup ---
    # Iterate through enabled SSIDs fetched by the ssid_coordinator
    # and create a set of sensors for each SSID using the create_ssid_sensors factory.
    if ssid_coordinator and ssid_coordinator.data:
        # ssid_coordinator.data is a dict of {unique_ssid_id: ssid_info_dict}
        # Values are the actual data dictionaries for each SSID
        enabled_ssids_info_list = list(
            ssid_coordinator.data.values()
        )  # Get list of SSID data dicts
        _LOGGER.debug(
            "Meraki HA: Found %d enabled SSIDs for sensor setup from SSIDDeviceCoordinator.",
            len(enabled_ssids_info_list),
        )  # Adjusted

        for ssid_info_data in enabled_ssids_info_list:  # For each enabled SSID
            # `unique_id` within ssid_info_data is the identifier for the SSID "device" in HA.
            # This was created by the SSIDDeviceCoordinator.
            # For MerakiEntity-based SSID sensors, `ssid_info_data` is passed as both `device_data` (for MerakiEntity's _device_info_data)
            # and `ssid_data` (for MerakiEntity's _ssid_info_data). This allows the entity to
            # correctly link to the SSID "device" and access SSID-specific attributes.
            unique_identifier_for_log = (
                ssid_info_data.get("unique_id")
                or f"{ssid_info_data.get('networkId')}_{ssid_info_data.get('number')}"
            )
            _LOGGER.debug(
                "Meraki HA: Setting up SSID sensors for: %s (Name: %s)",
                unique_identifier_for_log,
                ssid_info_data.get("name", "Unknown SSID"),
            )  # Adjusted

            # Call the factory function to create all standard sensors for this SSID
            # (e.g., availability, channel, client count).
            new_ssid_sensors = create_ssid_sensors(
                ssid_coordinator, ssid_info_data, ssid_info_data
            )
            entities.extend(new_ssid_sensors)
            _LOGGER.debug(
                "Meraki HA: Added %d sensors for SSID %s",
                len(new_ssid_sensors),
                ssid_info_data.get("name", unique_identifier_for_log),
            )
    else:
        _LOGGER.warning(
            "SSID coordinator (SSIDDeviceCoordinator) not available or has no data; skipping SSID sensors."
        )

    _LOGGER.debug(
        "Meraki HA: FINAL check before async_add_entities. Total entities in list: %d. First 5 unique_ids: %s. Last 5 unique_ids: %s",
        len(entities),
        [e.unique_id for e in entities[:5] if hasattr(e, "unique_id")],
        [e.unique_id for e in entities[-5:] if hasattr(e, "unique_id")],
    )
    # New log for id(entities) at FINAL check
    _LOGGER.debug("Meraki HA: Entities list id FINAL check: %s", id(entities))
    if entities:
        _LOGGER.info(
            "Meraki HA: Adding %d Meraki sensor entities.", len(entities)
        )  # Adjusted
        async_add_entities(entities)
    else:
        _LOGGER.info("Meraki HA: No Meraki sensor entities to add.")  # Adjusted
