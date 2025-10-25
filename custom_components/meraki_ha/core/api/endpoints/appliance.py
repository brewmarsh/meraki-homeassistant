"""Meraki API endpoints for appliances."""

import logging
from typing import Any

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

from ..cache import async_timed_cache

_LOGGER = logging.getLogger(__name__)


class ApplianceEndpoints:
    """Appliance-related endpoints."""

    def __init__(self, api_client, hass: HomeAssistant):
        """Initialize the endpoint."""
        self._api_client = api_client
        self._dashboard = api_client._dashboard
        self._hass = hass

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_network_appliance_traffic(
        self, network_id: str, timespan: int = 86400
    ) -> list[dict[str, Any]]:
        """Get traffic data for a network appliance."""
        traffic = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceTraffic,
            networkId=network_id,
            timespan=timespan,
        )
        validated = validate_response(traffic)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_appliance_traffic did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_vlans(self, network_id: str) -> list[dict[str, Any]]:
        """Get VLANs for a network."""
        vlans = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceVlans,
            networkId=network_id,
        )
        validated = validate_response(vlans)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_vlans did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    async def update_network_vlan(
        self, network_id: str, vlan_id: str, **kwargs
    ) -> dict[str, Any]:
        """Update a VLAN."""
        vlan = await self._api_client._run_sync(
            self._dashboard.appliance.updateNetworkApplianceVlan,
            networkId=network_id,
            vlanId=vlan_id,
            **kwargs,
        )
        validated = validate_response(vlan)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_network_vlan did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_l3_firewall_rules(self, network_id: str) -> dict[str, Any]:
        """Get L3 firewall rules for a network."""
        rules = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules,
            networkId=network_id,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_l3_firewall_rules did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def update_l3_firewall_rules(
        self, network_id: str, **kwargs
    ) -> dict[str, Any]:
        """Update L3 firewall rules for a network."""
        rules = await self._api_client._run_sync(
            self._dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_l3_firewall_rules did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_traffic_shaping(self, network_id: str) -> dict[str, Any]:
        """Get traffic shaping settings for a network."""
        settings = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceTrafficShaping,
            networkId=network_id,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_traffic_shaping did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def update_traffic_shaping(self, network_id: str, **kwargs) -> dict[str, Any]:
        """Update traffic shaping settings for a network."""
        settings = await self._api_client._run_sync(
            self._dashboard.appliance.updateNetworkApplianceTrafficShaping,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_traffic_shaping did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_vpn_status(self, network_id: str) -> dict[str, Any]:
        """Get site-to-site VPN status for a network."""
        status = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn,
            networkId=network_id,
        )
        validated = validate_response(status)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_vpn_status did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def update_vpn_status(self, network_id: str, **kwargs) -> dict[str, Any]:
        """Update site-to-site VPN status for a network."""
        status = await self._api_client._run_sync(
            self._dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(status)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_vpn_status did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_device_appliance_uplinks_settings(
        self, serial: str
    ) -> dict[str, Any]:
        """Get uplinks settings for a device."""
        uplinks = await self._api_client._run_sync(
            self._dashboard.appliance.getDeviceApplianceUplinksSettings,
            serial=serial,
        )
        validated = validate_response(uplinks)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_device_appliance_uplinks_settings did not return a dict."
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_appliance_content_filtering(
        self, network_id: str
    ) -> dict[str, Any]:
        """Get content filtering settings for a network."""
        result = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceContentFiltering,
            networkId=network_id,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_content_filtering did not return a dict."
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_appliance_content_filtering_categories(
        self, network_id: str
    ) -> dict[str, Any]:
        """Get content filtering categories for a network."""
        result = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceContentFilteringCategories,
            networkId=network_id,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_content_filtering_categories "
                "did not return a dict."
            )
            return {}
        return validated

    @handle_meraki_errors
    async def reboot_device(self, serial: str) -> dict[str, Any]:
        """Reboot a device."""
        result = await self._api_client._run_sync(
            self._dashboard.devices.rebootDevice, serial=serial
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning("reboot_device did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_appliance_ports(self, network_id: str) -> list[dict[str, Any]]:
        """Get all ports for an appliance."""
        ports = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkAppliancePorts,
            networkId=network_id,
        )
        validated = validate_response(ports)
        if not isinstance(validated, list):
            _LOGGER.warning("get_appliance_ports did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_appliance_settings(self, network_id: str) -> dict[str, Any]:
        """Get settings for a network appliance."""
        settings = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceSettings,
            networkId=network_id,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_network_appliance_settings did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_appliance_l7_firewall_rules(
        self, network_id: str
    ) -> dict[str, Any]:
        """Get L7 firewall rules for a network."""
        rules = await self._api_client._run_sync(
            self._dashboard.appliance.getNetworkApplianceL7FirewallRules,
            networkId=network_id,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_l7_firewall_rules did not return a dict."
            )
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_appliance_l7_firewall_rules(
        self, network_id: str, **kwargs
    ) -> dict[str, Any]:
        """Update L7 firewall rules for a network."""
        rules = await self._api_client._run_sync(
            self._dashboard.appliance.updateNetworkApplianceL7FirewallRules,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "update_network_appliance_l7_firewall_rules did not return a dict."
            )
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_appliance_content_filtering(
        self, network_id: str, **kwargs
    ) -> dict[str, Any]:
        """Update content filtering for a network."""
        result = await self._api_client._run_sync(
            self._dashboard.appliance.updateNetworkApplianceContentFiltering,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "update_network_appliance_content_filtering did not return a dict."
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_organization_appliance_uplink_statuses(self) -> list[dict[str, Any]]:
        """Get uplink status for all appliances in the organization."""
        statuses = await self._api_client._run_sync(
            self._dashboard.appliance.getOrganizationApplianceUplinkStatuses,
            organizationId=self._api_client.organization_id,
            total_pages="all",
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_organization_appliance_uplink_statuses did not return a list."
            )
            return []
        return validated
