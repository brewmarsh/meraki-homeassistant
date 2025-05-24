# /config/custom_components/meraki_ha/meraki_api/networks.py
import logging
from typing import List, Dict, Optional
from ._api_client import MerakiAPIClient
from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


class MerakiNetworksAPI:
    """Meraki networks API functions."""

    def __init__(self, client: MerakiAPIClient):
        """Initialize the Meraki Networks API.

        Args:
            client: An instance of the MerakiAPIClient.
        """
        self._client = client

    async def async_get_organization_networks(
        self, organization_id: str
    ) -> Optional[List[Dict[str, str]]]:
        """Retrieve a list of Meraki networks for an organization.

        Args:
            organization_id: The ID of the Meraki organization.

        Returns:
            A list of dictionaries, where each dictionary represents a Meraki network,
            or None if an error occurs.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/organizations/{organization_id}/networks"
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
                f"Unexpected error retrieving Meraki networks for organization '{organization_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error retrieving Meraki networks for organization '{organization_id}': {e}"
            ) from e

    async def async_get_network_clients_count(self, network_id: str) -> Optional[int]:
        """Retrieve the number of clients connected to a network in the last 24 hours.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            The number of clients connected to the network in the last 24 hours,
            or None if an error occurs.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/clients"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        params = {"timespan": 86400}
        try:
            clients = await self._client._async_meraki_request(
                "GET", url, headers, params=params
            )
            return len(clients)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error retrieving client count for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error retrieving client count for network '{network_id}': {e}"
            ) from e

    async def async_get_network_ids_and_names(
        self, organization_id: str
    ) -> Optional[List[Dict[str, str]]]:
        """Retrieve a list of network IDs and names for an organization.

        Args:
            organization_id: The ID of the Meraki organization.

        Returns:
            A list of dictionaries, where each dictionary contains the 'id' and 'name'
            of a Meraki network, or None if an error occurs.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        networks = await self.async_get_organization_networks(organization_id)
        if networks is None:
            return None
        return [{"id": network["id"], "name": network["name"]} for network in networks]

    # Add other network-related API calls here as needed.
    # Examples:
    # - async_get_network_devices(...)
    # - async_get_network_alerts(...)
    # - async_get_network_snmp(...)
