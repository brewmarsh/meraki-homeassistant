"""Provides the MerakiNetworkCoordinator for the Meraki Home Assistant integration.

This module defines `MerakiNetworkCoordinator`, a Home Assistant
`DataUpdateCoordinator` responsible for fetching Meraki network data from the
API and registering corresponding "network" devices in the Home Assistant
device registry.
"""

import logging
from typing import Any, Dict
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinates fetching and processing of Meraki network data.

    This coordinator fetches a list of all networks within the specified
    Meraki organization. For each network, it creates a corresponding
    "device" entry in the Home Assistant device registry. This allows
    entities to be associated with a network, even if there isn't a
    physical Meraki device directly representing the network itself.

    Attributes:
        api_key (str): The Meraki API key.
        org_id (str): The Meraki organization ID.
        device_name_format (str): User-selected format for device names
            (applied to the network "devices" created by this coordinator).
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        device_name_format: str,
    ) -> None:
        """Initializes the MerakiNetworkCoordinator.

        Args:
            hass (HomeAssistant): The Home Assistant instance.
            api_key (str): The Meraki API key for authentication.
            org_id (str): The Meraki organization ID.
            scan_interval (timedelta): The interval for periodic data updates.
            device_name_format (str): The format string for naming the
                network "devices" in Home Assistant (e.g., "prefix", "suffix").
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Meraki Networks",  # Coordinator name for logging
            update_interval=scan_interval,
        )
        self.api_key = api_key
        self.org_id = org_id
        self.device_name_format = device_name_format

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetches Meraki network data and registers corresponding HA devices.

        This method retrieves all networks for the configured organization,
        then iterates through them, creating a "device" in the Home Assistant
        device registry for each Meraki network. This allows network-level
        entities or information to be associated with a tangible representation
        in HA.

        Returns:
            Dict[str, Any]: A dictionary with a "networks" key, containing the
                list of raw network data from the API. Returns an empty
                dictionary if no networks are found or if a critical error occurs.

        Raises:
            UpdateFailed: If there's a failure in fetching the network data
                from the Meraki API or an unexpected error during processing.
        """
        device_registry = dr.async_get(self.hass)
        try:
            # Local import to avoid circular dependencies at module load time.
            from .api_data_fetcher import MerakiApiDataFetcher

            # Initialize API fetcher. `self` is passed as network_coordinator,
            # though MerakiApiDataFetcher doesn't directly use it in _fetch_data.
            api_fetcher = MerakiApiDataFetcher(self.api_key, None, self, None)

            # Construct the URL for fetching networks in the organization.
            networks_url = (
                f"https://api.meraki.com/api/v1/organizations/{self.org_id}/networks"
            )

            _LOGGER.debug("Making API call to get networks: %s", networks_url)
            networks_raw = await api_fetcher._fetch_data(networks_url)

            # Validate the fetched data.
            if networks_raw is None:
                # This case might occur if _fetch_data returns None on certain errors
                # (e.g. 404 for organization, handled in MerakiApiDataFetcher.async_get_networks)
                _LOGGER.warning(
                    "Failed to retrieve Meraki networks for organization %s (API returned None).",
                    self.org_id
                )
                # UpdateFailed could be raised here if networks are critical.
                # Current logic from original code implies returning {} or empty data.
                return {"networks": []} # Return empty list under "networks" key

            if not isinstance(networks_raw, list) or not networks_raw:
                _LOGGER.warning(
                    "No Meraki networks found for organization %s, or data format is unexpected. API response: %s",
                    self.org_id,
                    networks_raw if not isinstance(networks_raw, list) else "empty list"
                )
                return {"networks": []} # Consistent return type

            _LOGGER.info("Successfully retrieved %d networks for organization %s.", len(networks_raw), self.org_id)

            # Process each network and register it as a device in Home Assistant.
            for network_details in networks_raw:
                if not isinstance(network_details, dict):
                    _LOGGER.warning("Skipping non-dictionary item in networks list: %s", network_details)
                    continue

                network_id = network_details.get("id")
                network_name = network_details.get("name")

                if not network_id or not network_name:
                    _LOGGER.warning(
                        "Network entry found with missing ID or name: %s. Skipping.",
                        network_details,
                    )
                    continue

                # Format the device name based on user preference.
                # This "device" represents the Meraki Network itself.
                ha_device_name = network_name  # Default name
                if self.device_name_format == "prefix":
                    ha_device_name = f"[Network] {network_name}"
                elif self.device_name_format == "suffix":
                    ha_device_name = f"{network_name} [Network]"
                _LOGGER.debug(
                    "Determined Home Assistant device name for network %s (%s): %s",
                    network_id,
                    network_name,
                    ha_device_name,
                )

                # Create or update the device entry in Home Assistant's device registry.
                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, network_id)},  # Unique identifier
                    manufacturer="Cisco Meraki",
                    name=ha_device_name,
                    model="Network",  # Generic model type for these network devices
                    # Potentially add more info like via_device if applicable,
                    # or a configuration_url to the Meraki dashboard for this network.
                )
                _LOGGER.debug(
                    "Ensured Home Assistant device entry for Meraki Network: %s (%s)",
                    ha_device_name,
                    network_id,
                )

            # Return the raw network data for potential use by other components/entities.
            return {"networks": networks_raw}

        except aiohttp.ClientResponseError as err:
            _LOGGER.error("API request failed with status %s: %s", err.status, err.message)
            raise UpdateFailed(f"API request failed: {err.message} (Status: {err.status})") from err
        except aiohttp.ClientError as err:
            _LOGGER.error("API client error: %s", err)
            raise UpdateFailed(f"API client error: {err}") from err
        except Exception as e:
            # Catch any other unexpected errors.
            _LOGGER.exception("Unexpected error updating Meraki network data: %s", e)
            raise UpdateFailed(f"Unexpected error updating network data: {e}") from e
