import aiohttp
from typing import List, Dict, Optional
import logging

_LOGGER = logging.getLogger(__name__)


async def get_meraki_networks(
    api_key: str, organization_id: str
) -> Optional[List[Dict[str, str]]]:
    """Retrieve a list of Meraki networks."""
    base_url = "https://api.meraki.com/api/v1"
    endpoint = f"/organizations/{organization_id}/networks"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{base_url}{endpoint}", headers=headers
            ) as response:
                if response.status != 200:
                    _LOGGER.error(
                        f"Failed to retrieve Meraki networks. Status code: {response.status}"
                    )
                    try:
                        error_text = await response.text()
                        _LOGGER.error(f"Response content: {error_text}")
                    except aiohttp.ClientError:
                        _LOGGER.error("Failed to read response content.")
                    return None
                networks = await response.json()
                return networks
    except aiohttp.ClientError as e:
        _LOGGER.error(f"Error retrieving Meraki networks: {e}")
        return None
    except Exception as e:
        _LOGGER.error(f"An unexpected error occurred: {e}")
        return None


async def get_network_clients_count(api_key: str, network_id: str) -> Optional[int]:
    """Retrieve the number of clients connected to a network in the last 24 hours."""
    base_url = "https://api.meraki.com/api/v1"
    endpoint = f"/networks/{network_id}/clients?timespan=86400"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{base_url}{endpoint}", headers=headers
            ) as response:
                if response.status != 200:
                    _LOGGER.error(
                        f"Failed to retrieve client count for network {network_id}. Status code: {response.status}"
                    )
                    return None
                clients = await response.json()
                return len(clients)
    except aiohttp.ClientError as e:
        _LOGGER.error(f"Error retrieving client count for network {network_id}: {e}")
        return None
    except Exception as e:
        _LOGGER.error(f"An unexpected error occurred: {e}")
        return None


async def get_network_ids_and_names(
    api_key: str, org_id: str
) -> Optional[List[Dict[str, str]]]:
    """Retrieve a list of network IDs and names."""
    networks = await get_meraki_networks(api_key, org_id)
    if networks is None:
        return None
    return [{"id": network["id"], "name": network["name"]} for network in networks]
