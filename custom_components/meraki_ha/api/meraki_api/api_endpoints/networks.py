from typing import TYPE_CHECKING, List, Dict, Any

if TYPE_CHECKING:
    from .._api_client import MerakiAPIClient


class Networks:
    """Mock for networks endpoint."""

    def __init__(self, client: "MerakiAPIClient"):
        self._client = client

    async def getNetworkDevices(self, networkId: str) -> List[Dict[str, Any]]:
        """Mock for getNetworkDevices."""
        return await self._client.get_network_devices(networkId)

    async def getNetworkClients(
        self, networkId: str, timespan: int
    ) -> List[Dict[str, Any]]:
        """Mock for getNetworkClients."""
        return await self._client.get_network_clients(networkId)

    async def provisionNetworkClients(
        self,
        networkId: str,
        clients: List[Dict[str, Any]],
        policiesByMac: Dict[str, Any],
        groupPolicyId: str,
    ) -> Dict[str, Any]:
        """Mock for provisionNetworkClients."""
        return await self._client.provision_network_clients(
            networkId, clients, policiesByMac, groupPolicyId
        )

    async def getNetworkWirelessSsids(self, networkId: str) -> List[Dict[str, Any]]:
        """Mock for getNetworkWirelessSsids."""
        return await self._client.get_network_wireless_ssids(networkId)

    async def getNetworkApplianceSettings(self, networkId: str) -> Dict[str, Any]:
        """Mock for getNetworkApplianceSettings."""
        return await self._client.get_network_appliance_settings(networkId)
