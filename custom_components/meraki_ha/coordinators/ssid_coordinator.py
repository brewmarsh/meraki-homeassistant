"""SSID data coordinator for the Meraki Home Assistant integration.

This module defines `MerakiSsidCoordinator`, responsible for fetching SSID
(Service Set Identifier - wireless network name) data for all relevant Meraki
networks. It registers each SSID as a device in the Home Assistant device
registry, linking it to its parent Meraki network device.
"""
import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional # Added Optional

from homeassistant.config_entries import ConfigEntry # For self.config_entry type
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..const import DOMAIN # For device identifiers and logger naming
# Local import for MerakiApiDataFetcher to avoid circular dependencies at module load.
from .api_data_fetcher import MerakiApiDataFetcher, MerakiApiError

_LOGGER = logging.getLogger(__name__)

# Define MERAKI_API_URL if it's not available from const.py or another central place
MERAKI_API_BASE_URL = "https://api.meraki.com/api/v1"


class MerakiSsidCoordinator(DataUpdateCoordinator[Dict[str, List[Dict[str, Any]]]]):
    """Coordinator to fetch and manage Meraki SSID data.

    This coordinator iterates through networks known to have wireless capabilities,
    fetches their SSIDs, and registers each SSID as a distinct "device" in the
    Home Assistant device registry. These SSID devices are parented by their
    respective Meraki network "devices".
    """

    # config_entry: ConfigEntry # To hold the config entry instance

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        # device_name_format: str, # This was in __init__ but not used in this class directly
                                 # It's used by the caller (base_coordinator) to format names.
                                 # However, the _async_update_data uses it. Keeping for now.
        device_name_format: str, # Make sure this is passed if used
    ) -> None:
        """Initialize the Meraki SSID coordinator.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            org_id: The Meraki Organization ID.
            scan_interval: The interval for updating SSID data.
            device_name_format: The format for naming SSID "devices"
                in the registry (e.g., "prefix", "suffix", "network_prefix", "omitted").
        """
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} SSIDs ({org_id})", # More specific name
            update_interval=scan_interval,
        )
        self.api_key: str = api_key
        self.org_id: str = org_id
        # List of network data dicts, expected to be populated by another coordinator
        # or a setup process before _async_update_data is called.
        self.networks: List[Dict[str, Any]] = []
        self.device_name_format: str = device_name_format

        # Ensure self.data is initialized as per DataUpdateCoordinator's generic type
        self.data: Dict[str, List[Dict[str, Any]]] = {"ssids": []}


    async def _async_get_ssids(
        self, network_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all SSIDs for a specific Meraki network.

        Args:
            network_id: The ID of the Meraki network for which to fetch SSIDs.

        Returns:
            A list of dictionaries, where each dictionary represents an SSID.
            Returns an empty list if the network has no wireless SSIDs (e.g., a
            camera network) or if an error occurs that results in no data.
            Returns None if a critical API error occurs preventing data retrieval.

        Raises:
            UpdateFailed: If a critical error occurs during API communication,
                such as invalid API key or unrecoverable connection issues.
        """
        url = f"{MERAKI_API_BASE_URL}/networks/{network_id}/wireless/ssids"
        _LOGGER.debug("Fetching SSIDs for network ID: %s from %s", network_id, url)

        # Initialize api_fetcher here as it's specific to this request context
        # Passing 'self' as ssid_coordinator to api_fetcher if it needs context from this coordinator.
        api_fetcher = MerakiApiDataFetcher(
            self.api_key, self.org_id, network_coordinator=None, ssid_coordinator=self
        )

        try:
            response: Optional[
                List[Dict[str, Any]]
            ] = await api_fetcher._fetch_data(url)

            if response is None:
                # _fetch_data might return None on certain errors (e.g. non-JSON response, or specific HTTP codes if handled that way)
                _LOGGER.warning(
                    "API returned no data (None) for SSIDs in network %s. This might be normal if the network has no wireless capabilities or no SSIDs.",
                    network_id,
                )
                return [] # Treat as no SSIDs for this network

            # Meraki API sometimes returns errors within a 200 OK response, e.g. {"errors": ["..."]}
            if isinstance(response, dict) and "errors" in response:
                error_message = response["errors"]
                _LOGGER.error(
                    "Meraki API error while fetching SSIDs for network %s: %s",
                    network_id,
                    error_message,
                )
                # Depending on how critical this is, you might return [] or raise UpdateFailed
                # If one network failing to provide SSIDs shouldn't stop all, return [].
                return []

            if not isinstance(response, list):
                _LOGGER.warning(
                    "Unexpected API response format (expected list, got %s) for SSIDs in network %s: %s",
                    type(response).__name__,
                    network_id,
                    str(response)[:200], # Log snippet of response
                )
                return []

            _LOGGER.debug(
                "Successfully fetched %d SSIDs for network %s.",
                len(response),
                network_id,
            )
            return response
        except MerakiApiError as e: # Catch specific API errors from _fetch_data
            _LOGGER.error(
                "Meraki API error fetching SSIDs for network %s: %s", network_id, e
            )
            # If one network's SSIDs failing shouldn't halt everything, return empty list.
            # If it's critical (e.g. auth error), UpdateFailed should be raised by _fetch_data.
            # For now, assume non-critical for individual network SSID fetch unless it's an UpdateFailed type.
            if isinstance(e, UpdateFailed): # e.g. ConfigEntryAuthFailed is a subclass
                 raise
            return [] # Treat other API errors as "no SSIDs for this network"
        except Exception as err: # Catch any other unexpected error
            _LOGGER.exception(
                "Unexpected error fetching SSIDs for network %s: %s", network_id, err
            )
            # For truly unexpected errors, re-raise as UpdateFailed if it's critical for the coordinator.
            # However, if this is part of a loop, you might want to allow other networks to proceed.
            # The original code raised UpdateFailed here.
            raise UpdateFailed(
                f"Unexpected error fetching SSIDs for network {network_id}: {err}"
            ) from err


    async def _async_update_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch all SSIDs for relevant networks and register them as devices.

        This method iterates through networks determined to have wireless capabilities
        (based on `productTypes`), fetches their SSIDs, and registers each SSID
        as a device in the Home Assistant device registry.

        Returns:
            A dictionary containing a list of all processed SSID data,
            e.g., `{"ssids": [...]}`.

        Raises:
            UpdateFailed: If no network data is available (self.networks is empty)
                or if a critical error occurs during SSID fetching or device registration.
        """
        _LOGGER.debug(
            "Starting SSID data update. Known networks: %d", len(self.networks)
        )

        if not self.networks:
            _LOGGER.warning(
                "Network list is empty in SSID coordinator. Cannot fetch SSIDs. "
                "Ensure MerakiNetworkCoordinator runs first or network data is populated."
            )
            # Return current (likely empty) data to avoid breaking state if minor issue,
            # or raise UpdateFailed if this is considered a critical failure.
            # Original code raised UpdateFailed.
            raise UpdateFailed("Network data not available to MerakiSsidCoordinator.")

        all_ssids_processed: List[Dict[str, Any]] = []
        device_registry = dr.async_get(self.hass)

        for network in self.networks:
            network_id = network.get("id")
            network_name = network.get("name", "Unnamed Network")
            product_types: List[str] = network.get("productTypes", [])

            if not network_id:
                _LOGGER.warning("Skipping network with no ID: %s", network)
                continue

            # Only attempt to fetch SSIDs for networks that support wireless
            if "wireless" not in product_types:
                _LOGGER.debug(
                    "Skipping SSID fetch for network %s (%s) as it does not support wireless product types (%s).",
                    network_name,
                    network_id,
                    product_types,
                )
                continue

            _LOGGER.debug(
                "Processing network %s (%s) for SSIDs.", network_name, network_id
            )
            try:
                network_ssids_raw: Optional[
                    List[Dict[str, Any]]
                ] = await self._async_get_ssids(network_id)
            except UpdateFailed as e:
                # If _async_get_ssids raises UpdateFailed (e.g. auth error), propagate it
                _LOGGER.error("Failed to get SSIDs for network %s due to UpdateFailed: %s", network_id, e)
                raise # Re-raise to stop the entire update if critical
            except Exception as e: # Should be caught by _async_get_ssids, but as a safeguard
                _LOGGER.exception("Unexpected error from _async_get_ssids for network %s: %s", network_id, e)
                continue # Skip this network's SSIDs

            if network_ssids_raw:
                for ssid_data in network_ssids_raw:
                    ssid_number = ssid_data.get("number")
                    ssid_name = ssid_data.get("name", f"SSID {ssid_number}")
                    # Default to True if 'enabled' key is missing, though API usually provides it.
                    ssid_enabled = ssid_data.get("enabled", True)

                    if ssid_number is None:
                        _LOGGER.warning(
                            "SSID found without a number in network %s, skipping: %s",
                            network_id,
                            ssid_data,
                        )
                        continue

                    # Determine device name based on format
                    formatted_ssid_name = ssid_name # Default
                    if self.device_name_format == "prefix":
                        formatted_ssid_name = f"[SSID] {ssid_name}"
                    elif self.device_name_format == "suffix":
                        formatted_ssid_name = f"{ssid_name} [SSID]"
                    elif self.device_name_format == "network_prefix":
                        formatted_ssid_name = f"{network_name} - {ssid_name} [SSID]"
                    # If "omitted", name remains ssid_name

                    # Register SSID as a device in Home Assistant, linked to the network "device"
                    ha_device = device_registry.async_get_or_create(
                        config_entry_id=self.config_entry.entry_id,
                        identifiers={(DOMAIN, f"{network_id}_{ssid_number}")},
                        manufacturer="Cisco Meraki",
                        name=str(formatted_ssid_name), # Ensure name is string
                        model="SSID", # Generic model for SSID "devices"
                        via_device=(DOMAIN, network_id), # Link to parent network device
                        # sw_version=None, # SSIDs don't have firmware
                        # entry_type=dr.DeviceEntryType.SERVICE, # Optional
                    )
                    # Enrich SSID data with network context and HA device ID
                    processed_ssid_data = {
                        **ssid_data, # All original SSID data
                        "network_id": network_id,
                        "network_name": network_name, # For convenience
                        "device_id": ha_device.id, # HA device ID for this SSID
                        "enabled": ssid_enabled, # Ensure this is captured
                    }
                    all_ssids_processed.append(processed_ssid_data)
                    _LOGGER.debug(
                        "Registered/Updated Meraki SSID as HA device: %s (Identifier: %s_%s), Enabled: %s",
                        formatted_ssid_name,
                        network_id,
                        ssid_number,
                        ssid_enabled,
                    )
        self.data = {"ssids": all_ssids_processed}
        _LOGGER.info(
            "SSID update complete. Total SSIDs processed: %d",
            len(all_ssids_processed),
        )
        return self.data
