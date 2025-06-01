# custom_components/meraki_ha/sensor/__init__.py
"""Set up Meraki sensor entities."""
import asyncio
import logging
from functools import partial # Added import

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Attempt to import async_setup_entry from all known sensor modules
# It's assumed each module defines this function. If not, it will require individual handling.
# This is a forward-looking approach assuming modular setup for each sensor type.

_LOGGER = logging.getLogger(__name__)

# List of sensor modules that should have an async_setup_entry function
# (relative to the current 'sensor' package)
# This list needs to be maintained if new sensor types are added in separate files.
SENSOR_MODULES = [
    # ".meraki_ssid_psk", # Removed as per request
    ".ssid", # This would need an async_setup_entry, or its logic handled here
    ".connected_clients",
    ".device_status",
    ".network_clients",
    # ".network_status", # Assuming this was a typo or future module, common one is device_status
    ".radio_settings",
    ".uplink_status",
    # Note: ssid_availability, ssid_channel, ssid_client_count are typically
    # handled by the .ssid module's setup if it creates those sensors.
    # If .ssid has an async_setup_entry that calls create_ssid_sensors, it's covered.
    # If .ssid_availability was meant to be a separate file with its own async_setup_entry,
    # it would need to be listed here (e.g., ".ssid_availability").
    # Based on previous file structure, .ssid likely contained create_ssid_sensors.
    # For .ssid_availability.py to be loaded, it needs its own async_setup_entry
    # and to be listed here, e.g. ".ssid_availability"
]

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki sensor entities from a config entry."""
    _LOGGER.info("Setting up Meraki sensor platform using dynamic module loading.")

    platform_setup_tasks = []

    # Corrected import path for modules within the 'sensor' package
    # The __name__ will be 'custom_components.meraki_ha.sensor'
    # So, f"{__name__}{module_name}" would be e.g. 'custom_components.meraki_ha.sensor.meraki_ssid_psk'
    # which is correct for __import__.

    for module_name_suffix in SENSOR_MODULES:
        full_module_path = f"custom_components.meraki_ha.sensor{module_name_suffix}"
        try:
            # Dynamically import the module
            # Use functools.partial to correctly pass arguments to __import__
            module_importer = partial(__import__, full_module_path, fromlist=["async_setup_entry"])
            module = await hass.async_add_import_executor_job(module_importer)

            if hasattr(module, "async_setup_entry"):
                _LOGGER.debug(f"Calling async_setup_entry for sensor module: {full_module_path}")
                # Schedule the setup entry task
                task = module.async_setup_entry(hass, config_entry, async_add_entities)
                platform_setup_tasks.append(task)
            else:
                _LOGGER.warning(
                    f"Sensor module {full_module_path} does not have an async_setup_entry function. "
                    "Its sensors may not be loaded."
                )
        except ImportError as e:
            # This is expected if a module in SENSOR_MODULES doesn't exist.
            _LOGGER.debug(f"Could not import sensor module {full_module_path}: {e}. This may be expected if the file doesn't exist.")
        except Exception as e:
            _LOGGER.error(f"Error setting up sensor module {full_module_path}: {e}", exc_info=True)

    if platform_setup_tasks:
        await asyncio.gather(*platform_setup_tasks)
        _LOGGER.info(f"Finished asynchronous setup for {len(platform_setup_tasks)} Meraki sensor modules.")
    else:
        _LOGGER.warning("No Meraki sensor modules were successfully processed for setup.")

    return True # Return True to indicate platform setup attempt was made.
```
