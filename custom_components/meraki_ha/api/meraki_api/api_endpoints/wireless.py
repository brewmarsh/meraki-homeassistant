from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from .._api_client import MerakiAPIClient


class Wireless:
    """Mock for wireless endpoint."""

    def __init__(self, client: "MerakiAPIClient"):
        self._client = client

    async def getNetworkWirelessSsids(self, networkId: str) -> List[Dict[str, Any]]:
        """Mock for getNetworkWirelessSsids."""
        return await self._client.get_network_wireless_ssids(networkId)
