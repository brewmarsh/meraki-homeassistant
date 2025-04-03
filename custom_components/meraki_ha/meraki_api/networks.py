import aiohttp  # Keep aiohttp import
from typing import List, Dict, Optional
import logging

from ._api_client import _async_meraki_request  # Import the common function
from .exceptions import MerakiApiError  # Import MerakiApiError

_LOGGER = logging.getLogger(__name__)


async def get_meraki_networks(
    api_key: str, organization_id: str  # Removed session parameter
) -> Optional[List[Dict[str, str]]]:
    """Retrieve a list of Meraki networks."""
    endpoint = f"/organizations/{organization_id}/networks"
    try:
        return await _async_meraki_request(
            api_key, "GET", endpoint
        )  # Removed session argument
    except aiohttp.ClientError as e:
        _LOGGER.error(f"Error retrieving Meraki networks: {e}")
        raise MerakiApiError(f"Aiohttp Client Error: {e}") from e
    except Exception as e:
        _LOGGER.error(f"An unexpected error occurred: {e}")
        raise MerakiApiError(f"Unexpected error: {e}") from e


async def get_network_clients_count(
    api_key: str, network_id: str  # Removed session parameter
) -> Optional[int]:
    """Retrieve the number of clients connected to a network in the last 24 hours."""

    endpoint = f"/networks/{network_id}/clients?timespan=86400"
    try:
        clients = await _async_meraki_request(
            api_key, "GET", endpoint
        )  # Removed session argument
        return len(clients)
    except aiohttp.ClientError as e:
        _LOGGER.error(f"Error retrieving client count for network {network_id}: {e}")
        raise MerakiApiError(f"Aiohttp Client Error: {e}") from e
    except Exception as e:
        _LOGGER.error(f"An unexpected error occurred: {e}")
        raise MerakiApiError(f"Unexpected error: {e}") from e


async def get_network_ids_and_names(
    api_key: str, org_id: str  # Removed session parameter
) -> Optional[List[Dict[str, str]]]:
    """Retrieve a list of network IDs and names."""
    networks = await get_meraki_networks(api_key, org_id)  # Removed session argument
    if networks is None:
        return None
    return [{"id": network["id"], "name": network["name"]} for network in networks]
