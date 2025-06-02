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

# Import sensor entity classes for SSIDs
from .ssid_availability import MerakiSSIDAvailabilitySensor
from .ssid_channel import MerakiSSIDChannelSensor
from .ssid_client_count import MerakiSSIDClientCountSensor


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
            
            # Always add DeviceStatusSensor
            entities.append(MerakiDeviceStatusSensor(main_coordinator, device_info))
            _LOGGER.debug("Meraki HA: Added MerakiDeviceStatusSensor for %s", device_info.get('name', serial))

            product_type = device_info.get("productType")
            
            _LOGGER.debug(
                "Meraki HA: Entities count for %s (Serial: %s) BEFORE 'appliance' check: %d",
                device_info.get('name', serial),
                serial,
                len(entities)
            )
            # Combined log for product_type check and entities list id
            _LOGGER.debug(
                "Meraki HA: Checking product_type for device %s (Serial: %s). product_type is '%s' (Type: %s). Entities list id: %s. Current len: %d",
                device_info.get('name', serial),
                serial,
                product_type,
                type(product_type).__name__,
                id(entities),
                len(entities)
            )

            if product_type == "appliance":
                _LOGGER.debug("Meraki HA: Device %s IS an appliance. Attempting to add MerakiNetworkInfoSensor.", device_info.get('name', serial))
                entities.append(MerakiNetworkInfoSensor(main_coordinator, device_info))
                _LOGGER.debug("Meraki HA: Added MerakiNetworkInfoSensor for %s", device_info.get('name', serial))
                _LOGGER.debug(
                    "Meraki HA: Entities list id (inside appliance block, after appends) for %s: %s. Current len: %d",
                    serial,
                    id(entities),
                    len(entities)
                )
            # Temporarily comment out other appliance sensors
            #    entities.append(MerakiUplinkStatusSensor(main_coordinator, device_info))
            #    entities.append(MerakiWAN1ConnectivitySensor(main_coordinator, device_info))
            #    entities.append(MerakiWAN2ConnectivitySensor(main_coordinator, device_info))
            #    entities.append(MerakiFirmwareStatusSensor(main_coordinator, device_info))
            #    _LOGGER.debug("Meraki HA: Added new MX-specific sensors for %s", device_info.get('name', serial))
            
            # Temporarily comment out wireless specific sensors
            # if product_type == "wireless": # Standard check for MR devices
            #    entities.append(MerakiDeviceConnectedClientsSensor(main_coordinator, device_info))

            _LOGGER.debug(
                "Meraki HA: Entities count for %s (Serial: %s) AFTER 'appliance' check logic: %d. Last entity unique_id: %s",
                device_info.get('name', serial),
                serial,
                len(entities),
                entities[-1].unique_id if entities and hasattr(entities[-1], 'unique_id') else "N/A"
            )

    else:
        _LOGGER.warning("Main coordinator not available or has no data; skipping physical device sensors.")
    _LOGGER.debug("Meraki HA: Entities list id AFTER physical devices loop: %s. Current len: %d", id(entities), len(entities))

    # Get the SSID device coordinator from the nested 'coordinators' dictionary
    # coordinators_dict = entry_data.get(DATA_COORDINATORS, {})
    # ssid_coordinator: SSIDDeviceCoordinator = coordinators_dict.get(DATA_SSID_DEVICES_COORDINATOR)

    # if ssid_coordinator and ssid_coordinator.data:
    #    # ssid_coordinator.data is a dict of {unique_ssid_id: ssid_data_dict}
    #    enabled_ssids_data = ssid_coordinator.data.values()
    #    _LOGGER.debug("Meraki HA: Found %d enabled SSIDs for sensor setup.", len(enabled_ssids_data)) # Adjusted
    #    for ssid_data in enabled_ssids_data:
    #        unique_ssid_id = ssid_data.get("unique_id")
    #        if not unique_ssid_id:
    #            _LOGGER.warning(f"Skipping SSID with missing unique_id: {ssid_data.get('name', 'Unknown SSID')}")
    #            continue
    #
    #        _LOGGER.debug("Meraki HA: Setting up SSID sensors for: %s", ssid_data.get('name', unique_ssid_id)) # Adjusted
    #        entities.append(MerakiSSIDAvailabilitySensor(ssid_coordinator, ssid_data))
    #        entities.append(MerakiSSIDChannelSensor(ssid_coordinator, ssid_data)) 
    #        entities.append(MerakiSSIDClientCountSensor(ssid_coordinator, ssid_data))
    # else:
    #    _LOGGER.warning("SSID coordinator not available or has no data; skipping SSID sensors.")
        
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
