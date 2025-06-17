# custom_components/meraki_ha/text/meraki_ssid_name.py
"""Text entity for renaming Meraki SSIDs."""

import logging
from typing import Any, Dict # Optional removed

from homeassistant.components.text import TextEntity, TextMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError # Added import
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN, DATA_CLIENT
from ..meraki_api import MerakiAPIClient
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    _LOGGER.debug("meraki_ssid_name.py: Setting up Meraki SSID name text entities.")
    try:
        # Attempt to retrieve coordinators and client
        try:
            ssid_coordinator: SSIDDeviceCoordinator = hass.data[DOMAIN][config_entry.entry_id][
                "coordinators"
            ]["ssid_devices"]
            meraki_client: MerakiAPIClient = hass.data[DOMAIN][config_entry.entry_id][
                DATA_CLIENT
            ]
        except KeyError as e:
            _LOGGER.error(
                "meraki_ssid_name.py: Failed to retrieve required data from hass.data (KeyError: %s). Cannot set up text entities.", e,
                exc_info=True
            )
            return False

        if not ssid_coordinator or not ssid_coordinator.data: # Added check for ssid_coordinator itself
            _LOGGER.warning("meraki_ssid_name.py: SSID Coordinator not available or has no data, skipping text entity setup but platform reports failure.")
            return False # Explicitly return False if critical data is missing

        text_entities = []
        # Loop to create entities, also wrapped in try/except
        try:
            for ssid_unique_id, ssid_data in ssid_coordinator.data.items():
                # Add a try-except for individual entity creation if needed, though often one bad apple might mean stopping all for the platform
                if not isinstance(ssid_data, dict): # Basic check for data sanity
                    _LOGGER.warning("meraki_ssid_name.py: ssid_data for id %s is not a dictionary, skipping.", ssid_unique_id)
                    continue
                text_entities.append(
                    MerakiSSIDNameTextEntity(
                        ssid_coordinator, meraki_client, config_entry, ssid_unique_id, ssid_data
                    )
                )
        except Exception as e_entity_creation: # Catch any error during entity list creation
            _LOGGER.error("meraki_ssid_name.py: Error creating list of text entities: %s", e_entity_creation, exc_info=True)
            return False

        if text_entities: # Only add if list is not empty
            async_add_entities(text_entities, update_before_add=True)
            _LOGGER.debug("meraki_ssid_name.py: Added %d Meraki SSID name text entities.", len(text_entities))
        else:
            _LOGGER.debug("meraki_ssid_name.py: No text entities were created or added.")
            # If no entities are added, it's still a successful setup of the platform itself (it did its job, found nothing to add).

        _LOGGER.debug("meraki_ssid_name.py: Finished setting up Meraki SSID name text entities, returning True.")
        return True

    except Exception as e: # Catch-all for the entire function
        _LOGGER.error("meraki_ssid_name.py: Unexpected error during text entity setup: %s", e, exc_info=True)
        return False


class MerakiSSIDNameTextEntity(CoordinatorEntity[SSIDDeviceCoordinator], TextEntity):
    """Representation of a Meraki SSID name as a text entity for renaming."""

    _attr_mode = TextMode.TEXT  # Can be 'text' or 'password'

    def __init__(
        self,
        coordinator: SSIDDeviceCoordinator,
        meraki_client: MerakiAPIClient,
        config_entry: ConfigEntry,
        ssid_unique_id: str,  # HA device unique_id for the SSID
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki SSID name text entity."""
        super().__init__(coordinator)
        self._meraki_client = meraki_client
        self._config_entry = config_entry
        self._ssid_unique_id = ssid_unique_id

        self._network_id = ssid_data.get("networkId")
        self._ssid_number = ssid_data.get("number")
        initial_name = ssid_data.get("name", f"SSID {self._ssid_number}")

        self._attr_unique_id = f"{self._ssid_unique_id}_name_text"
        self._attr_name = f"{initial_name} Name"  # e.g., "Guest WiFi Name"
        self._attr_native_value = initial_name  # Set initial state

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information to link this entity to the SSID device."""
        return {
            "identifiers": {(DOMAIN, self._ssid_unique_id)},
        }

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # First, check coordinator readiness (includes self.coordinator.data is not None)
        if not super().available:
            return False
        # Then, check if this specific SSID's data key exists in the coordinator's data
        # self.coordinator.data is Dict[unique_ssid_id, ssid_data_dict]
        return self._ssid_unique_id in self.coordinator.data

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        current_ssid_data = self.coordinator.data.get(self._ssid_unique_id)
        if current_ssid_data:
            new_name = current_ssid_data.get("name", f"SSID {self._ssid_number}")
            self._attr_native_value = new_name
            self._attr_name = (
                f"{new_name} Name"  # Update entity name if SSID name changes
            )
        else:
            # Data for this SSID not found, log warning, state remains unchanged or becomes unavailable
            _LOGGER.warning(
                f"Could not find data for SSID {self._ssid_unique_id} in coordinator for text entity."
            )
            # Optionally set to None or some indicator of unavailability
            # self._attr_native_value = None
        self.async_write_ha_state()

    async def async_set_value(self, value: str) -> None:
        """Change the SSID name via the Meraki API."""
        if not self._network_id or self._ssid_number is None:
            _LOGGER.error(
                f"Cannot set SSID name for {self.name}: Missing networkId or SSID number."
            )
            return

        _LOGGER.debug(
            f"Setting SSID name for {self._network_id}/{self._ssid_number} to: {value}"
        )

        try:
            await self._meraki_client.wireless.updateNetworkWirelessSsid(
                networkId=self._network_id,
                number=self._ssid_number,
                name=value,  # The new name for the SSID
            )
            # Update the internal state optimistically for quicker UI response
            self._attr_native_value = value
            self._attr_name = f"{value} Name"
            self.async_write_ha_state()

            # Request a coordinator refresh to confirm the change from the API
            await self.coordinator.async_request_refresh()
        except Exception as e:
            _LOGGER.error(f"Failed to set SSID name for {self.name} to '{value}': {e}")
            raise HomeAssistantError(f"Failed to update SSID name for {self.name} to '{value}': {e}") from e
            # Optionally, force a refresh to revert optimistic update.
            # For now, we rely on the next scheduled or requested refresh.
