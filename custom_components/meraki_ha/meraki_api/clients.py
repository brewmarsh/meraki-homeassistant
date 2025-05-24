# /config/custom_components/meraki_ha/meraki_api/clients.py
import logging
from typing import Any, Dict, List

from ._api_client import MerakiAPIClient
from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha clients.py loaded")


class MerakiClientsAPI:
    """Meraki client API functions."""

    def __init__(self, client: MerakiAPIClient):
        """Initialize the Meraki Clients API.

        Args:
            client: An instance of the MerakiAPIClient.
        """
        self._client = client

    async def async_update_connected_clients(
        self, org_id: str, serial: str, clients: List[Dict[str, Any]]
    ) -> None:
        """Update connected clients (currently a placeholder).

        This function is a placeholder and doesn't perform any actual updates.
        It can be expanded to implement client update logic if needed.

        Args:
            org_id: Meraki organization ID.
            serial: Meraki device serial number.
            clients: List of connected clients (currently unused).
        """
        _LOGGER.debug(f"Updating connected clients for device serial: {serial}")
        # Add your client update logic here if required.
        # For now, it's just a placeholder.
        _LOGGER.debug(f"Client update placeholder called for {serial}")

    async def async_get_device_clients(self, serial: str) -> List[Dict[str, Any]]:
        """Get the clients associated with a specific Meraki device.

        Args:
            serial: Device serial number.

        Returns:
            A list of clients associated with the device.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/clients"
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
                f"Unexpected error getting clients for device '{serial}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error getting clients for device '{serial}': {e}"
            ) from e

    async def async_get_network_clients(
        self, network_id: str, timespan: int = 86400
    ) -> List[Dict[str, Any]]:
        """Get the clients associated with a network, optionally within a timespan.

        Args:
            network_id: Network ID.
            timespan: The timespan for which to retrieve clients, in seconds (default: 24 hours).

        Returns:
            A list of clients associated with the network.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/clients"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        params = {"timespan": timespan}
        try:
            return await self._client._async_meraki_request(
                "GET", url, headers, params=params
            )
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error getting clients for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error getting clients for network '{network_id}': {e}"
            ) from e

    async def async_get_client(self, client_id: str) -> Dict[str, Any]:
        """Get details for a specific Meraki client.

        Args:
            client_id: The ID of the client.

        Returns:
            A dictionary containing the details of the Meraki client.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/clients/{client_id}"
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
                f"Unexpected error getting client details for client '{client_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error getting client details for client '{client_id}': {e}"
            ) from e

    # Add other client-related API calls here as needed.
    # Examples:
    # - async_get_network_client_policy(...)
    # - async_update_network_client_policy(...)
