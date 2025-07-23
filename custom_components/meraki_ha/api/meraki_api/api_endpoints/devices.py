from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from .._api_client import MerakiAPIClient


class Devices:
    """Mock for devices endpoint."""

    def __init__(self, client: "MerakiAPIClient"):
        self._client = client

    async def getDeviceClients(self, serial: str) -> List[Dict[str, Any]]:
        """Mock for getDeviceClients."""
        return await self._client.get_device_clients(serial)

    async def getDeviceUplink(self, serial: str) -> Dict[str, Any]:
        """Mock for getDeviceUplink."""
        return await self._client.get_device_uplink(serial)
