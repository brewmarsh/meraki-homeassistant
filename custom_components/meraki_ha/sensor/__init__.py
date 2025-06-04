import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
# Assuming these consts correctly point to the keys used in hass.data for coordinators
from ..const import DOMAIN, DATA_COORDINATOR, DATA_COORDINATORS, DATA_SSID_DEVICES_COORDINATOR 

# Import coordinator types
from ..coordinators.base_coordinator import MerakiDataUpdateCoordinator
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator

# Import sensor entity classes for physical devices
from .device_status import MerakiDeviceStatusSensor
from .uplink_status import MerakiUplinkStatusSensor
# Import for connected clients sensor for physical APs
from .connected_clients import MerakiDeviceConnectedClientsSensor 

# Import new MX-specific sensors
from .meraki_wan1_connectivity import MerakiWAN1ConnectivitySensor
from .meraki_wan2_connectivity import MerakiWAN2ConnectivitySensor
from .meraki_network_info import MerakiNetworkInfoSensor
from .meraki_firmware_status import MerakiFirmwareStatusSensor

# Import from sensor_registry
from ..sensor_registry import SENSOR_REGISTRY, COMMON_DEVICE_SENSORS, get_sensors_for_device_type

# Import sensor entity classes for SSIDs
# from .ssid_availability import MerakiSSIDAvailabilitySensor # Now created by factory
# from .ssid_channel import MerakiSSIDChannelSensor # Now created by factory
# from .ssid_client_count import MerakiSSIDClientCountSensor # Now created by factory

# Import the factory function for SSID sensors
from .ssid import create_ssid_sensors


_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    _LOGGER.info("Meraki HA: Setting up sensor platform.") # Adjusted
    entities = []
    _LOGGER.debug("Meraki HA: Initial entities list id: %s", id(entities))

    # Get the entry specific data store
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Get the main data coordinator for physical devices
    main_coordinator: MerakiDataUpdateCoordinator = entry_data.get(DATA_COORDINATOR)

    if main_coordinator and main_coordinator.data:
        physical_devices = main_coordinator.data.get("devices", [])
        _LOGGER.debug("Meraki HA: Found %d physical devices for sensor setup.", len(physical_devices)) # Adjusted
        for device_info in physical_devices:
            serial = device_info.get("serial")
            if not serial: 
                _LOGGER.warning(f"Skipping device with missing serial: {device_info.get('name', 'Unknown Name')}")
                continue

            _LOGGER.debug("Meraki HA: Setting up physical device sensors for: %s", device_info.get('name', serial)) # Adjusted
            
            # Add common sensors for all devices
            for sensor_class in COMMON_DEVICE_SENSORS:
                try:
                    entities.append(sensor_class(main_coordinator, device_info))
                    _LOGGER.debug("Meraki HA: Added common sensor %s for %s", sensor_class.__name__, device_info.get('name', serial))
                except Exception as e:
                    _LOGGER.error("Meraki HA: Error adding common sensor %s for %s: %s", sensor_class.__name__, device_info.get('name', serial), e)

            # Add productType-specific sensors
            product_type = device_info.get("productType")
            _LOGGER.debug( # Keep this important logging
                "Meraki HA: Processing device for sensor setup. Serial: %s, Model: %s, Name: %s, ProductType from data: %s",
                serial, # Ensure 'serial' is defined in this scope from device_info.get("serial")
                device_info.get("model"),
                device_info.get("name"),
                product_type,
            )

            if product_type:
                sensors_for_type = get_sensors_for_device_type(product_type)
                if not sensors_for_type:
                    _LOGGER.debug("Meraki HA: No specific sensor classes defined in registry for productType '%s' for device %s", product_type, device_info.get('name', serial))
                for sensor_class in sensors_for_type:
                    try:
                        entities.append(sensor_class(main_coordinator, device_info))
                        _LOGGER.debug("Meraki HA: Added sensor %s for %s (productType: %s)", sensor_class.__name__, device_info.get('name', serial), product_type)
                    except Exception as e:
                        _LOGGER.error("Meraki HA: Error adding sensor %s for %s (productType: %s): %s", sensor_class.__name__, device_info.get('name', serial), product_type, e)
            else:
                _LOGGER.debug("Meraki HA: No productType found for device %s, skipping productType-specific sensors.", device_info.get('name', serial))

    else:
        _LOGGER.warning("Main coordinator not available or has no data; skipping physical device sensors.")
    _LOGGER.debug("Meraki HA: Entities list id AFTER physical devices loop: %s. Current len: %d", id(entities), len(entities))

    # Get the SSID device coordinator
    # Ensure DATA_SSID_DEVICES_COORDINATOR is the correct key used during coordinator setup in __init__.py of the component
    ssid_coordinator: SSIDDeviceCoordinator = entry_data.get(DATA_SSID_DEVICES_COORDINATOR)

    if ssid_coordinator and ssid_coordinator.data:
        # ssid_coordinator.data is a dict of {unique_ssid_id: ssid_info_dict}
        # Values are the actual data dictionaries for each SSID
        enabled_ssids_info_list = list(ssid_coordinator.data.values())
        _LOGGER.debug("Meraki HA: Found %d enabled SSIDs for sensor setup from SSIDDeviceCoordinator.", len(enabled_ssids_info_list)) # Adjusted

        for ssid_info_data in enabled_ssids_info_list:
            # unique_ssid_id is expected to be part of ssid_info_data, put there by SSIDDeviceCoordinator
            # Or, if not, the factory/sensors will need to construct it from networkId and SSID number.
            # For MerakiEntity, passing ssid_info_data as both device_data and ssid_data
            # means it will look for networkId and number within this dict.

            unique_identifier_for_log = ssid_info_data.get("unique_id") or f"{ssid_info_data.get('networkId')}_{ssid_info_data.get('number')}"
            _LOGGER.debug("Meraki HA: Setting up SSID sensors for: %s (Name: %s)", unique_identifier_for_log, ssid_info_data.get('name', 'Unknown SSID')) # Adjusted

            # Call the factory function to create all sensors for this SSID
            # Passing ssid_info_data as both 'device_data' and 'ssid_data' arguments
            # This assumes MerakiEntity and individual sensor classes can derive
            # necessary info (like networkId for device_info linking) from this combined data.
            new_ssid_sensors = create_ssid_sensors(ssid_coordinator, ssid_info_data, ssid_info_data)
            entities.extend(new_ssid_sensors)
            _LOGGER.debug("Meraki HA: Added %d sensors for SSID %s", len(new_ssid_sensors), ssid_info_data.get('name', unique_identifier_for_log))
    else:
        _LOGGER.warning("SSID coordinator (SSIDDeviceCoordinator) not available or has no data; skipping SSID sensors.")
        
    _LOGGER.debug(
        "Meraki HA: FINAL check before async_add_entities. Total entities in list: %d. First 5 unique_ids: %s. Last 5 unique_ids: %s",
        len(entities),
        [e.unique_id for e in entities[:5] if hasattr(e, 'unique_id')],
        [e.unique_id for e in entities[-5:] if hasattr(e, 'unique_id')]
    )
    # New log for id(entities) at FINAL check
    _LOGGER.debug("Meraki HA: Entities list id FINAL check: %s", id(entities))
    if entities:
        _LOGGER.info("Meraki HA: Adding %d Meraki sensor entities.", len(entities)) # Adjusted
        async_add_entities(entities)
    else:
        _LOGGER.info("Meraki HA: No Meraki sensor entities to add.") # Adjusted
