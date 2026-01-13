"""Meraki API endpoints for appliances."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

from ..cache import async_timed_cache

if TYPE_CHECKING:
    from ..client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class ApplianceEndpoints:
    """Appliance-related endpoints."""

    def __init__(self, api_client: MerakiAPIClient, hass: HomeAssistant) -> None:
        """
        Initialize the endpoint.

        Args:
            api_client: The Meraki API client.
            hass: The Home Assistant instance.

        """
        self._api_client = api_client
        self._dashboard = api_client.dashboard
        self._hass = hass

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_network_appliance_traffic(
        self,
        network_id: str,
        timespan: int = 86400,
    ) -> list[dict[str, Any]]:
        """
        Get traffic data for a network appliance.

        Args:
            network_id: The ID of the network.
            timespan: The timespan for the traffic data.

        Returns
        -------
            A list of traffic data.

        """
        traffic = await self._api_client.run_sync(
            self._dashboard.appliance.getNetworkApplianceTraffic,
            networkId=network_id,
            timespan=timespan,
        )
        validated = validate_response(traffic)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_appliance_traffic did not return a list")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_vlans(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get VLANs for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            A list of VLANs.

        """
        vlans = await self._api_client.run_sync(
            self._dashboard.appliance.getNetworkApplianceVlans,
            networkId=network_id,
        )
        validated = validate_response(vlans)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_vlans did not return a list")
            return []
        return validated

    @handle_meraki_errors
    async def update_network_vlan(
        self,
        network_id: str,
        vlan_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update a VLAN.

        Args:
            network_id: The ID of the network.
            vlan_id: The ID of the VLAN.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated VLAN.

        """
        vlan = await self._api_client.run_sync(
            self._dashboard.appliance.updateNetworkApplianceVlan,
            networkId=network_id,
            vlanId=vlan_id,
            **kwargs,
        )
        validated = validate_response(vlan)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_network_vlan did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_l3_firewall_rules(self, network_id: str) -> dict[str, Any]:
        """
        Get L3 firewall rules for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The L3 firewall rules.

        """
        rules = await self._api_client.run_sync(
            self._dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules,
            networkId=network_id,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_l3_firewall_rules did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def update_l3_firewall_rules(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update L3 firewall rules for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated L3 firewall rules.

        """
        rules = await self._api_client.run_sync(
            self._dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_l3_firewall_rules did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_traffic_shaping(self, network_id: str) -> dict[str, Any]:
        """
        Get traffic shaping settings for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The traffic shaping settings.

        """
        settings = await self._api_client.run_sync(
            self._dashboard.appliance.getNetworkApplianceTrafficShaping,
            networkId=network_id,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_traffic_shaping did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def update_traffic_shaping(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update traffic shaping settings for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated traffic shaping settings.

        """
        settings = await self._api_client.run_sync(
            self._dashboard.appliance.updateNetworkApplianceTrafficShaping,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_traffic_shaping did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_vpn_status(self, network_id: str) -> dict[str, Any]:
        """
        Get site-to-site VPN status for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The VPN status.

        """
        status = await self._api_client.run_sync(
            self._dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn,
            networkId=network_id,
        )
        validated = validate_response(status)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_vpn_status did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def update_vpn_status(self, network_id: str, **kwargs: Any) -> dict[str, Any]:
        """
        Update site-to-site VPN status for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated VPN status.

        """
        status = await self._api_client.run_sync(
            self._dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(status)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_vpn_status did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_device_appliance_uplinks_settings(
        self,
        serial: str,
    ) -> dict[str, Any]:
        """
        Get uplinks settings for a device.

        Args:
            serial: The serial number of the device.

        Returns
        -------
            The uplinks settings.

        """
        uplinks = await self._api_client.run_sync(
            self._dashboard.appliance.getDeviceApplianceUplinksSettings,
            serial=serial,
        )
        validated = validate_response(uplinks)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_device_appliance_uplinks_settings did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_appliance_content_filtering(
        self,
        network_id: str,
    ) -> dict[str, Any]:
        """
        Get content filtering settings for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The content filtering settings.

        """
        result = await self._api_client.run_sync(
            self._dashboard.appliance.getNetworkApplianceContentFiltering,
            networkId=network_id,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_content_filtering did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_appliance_content_filtering_categories(
        self,
        network_id: str,
    ) -> dict[str, Any]:
        """
        Get content filtering categories for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The content filtering categories.

        """
        result = await self._api_client.run_sync(
            self._dashboard.appliance.getNetworkApplianceContentFilteringCategories,
            networkId=network_id,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_content_filtering_categories "
                "did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    async def reboot_device(self, serial: str) -> dict[str, Any]:
        """
        Reboot a device.

        Args:
            serial: The serial number of the device.

        Returns
        -------
            The response from the API.

        """
        result = await self._api_client.run_sync(
            self._dashboard.devices.rebootDevice,
            serial=serial,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning("reboot_device did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_appliance_ports(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get all ports for an appliance.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            A list of ports.

        """
        ports = await self._api_client.run_sync(
            self._dashboard.appliance.getNetworkAppliancePorts,
            networkId=network_id,
        )
        validated = validate_response(ports)
        if not isinstance(validated, list):
            _LOGGER.warning("get_appliance_ports did not return a list")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_appliance_settings(self, network_id: str) -> dict[str, Any]:
        """
        Get settings for a network appliance.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The settings for the network appliance.

        """
        settings = await self._api_client.run_sync(
            self._dashboard.appliance.getNetworkApplianceSettings,
            networkId=network_id,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_network_appliance_settings did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_appliance_l7_firewall_rules(
        self,
        network_id: str,
    ) -> dict[str, Any]:
        """
        Get L7 firewall rules for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The L7 firewall rules.

        """
        rules = await self._api_client.run_sync(
            self._dashboard.appliance.getNetworkApplianceL7FirewallRules,
            networkId=network_id,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_l7_firewall_rules did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_appliance_l7_firewall_rules(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update L7 firewall rules for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated L7 firewall rules.

        """
        rules = await self._api_client.run_sync(
            self._dashboard.appliance.updateNetworkApplianceL7FirewallRules,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "update_network_appliance_l7_firewall_rules did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_appliance_content_filtering(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update content filtering for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated content filtering settings.

        """
        result = await self._api_client.run_sync(
            self._dashboard.appliance.updateNetworkApplianceContentFiltering,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "update_network_appliance_content_filtering did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_organization_appliance_uplink_statuses(self) -> list[dict[str, Any]]:
        """
        Get uplink status for all appliances in the organization.

        Returns
        -------
            A list of uplink statuses.

        """
        statuses = await self._api_client.run_sync(
            self._dashboard.appliance.getOrganizationApplianceUplinkStatuses,
            organizationId=self._api_client.organization_id,
            total_pages="all",
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_organization_appliance_uplink_statuses did not return a list",
            )
            return []
        return validated
