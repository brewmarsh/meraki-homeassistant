"""Handles Meraki network-specific API interactions.

This module provides functions to retrieve information about Meraki networks
within an organization, including network lists, client counts, and basic
network details like ID and name. It utilizes the centralized
`_async_meraki_request` function for API calls.
"""
import aiohttp
from typing import List, Dict, Optional
import logging

from ._api_client import _async_meraki_request
from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


async def get_meraki_networks(
    api_key: str, organization_id: str
) -> Optional[List[Dict[str, str]]]:
    """Retrieves a list of all Meraki networks within a given organization.

    Args:
        api_key (str): The Meraki API key for authentication.
        organization_id (str): The ID of the Meraki organization.

    Returns:
        Optional[List[Dict[str, str]]]: A list of dictionaries, where each
            dictionary represents a network and contains details such as 'id',
            'name', 'productTypes', 'timeZone', etc. Returns None if the
            API request fails and an error is logged, though the current
            implementation raises MerakiApiError in such cases.

    Raises:
        MerakiApiError: If an `aiohttp.ClientError` (e.g., connection error)
            or any other unexpected exception occurs during the API request.
    """
    endpoint = f"/organizations/{organization_id}/networks"
    _LOGGER.debug("Retrieving Meraki networks for organization ID: %s", organization_id)
    try:
        # Make the API request to fetch network data.
        networks_data = await _async_meraki_request(api_key, "GET", endpoint)
        # The _async_meraki_request is expected to return a list of dicts.
        # Add type checking if there's a chance of other return types.
        if not isinstance(networks_data, list):
            _LOGGER.warning(
                "Expected list of networks, got %s for organization %s",
                type(networks_data),
                organization_id,
            )
            # Depending on desired strictness, could return None or raise error.
            # Raising an error might be better for unexpected formats.
            # For now, matching original Optional return, though None case seems unlikely due to raises.
            return None
        return networks_data
    except aiohttp.ClientError as e:
        _LOGGER.error(
            "Aiohttp client error retrieving Meraki networks for org %s: %s",
            organization_id,
            e,
        )
        raise MerakiApiError(f"Aiohttp Client Error: {e}") from e
    except Exception as e:
        _LOGGER.error(
            "Unexpected error retrieving Meraki networks for org %s: %s",
            organization_id,
            e,
        )
        raise MerakiApiError(f"Unexpected error: {e}") from e


async def get_network_clients_count(
    api_key: str, network_id: str
) -> Optional[int]:
    """Retrieves the count of clients connected to a network in the last 24 hours.

    Args:
        api_key (str): The Meraki API key.
        network_id (str): The ID of the Meraki network.

    Returns:
        Optional[int]: The number of clients connected to the network within
            the timespan. Returns None if the client list cannot be retrieved
            or is not in the expected list format, though current error handling
            will raise MerakiApiError.

    Raises:
        MerakiApiError: If an API error occurs during the request.
    """
    # timespan=86400 means clients seen in the last 24 hours.
    endpoint = f"/networks/{network_id}/clients?timespan=86400"
    _LOGGER.debug("Retrieving client count for network ID: %s", network_id)
    try:
        # Fetch the list of clients.
        clients = await _async_meraki_request(api_key, "GET", endpoint)
        # The response is expected to be a list of client objects.
        if isinstance(clients, list):
            return len(clients)
        else:
            _LOGGER.warning(
                "Expected a list of clients for network %s, but received type %s.",
                network_id,
                type(clients),
            )
            # Consistent with Optional return, but raising error might be preferred.
            return None
    except aiohttp.ClientError as e:
        _LOGGER.error(
            "Aiohttp client error retrieving client count for network %s: %s",
            network_id,
            e,
        )
        raise MerakiApiError(f"Aiohttp Client Error: {e}") from e
    except Exception as e:
        _LOGGER.error(
            "Unexpected error retrieving client count for network %s: %s", network_id, e
        )
        raise MerakiApiError(f"Unexpected error: {e}") from e


async def get_network_ids_and_names(
    api_key: str, org_id: str
) -> Optional[List[Dict[str, str]]]:
    """Retrieves a simplified list of network IDs and names for an organization.

    This function first fetches all networks for the given organization and then
    extracts just the 'id' and 'name' for each network.

    Args:
        api_key (str): The Meraki API key.
        org_id (str): The ID of the Meraki organization.

    Returns:
        Optional[List[Dict[str, str]]]: A list of dictionaries, where each
            dictionary contains the 'id' and 'name' of a network.
            Returns None if the initial network fetch fails (e.g., returns None
            or raises an exception that's caught and results in None).

    Raises:
        MerakiApiError: Propagated from `get_meraki_networks` if an API error
            occurs during the initial network fetch.
    """
    _LOGGER.debug("Retrieving network IDs and names for organization ID: %s", org_id)
    try:
        # Fetch the full list of networks for the organization.
        networks = await get_meraki_networks(api_key, org_id)

        # If networks is None (e.g., due to an error in get_meraki_networks
        # that somehow didn't raise an exception, or if that function changes
        # to return None more broadly), propagate the None.
        if networks is None:
            _LOGGER.warning(
                "Received None for networks list for organization %s. Cannot extract IDs and names.",
                org_id,
            )
            return None

        # Extract 'id' and 'name' from each network dictionary.
        # This assumes each network dict in the list will have 'id' and 'name' keys.
        return [
            {"id": network["id"], "name": network["name"]}
            for network in networks
            if "id" in network and "name" in network # Basic check for key existence
        ]
    except MerakiApiError:
        # Re-raise MerakiApiError if it occurs during get_meraki_networks.
        # No specific logging here as it would be logged in get_meraki_networks.
        raise
    except Exception as e:
        # Catch any other unexpected errors during the list comprehension or processing.
        _LOGGER.error(
            "Unexpected error processing network IDs and names for org %s: %s", org_id, e
        )
        # Optionally, could raise a new MerakiApiError here.
        # For now, returning None to match original Optional signature if not MerakiApiError.
        return None
