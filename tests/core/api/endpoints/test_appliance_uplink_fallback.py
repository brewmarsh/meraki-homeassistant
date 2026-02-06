"""Fetch strategy for Meraki Appliance (MX) devices."""

from __future__ import annotations

import logging
from typing import Any

import meraki

from .base import MerakiFetchStrategy

_LOGGER = logging.getLogger(__name__)

class ApplianceFetchStrategy(MerakiFetchStrategy):
    """Strategy for fetching MX-specific data."""

    async def fetch_device_data(self, device_serial: str, network_id: str) -> dict[str, Any]:
        """Fetch all relevant data for an MX appliance."""
        data = {}

        # 1. Fetch Uplink Performance (Handled with dynamic fallbacks)
        data["uplink_performance"] = await self._get_uplink_performance(network_id)

        # 2. Fetch Appliance Ports (Handled with 400-error sanitization)
        data["ports"] = await self._get_appliance_ports(network_id)

        return data

    async def _get_uplink_performance(self, network_id: str) -> list[dict[str, Any]]:
        """
        Fetch performance data using version-resilient SDK methods.
        Tries UsageHistory first for 60s granularity.
        """
        methods_to_try = [
            ("getNetworkApplianceUplinksUsageHistory", {"timespan": 60}),
            ("getNetworkApplianceUplinksLossAndLatency", {}),
            ("getNetworkApplianceUplinksUplinksLossAndLatency", {}), # SDK Bug fallback
        ]

        appliance_api = self.client.dashboard.appliance

        for method_name, extra_args in methods_to_try:
            method = getattr(appliance_api, method_name, None)
            if method:
                try:
                    _LOGGER.debug("Fetching uplink performance via %s", method_name)
                    return await self.client.run_sync(
                        method, 
                        networkId=network_id, 
                        **extra_args
                    )
                except meraki.APIError as e:
                    _LOGGER.debug("Method %s failed or not supported: %s", method_name, e)
                    continue
        
        _LOGGER.warning("All uplink performance fetch methods failed for network %s", network_id)
        return []

    async def _get_appliance_ports(self, network_id: str) -> list[dict[str, Any]]:
        """
        Fetch MX port status. 
        Gracefully handles the 400 error if VLANs are disabled.
        """
        try:
            return await self.client.run_sync(
                self.client.dashboard.appliance.getNetworkAppliancePorts,
                networkId=network_id
            )
        except meraki.APIError as e:
            if e.status == 400 and "VLANs" in str(e.message):
                # This is a configuration requirement, not a code error.
                _LOGGER.warning(
                    "Cannot fetch Port status for network %s: VLANs must be enabled in the Meraki Dashboard",
                    network_id
                )
                return []
            
            # Re-raise if it's a different kind of error
            raise e

    async def fetch_traffic_data(self, network_id: str) -> list[dict[str, Any]]:
        """Fetch traffic analysis, silencing 400 errors if disabled."""
        try:
            return await self.client.run_sync(
                self.client.dashboard.networks.getNetworkTraffic,
                networkId=network_id,
                timespan=3600
            )
        except meraki.APIError as e:
            if e.status == 400 and "Traffic Analysis" in str(e.message):
                _LOGGER.debug("Traffic analysis is disabled for network %s", network_id)
                return []
            raise e