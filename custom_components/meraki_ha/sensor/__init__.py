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
            entities.append(MerakiDeviceStatusSensor(main_coordinator, device_info))
            
            product_type = device_info.get("productType")
            _LOGGER.debug(
                "Meraki HA: Checking product_type for device %s (Serial: %s). product_type is '%s' (Type: %s)",
                device_info.get('name', serial),
                serial,
                product_type,
                type(product_type).__name__
            )
            _LOGGER.debug(
                "Meraki HA: Entities count for %s (Serial: %s) BEFORE 'appliance' check: %d",
                device_info.get('name', serial),
                serial,
                len(entities)
            )
            # Add UplinkStatusSensor only if the device has uplink information (typically gateways/appliances)
            if product_type == "appliance": # Standard check for MX devices
                 entities.append(MerakiUplinkStatusSensor(main_coordinator, device_info))
                 # Add new MX-specific sensors
                 entities.append(MerakiWAN1ConnectivitySensor(main_coordinator, device_info))
                 entities.append(MerakiWAN2ConnectivitySensor(main_coordinator, device_info))
                 entities.append(MerakiNetworkInfoSensor(main_coordinator, device_info))
                 entities.append(MerakiFirmwareStatusSensor(main_coordinator, device_info))
                 _LOGGER.debug("Meraki HA: Added new MX-specific sensors for %s", device_info.get('name', serial))
            _LOGGER.debug(
                "Meraki HA: Entities count for %s (Serial: %s) AFTER 'appliance' check logic: %d. Last entity unique_id: %s",
                device_info.get('name', serial),
                serial,
                len(entities),
                entities[-1].unique_id if entities and hasattr(entities[-1], 'unique_id') else "N/A"
            )
            
            # Add ConnectedClients sensor for wireless APs (MR series)
            if product_type == "wireless": # Standard check for MR devices
                entities.append(MerakiDeviceConnectedClientsSensor(main_coordinator, device_info))
            
            # Potentially add MerakiRadioSettingsSensor for 'wireless' productType if desired
            # from .sensor.radio_settings import MerakiRadioSettingsSensor
            # if product_type == "wireless":
            #     entities.append(MerakiRadioSettingsSensor(main_coordinator, device_info))

    else:
        _LOGGER.warning("Main coordinator not available or has no data; skipping physical device sensors.")

    # Get the SSID device coordinator from the nested 'coordinators' dictionary
    coordinators_dict = entry_data.get(DATA_COORDINATORS, {})
    ssid_coordinator: SSIDDeviceCoordinator = coordinators_dict.get(DATA_SSID_DEVICES_COORDINATOR)

    if ssid_coordinator and ssid_coordinator.data:
        # ssid_coordinator.data is a dict of {unique_ssid_id: ssid_data_dict}
        enabled_ssids_data = ssid_coordinator.data.values()
        _LOGGER.debug("Meraki HA: Found %d enabled SSIDs for sensor setup.", len(enabled_ssids_data)) # Adjusted
        for ssid_data in enabled_ssids_data:
            unique_ssid_id = ssid_data.get("unique_id")
            if not unique_ssid_id:
                _LOGGER.warning(f"Skipping SSID with missing unique_id: {ssid_data.get('name', 'Unknown SSID')}")
                continue

            _LOGGER.debug("Meraki HA: Setting up SSID sensors for: %s", ssid_data.get('name', unique_ssid_id)) # Adjusted
            # Assuming these sensor classes are designed to take (ssid_coordinator, ssid_data)
            # and link to the SSID HA device via ssid_data['unique_id']
            entities.append(MerakiSSIDAvailabilitySensor(ssid_coordinator, ssid_data))
            entities.append(MerakiSSIDChannelSensor(ssid_coordinator, ssid_data)) 
            entities.append(MerakiSSIDClientCountSensor(ssid_coordinator, ssid_data))
    else:
        _LOGGER.warning("SSID coordinator not available or has no data; skipping SSID sensors.")
        
    _LOGGER.debug(
        "Meraki HA: FINAL check before async_add_entities. Total entities in list: %d. First 5 unique_ids: %s. Last 5 unique_ids: %s",
        len(entities),
        [e.unique_id for e in entities[:5] if hasattr(e, 'unique_id')],
        [e.unique_id for e in entities[-5:] if hasattr(e, 'unique_id')]
    )
    if entities:
        _LOGGER.info("Meraki HA: Adding %d Meraki sensor entities.", len(entities)) # Adjusted
        async_add_entities(entities)
    else:
        _LOGGER.info("Meraki HA: No Meraki sensor entities to add.") # Adjusted
