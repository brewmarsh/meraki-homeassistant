"""Provides the MerakiSsidCoordinator for the Meraki Home Assistant integration.

This module defines `MerakiSsidCoordinator`, a Home Assistant
`DataUpdateCoordinator` responsible for fetching Meraki SSID (Wireless Network)
data from the API. It also registers corresponding "SSID" devices in the
Home Assistant device registry, linking them to their parent Meraki network device.
"""

import logging
from datetime import timedelta
from typing import Any, Dict, List

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers import device_registry as dr
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiSsidCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinates fetching and processing of Meraki SSID data.

    This coordinator retrieves SSID configurations for each wireless-capable
    network in the Meraki organization. For each SSID, it creates a
    corresponding "device" entry in the Home Assistant device registry,
    linking it to the parent network "device" (created by `MerakiNetworkCoordinator`).

    Attributes:
        api_key (str): The Meraki API key.
        org_id (str): The Meraki organization ID.
        networks (List[Dict[str, Any]]): A list of network data dictionaries,
            typically populated by another coordinator or process before this
            coordinator's update cycle. This coordinator relies on this list
            to know which networks to query for SSIDs.
        device_name_format (str): User-selected format for device names,
            applied to the SSID "devices".
        data (Dict[str, Any]): Stores the fetched and processed SSID data,
            structured as {"ssids": [...]}.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        device_name_format: str,
    ) -> None:
        """Initializes the MerakiSsidCoordinator.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            api_key (str): The Meraki API key.
            org_id (str): The Meraki organization ID. (Note: org_id is stored
                but not directly used in current methods, as API calls are
                network-specific using `self.networks`).
            scan_interval (timedelta): The interval for periodic data updates.
            device_name_format (str): The format string for naming SSID "devices".
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki SSIDs",  # Coordinator name for logging
            update_interval=scan_interval,
        )
        self.api_key = api_key
        self.org_id = org_id  # Stored, but network_id from self.networks is used for API calls
        self.networks: List[Dict[str, Any]] = []  # Initialize as empty list
        self.device_name_format = device_name_format
        self.data: Dict[str, Any] = {"ssids": []}  # Initialize data structure

    async def _async_get_ssids_for_network(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """Fetches all SSIDs for a specific Meraki network ID.

        Args:
            network_id (str): The ID of the Meraki network.

        Returns:
            List[Dict[str, Any]]: A list of SSID dictionaries from the API.
                Returns an empty list if the API call fails or no SSIDs are found.

        Raises:
            UpdateFailed: If a non-recoverable error occurs during API fetch,
                though current implementation aims to return empty list on error.
        """
        ssids_url = (
            f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids"
        )
        _LOGGER.debug("Fetching SSIDs for network ID %s from URL: %s", network_id, ssids_url)
        try:
            # Local import to avoid circular dependencies.
            from .api_data_fetcher import MerakiApiDataFetcher

            # `self` is passed as ssid_coordinator, though not directly used by _fetch_data.
            api_fetcher = MerakiApiDataFetcher(self.api_key, None, None, self)

            ssids_raw = await api_fetcher._fetch_data(ssids_url)

            if ssids_raw is None or not isinstance(ssids_raw, list):
                _LOGGER.warning(
                    "API did not return a valid list of SSIDs for network %s. Response: %s",
                    network_id,
                    ssids_raw,
                )
                return []  # Return empty list on unexpected response type or None
            _LOGGER.debug(
                "Successfully fetched %d SSIDs for network %s.", len(ssids_raw), network_id
            )
            return ssids_raw
        except Exception as err:
            # Catch broad exceptions from _fetch_data to prevent coordinator failure.
            _LOGGER.error("Error fetching SSIDs for network %s: %s", network_id, err)
            # Depending on strictness, could raise UpdateFailed.
            # For resilience, returning empty list for this network's SSIDs.
            return []


    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetches Meraki SSID data for all relevant networks and registers HA devices.

        This method iterates through the `self.networks` list (expected to be
        populated beforehand). For each network that supports wireless, it fetches
        SSID configurations and creates a corresponding "device" in the Home
        Assistant device registry for each SSID.

        Returns:
            Dict[str, Any]: A dictionary with an "ssids" key, containing a list
                of processed SSID data, including their HA device ID.

        Raises:
            UpdateFailed: If `self.networks` is not populated, or if an
                unexpected error occurs during the overall update process.
        """
        _LOGGER.debug("SSID Coordinator: Starting update. Known networks: %s", self.networks)

        if not self.networks:
            _LOGGER.error(
                "Networks list is not populated in MerakiSsidCoordinator. "
                "Ensure it's set before calling _async_update_data. Cannot fetch SSIDs."
            )
            # This indicates a potential logic error in how coordinators are chained or data is passed.
            raise UpdateFailed("Networks data not available to SSID coordinator.")

        all_processed_ssids: List[Dict[str, Any]] = []
        device_registry = dr.async_get(self.hass)

        for network in self.networks:
            if not isinstance(network, dict):
                _LOGGER.warning("Skipping non-dictionary item in networks list: %s", network)
                continue

            network_id = network.get("id")
            network_name = network.get("name", "Unknown Network") # Default name
            product_types = network.get("productTypes", [])

            if not network_id:
                _LOGGER.warning("Skipping network with missing ID: %s", network)
                continue

            # Only attempt to fetch SSIDs for networks that support wireless.
            if "wireless" not in product_types:
                _LOGGER.debug(
                    "Skipping network %s (%s) as it does not support wireless product types (%s).",
                    network_id,
                    network_name,
                    product_types,
                )
                continue

            _LOGGER.debug(
                "Processing wireless-capable network: %s (%s)", network_id, network_name
            )
            network_ssids_raw = await self._async_get_ssids_for_network(network_id)

            if network_ssids_raw: # If list is not empty
                for ssid_raw_details in network_ssids_raw:
                    if not isinstance(ssid_raw_details, dict):
                        _LOGGER.warning("Skipping non-dictionary SSID item: %s for network %s", ssid_raw_details, network_id)
                        continue

                    ssid_number = ssid_raw_details.get("number") # SSID number (0-14)
                    ssid_name = ssid_raw_details.get("name")
                    # Default to True if 'enabled' key is missing, though API usually includes it.
                    ssid_enabled = ssid_raw_details.get("enabled", True)

                    if ssid_number is None or ssid_name is None:
                        _LOGGER.warning(
                            "SSID entry found with missing number or name for network %s: %s. Skipping.",
                            network_id,
                            ssid_raw_details,
                        )
                        continue

                    # Format the Home Assistant device name for the SSID.
                    ha_device_name = ssid_name # Default
                    if self.device_name_format == "prefix":
                        ha_device_name = f"[SSID] {ssid_name}"
                    elif self.device_name_format == "suffix":
                        ha_device_name = f"{ssid_name} [SSID]"
                    elif self.device_name_format == "network_prefix":
                        ha_device_name = f"{network_name} - {ssid_name} [SSID]"

                    _LOGGER.debug(
                        "Determined HA device name for SSID '%s' (Number: %s) in network %s: %s",
                        ssid_name,
                        ssid_number,
                        network_name,
                        ha_device_name,
                    )

                    # Create or update the "device" entry for the SSID in Home Assistant.
                    # This SSID device is linked to its parent Meraki Network device.
                    ha_ssid_device_entry = device_registry.async_get_or_create(
                        config_entry_id=self.config_entry.entry_id,
                        identifiers={(DOMAIN, f"{network_id}_{ssid_number}")}, # Unique ID for SSID
                        manufacturer="Cisco Meraki",
                        name=ha_device_name,
                        model="SSID", # Generic model for these SSID representations
                        via_device=(DOMAIN, network_id), # Link to the parent network device
                    )

                    # Store processed SSID data along with its network context and HA device ID.
                    processed_ssid_info = {
                        **ssid_raw_details, # Include all original SSID data
                        "network_id": network_id,
                        "device_id": ha_ssid_device_entry.id, # HA's internal device ID for this SSID
                        "enabled": ssid_enabled, # Ensure 'enabled' status is part of stored data
                    }
                    all_processed_ssids.append(processed_ssid_info)

                    _LOGGER.debug(
                        "Ensured HA device entry for SSID: %s (Network: %s, SSID No: %s), Enabled: %s",
                        ha_device_name,
                        network_name,
                        ssid_number,
                        ssid_enabled,
                    )

        # Update the coordinator's data.
        self.data = {"ssids": all_processed_ssids}
        _LOGGER.info(
            "SSID Coordinator update complete. Total SSIDs processed: %d",
            len(all_processed_ssids),
        )
        return self.data
        # Error handling for the overall update process:
        # UpdateFailed exceptions from _async_get_ssids_for_network are currently handled by returning [].
        # If a more critical failure needs to stop the entire coordinator,
        # those specific exceptions should be re-raised or new UpdateFailed thrown here.
        # The current broad try/except in the original code is removed to allow more specific error
        # propagation if needed from helper methods, or rely on HA's default DataUpdateCoordinator error handling.
