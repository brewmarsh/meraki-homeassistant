import aiohttp
from typing import List, Dict, Optional
import logging

_LOGGER = logging.getLogger(__name__)


async def get_meraki_networks(
    api_key: str, organization_id: str
) -> Optional[List[Dict[str, str]]]:
    """Retrieve a list of Meraki networks."""
    base_url = "https://api.meraki.com/api/v1"
    endpoint = f"/organizations/{organization_id}/networks"  # Corrected endpoint
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
