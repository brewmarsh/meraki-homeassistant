# /config/custom_components/meraki_ha/meraki_api/wireless.py
import logging
from typing import Any, Dict, List
from ._api_client import MerakiAPIClient
from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


class MerakiWirelessAPI:
    """Meraki wireless API functions."""

    def __init__(self, client: MerakiAPIClient):
        """Initialize the Meraki Wireless API.

        Args:
            client: An instance of the MerakiAPIClient.
        """
        self._client = client

    async def async_get_device_wireless_radio_settings(
        self, serial: str
    ) -> Dict[str, Any]:
        """Fetch wireless radio settings for a Meraki MR device.

        Args:
            serial: Serial number of the Meraki MR access point.

        Returns:
            A dictionary containing the wireless radio settings for the device.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/wireless/radio/settings"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            return await self._client._async_meraki_request("GET", url, headers)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error fetching wireless radio settings for device '{serial}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching wireless radio settings for device '{serial}': {e}"
            ) from e

    async def async_get_network_wireless_rf_profile(
        self, network_id: str, rf_profile_id: str
    ) -> Dict[str, Any]:
        """Fetch wireless RF profile settings for a Meraki network.

        Args:
            network_id: The ID of the Meraki network.
            rf_profile_id: The ID of the RF profile to retrieve.

        Returns:
            A dictionary containing the RF profile settings.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/wireless/rfProfiles/{rf_profile_id}"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            return await self._client._async_meraki_request("GET", url, headers)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error fetching wireless RF profile '{rf_profile_id}' for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching wireless RF profile '{rf_profile_id}' for network '{network_id}': {e}"
            ) from e

    async def async_get_wireless_connected_client_count(
        self, network_id: str, ap_mac: str
    ) -> int:
        """Gets the count of online clients connected to a specific Meraki access point.

        Args:
            network_id: The ID of the Meraki network.
            ap_mac: The MAC address of the Meraki access point.

        Returns:
            The number of clients with an "Online" status connected to the specified
            access point.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/clients"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            clients: List[Dict[str, Any]] = await self._client._async_meraki_request(
                "GET", url, headers
            )
            connected_clients = [
                client
                for client in clients
                if client.get("apMac") == ap_mac and client.get("status") == "Online"
            ]
            return len(connected_clients)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error fetching connected client count for AP '{ap_mac}' in network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching connected client count for AP '{ap_mac}' in network '{network_id}': {e}"
            ) from e

    async def async_get_wireless_ssids(self, network_id: str) -> List[Dict[str, Any]]:
        """Get the SSIDs configured for a Meraki network.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents an SSID
            configuration for the network.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/wireless/ssids"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        _LOGGER.debug(f"async_get_wireless_ssids: Sending GET request to {endpoint}")
        try:
            ssids = await self._client._async_meraki_request("GET", url, headers)
            _LOGGER.debug(f"async_get_wireless_ssids: Meraki API response: {ssids}")
            return ssids
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Error fetching network SSIDs for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Error fetching network SSIDs for network '{network_id}': {e}"
            ) from e

    async def async_get_network_wireless_clients(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """Get all wireless clients in a network.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a wireless client.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/wireless/clients"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            return await self._client._async_meraki_request("GET", url, headers)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Error fetching wireless clients for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Error fetching wireless clients for network '{network_id}': {e}"
            ) from e

    async def async_get_device_wireless_status(self, serial: str) -> Dict[str, Any]:
        """Get the status of a Meraki wireless device.

        Args:
            serial: Serial number of the Meraki MR access point.

        Returns:
            A dictionary containing the status information for the wireless device.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/wireless/status"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            return await self._client._async_meraki_request("GET", url, headers)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(f"Error fetching wireless status for device '{serial}': {e}")
            raise MerakiApiError(
                f"Error fetching wireless status for device '{serial}': {e}"
            ) from e

    # Add other wireless-related API calls here as needed.
    # Examples:
    # - async_get_network_wireless_settings(...)
    # - async_get_network_wireless_signal_quality_history(...)
