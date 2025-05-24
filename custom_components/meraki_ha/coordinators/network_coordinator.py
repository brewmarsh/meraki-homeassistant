"""Network data coordinator for the Meraki Home Assistant integration.

This module defines the `MerakiNetworkCoordinator`, which is responsible for
fetching details about all networks within a Meraki organization. It also
registers each Meraki network as a "device" in the Home Assistant device
registry to act as a parent for actual Meraki hardware devices associated
with that network.
"""
import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional # Added List, Optional

from homeassistant.config_entries import ConfigEntry # For self.config_entry type
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..const import DOMAIN # For device identifiers and logger naming
# Local import for MerakiApiDataFetcher to avoid circular dependencies at module load.
# Ensure MerakiApiDataFetcher and MerakiApiError are defined in api_data_fetcher.py.
from .api_data_fetcher import MerakiApiDataFetcher, MerakiApiError

_LOGGER = logging.getLogger(__name__)

# Define MERAKI_API_URL if it's not available from const.py or another central place
MERAKI_API_BASE_URL = "https://api.meraki.com/api/v1"


class MerakiNetworkCoordinator(
    DataUpdateCoordinator[Dict[str, List[Dict[str, Any]]]]
):
    """Coordinator to fetch and manage Meraki network data.

    This coordinator retrieves information about all networks in the specified
    Meraki organization. For each network, it creates a corresponding "device"
    entry in the Home Assistant device registry. This allows physical Meraki
    devices to be associated with their respective networks in Home Assistant.
    """

    # config_entry: ConfigEntry # Added to hold the config entry instance

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        device_name_format: str,
        # config_entry: ConfigEntry, # Pass the ConfigEntry
    ) -> None:
        """Initialize the Meraki network coordinator.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            org_id: The Meraki Organization ID.
            scan_interval: The interval for updating network data.
            device_name_format: The format for naming network "devices"
                in the registry (e.g., "prefix", "suffix", "omitted").
            # config_entry: The config entry associated with this coordinator.
        """
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} Networks ({org_id})", # More specific name
            update_interval=scan_interval,
        )
        self.api_key: str = api_key
        self.org_id: str = org_id
        self.device_name_format: str = device_name_format
        # To use self.config_entry in _async_update_data, it must be stored.
        # It's typically passed to DataUpdateCoordinator's constructor or set if needed.
        # For device_registry.async_get_or_create, config_entry_id is on self.
        # self.config_entry is automatically set by Home Assistant when the coordinator
        # is linked to a config entry (e.g. via hass.data).
        # If direct access to the ConfigEntry object is needed earlier, it must be passed.

        # Ensure self.data is initialized as per DataUpdateCoordinator's generic type
        self.data: Dict[str, List[Dict[str, Any]]] = {"networks": []}


    async def _async_update_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch and process network data from the Meraki API.

        Retrieves all networks for the configured organization and registers
        each as a device in the Home Assistant device registry.

        Returns:
            A dictionary containing a list of raw network data from the API,
            e.g., `{"networks": [...]}`.

        Raises:
            UpdateFailed: If there's a critical error fetching network data
                or interacting with the device registry.
        """
        device_registry = dr.async_get(self.hass)
        api_fetcher = MerakiApiDataFetcher(api_key=self.api_key, org_id=self.org_id)

        try:
            _LOGGER.debug(
                "Fetching all networks for organization ID: %s", self.org_id
            )
            # The original code had a typo in the URL construction (missing /organizations/)
            url = f"{MERAKI_API_BASE_URL}/organizations/{self.org_id}/networks"
            networks_raw: Optional[
                List[Dict[str, Any]]
            ] = await api_fetcher._fetch_data(url)

            if networks_raw is None:
                # This case might occur if _fetch_data returns None on error
                _LOGGER.warning(
                    "Failed to retrieve Meraki networks for org %s (API fetcher returned None).",
                    self.org_id,
                )
                # Keep self.data as is or clear it, returning current state
                # to avoid entities erroring if they expect data.
                # Or raise UpdateFailed. Original code raised UpdateFailed.
                raise UpdateFailed(
                    f"Failed to retrieve Meraki networks for org {self.org_id} (fetcher returned None)."
                )

            if not networks_raw: # Handles empty list
                _LOGGER.info(
                    "No Meraki networks found for organization %s.", self.org_id
                )
                self.data = {"networks": []} # Update data to empty list
                return self.data

            _LOGGER.debug(
                "Successfully retrieved %d networks for org %s.",
                len(networks_raw),
                self.org_id,
            )

            for network_data in networks_raw:
                network_id = network_data.get("id")
                network_name = network_data.get("name", "Unnamed Network")

                if not network_id:
                    _LOGGER.warning(
                        "Found a network without an ID, skipping registration: %s",
                        network_data,
                    )
                    continue

                # Determine the device name based on the specified format
                device_name = network_name # Default
                if self.device_name_format == "prefix":
                    device_name = f"[Network] {network_name}"
                elif self.device_name_format == "suffix":
                    device_name = f"{network_name} [Network]"

                # Register the network as a device in Home Assistant
                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, network_id)},
                    manufacturer="Cisco Meraki", # Standardized manufacturer
                    name=str(device_name), # Ensure name is a string
                    model="Network", # Generic model for these network "devices"
                    # entry_type=dr.DeviceEntryType.SERVICE, # Optional: classify
                )
                _LOGGER.debug(
                    "Registered/Updated Meraki Network as HA device: %s (ID: %s)",
                    device_name,
                    network_id,
                )
            self.data = {"networks": networks_raw}
            return self.data

        except MerakiApiError as e:
            _LOGGER.error(
                "Meraki API error while updating network data for org %s: %s",
                self.org_id,
                e,
            )
            raise UpdateFailed(
                f"Meraki API error updating network data: {e}"
            ) from e
        except Exception as e: # pylint: disable=broad-except
            _LOGGER.exception(
                "Unexpected error updating network data for org %s: %s", self.org_id, e
            )
            raise UpdateFailed(
                f"Unexpected error updating network data: {e}"
            ) from e
