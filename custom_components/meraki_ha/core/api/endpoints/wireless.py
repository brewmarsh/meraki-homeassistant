"""Meraki API endpoints for wireless devices.."""

import logging
from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

from ..cache import async_timed_cache

if TYPE_CHECKING:
    from ..client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class WirelessEndpoints:
    """Wireless-related endpoints."""

    def __init__(self, api_client: "MerakiAPIClient") -> None:
        """Initialize the endpoint."""
        self._api_client = api_client
<<<<<<< HEAD
<<<<<<< HEAD
        self._dashboard = api_client.dashboard
=======
<<<<<<< HEAD
        self._dashboard = api_client.dashboard
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_ssids(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get all SSIDs for a network.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            A list of SSIDs.

        """
<<<<<<< HEAD
<<<<<<< HEAD
        ssids = await self._api_client.run_sync(
            self._dashboard.wireless.getNetworkWirelessSsids,
=======
<<<<<<< HEAD
        ssids = await self._api_client.run_sync(
            self._dashboard.wireless.getNetworkWirelessSsids,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return []
        ssids = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.getNetworkWirelessSsids,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            networkId=network_id,
        )
        validated = validate_response(ssids)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_ssids did not return a list")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_wireless_settings(self, serial: str) -> dict[str, Any]:
        """
        Get wireless radio settings for an access point.

        Args:
        ----
            serial: The serial number of the device.

        Returns
        -------
            The wireless settings.

        """
<<<<<<< HEAD
<<<<<<< HEAD
        settings = await self._api_client.run_sync(
            self._dashboard.wireless.getDeviceWirelessRadioSettings,
=======
<<<<<<< HEAD
        settings = await self._api_client.run_sync(
            self._dashboard.wireless.getDeviceWirelessRadioSettings,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return {}
        settings = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.getDeviceWirelessRadioSettings,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            serial=serial,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_wireless_settings did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    async def create_network_wireless_ssid_identity_psk(
        self,
        network_id: str,
        number: str,
        name: str,
        group_policy_id: str,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create an Identity PSK for an SSID.

        Args:
        ----
            network_id: The ID of the network.
            number: The SSID number.
            name: The name of the Identity PSK.
            group_policy_id: The group policy ID.
            **kwargs: Additional arguments.

        Returns
        -------
            The created Identity PSK.

        """
        if self._api_client.dashboard is None:
            return {}
        psk = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.createNetworkWirelessSsidIdentityPsk,
            network_id,
            number,
            name,
            group_policy_id,
            **kwargs,
        )
        validated = validate_response(psk)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "create_network_wireless_ssid_identity_psk did not return a dict"
            )
            return {}
        return validated

    @handle_meraki_errors
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    @async_timed_cache()
    async def get_network_wireless_ssid(
        self,
        network_id: str,
        number: str,
    ) -> dict[str, Any]:
        """
        Get a single SSID.

        Args:
        ----
            network_id: The ID of the network.
            number: The SSID number.

        Returns
        -------
            The SSID details.

        """
<<<<<<< HEAD
<<<<<<< HEAD
        ssid = await self._api_client.run_sync(
            self._dashboard.wireless.getNetworkWirelessSsid,
=======
<<<<<<< HEAD
        ssid = await self._api_client.run_sync(
            self._dashboard.wireless.getNetworkWirelessSsid,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return {}
        ssid = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.getNetworkWirelessSsid,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            networkId=network_id,
            number=number,
        )
        validated = validate_response(ssid)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_network_wireless_ssid did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    @async_timed_cache()
    async def get_network_wireless_settings(self, network_id: str) -> dict[str, Any]:
        """
        Get wireless settings for a network.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            The wireless settings.
        """
        if self._api_client.dashboard is None:
            return {}
        settings = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.getNetworkWirelessSettings,
            networkId=network_id,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_network_wireless_settings did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_wireless_settings(
        self, network_id: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Update wireless settings for a network.

        Args:
        ----
            network_id: The ID of the network.
            **kwargs: The settings to update.

        Returns
        -------
            The updated settings.
        """
        if self._api_client.dashboard is None:
            return {}
        settings = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.updateNetworkWirelessSettings,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_network_wireless_settings did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    async def update_network_wireless_ssid(
        self,
        network_id: str,
        number: str,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Update an SSID.

        Args:
        ----
            network_id: The ID of the network.
            number: The SSID number.
            **kwargs: The SSID settings to update.

        Returns
        -------
            The updated SSID.

        """
<<<<<<< HEAD
<<<<<<< HEAD
        ssid = await self._api_client.run_sync(
            self._dashboard.wireless.updateNetworkWirelessSsid,
=======
<<<<<<< HEAD
        ssid = await self._api_client.run_sync(
            self._dashboard.wireless.updateNetworkWirelessSsid,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return {}
        ssid = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.updateNetworkWirelessSsid,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            networkId=network_id,
            number=number,
            **kwargs,
        )
        validated = validate_response(ssid)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_network_wireless_ssid did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_wireless_rf_profiles(
        self,
        network_id: str,
    ) -> list[dict[str, Any]]:
        """
        Get all RF profiles for a network.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            A list of RF profiles.

        """
<<<<<<< HEAD
<<<<<<< HEAD
        profiles = await self._api_client.run_sync(
            self._dashboard.wireless.getNetworkWirelessRfProfiles,
=======
<<<<<<< HEAD
        profiles = await self._api_client.run_sync(
            self._dashboard.wireless.getNetworkWirelessRfProfiles,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return []
        profiles = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.getNetworkWirelessRfProfiles,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            networkId=network_id,
        )
        validated = validate_response(profiles)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_wireless_rf_profiles did not return a list")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_wireless_ssid_l7_firewall_rules(
        self,
        network_id: str,
        number: str,
    ) -> dict[str, Any]:
        """
        Get L7 firewall rules for an SSID.

        Args:
        ----
            network_id: The ID of the network.
            number: The SSID number.

        Returns
        -------
            The L7 firewall rules.

        """
<<<<<<< HEAD
<<<<<<< HEAD
        rules = await self._api_client.run_sync(
            self._dashboard.wireless.getNetworkWirelessSsidL7FirewallRules,
=======
<<<<<<< HEAD
        rules = await self._api_client.run_sync(
            self._dashboard.wireless.getNetworkWirelessSsidL7FirewallRules,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return {}
        rules = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.getNetworkWirelessSsidL7FirewallRules,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            networkId=network_id,
            number=number,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "getNetworkWirelessSsidFirewallL7FirewallRules did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_wireless_ssid_l7_firewall_rules(
        self,
        network_id: str,
        number: str,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Update L7 firewall rules for an SSID.

        Args:
        ----
            network_id: The ID of the network.
            number: The SSID number.
            **kwargs: The L7 firewall rules to update.

        Returns
        -------
            The updated L7 firewall rules.

        """
<<<<<<< HEAD
<<<<<<< HEAD
        rules = await self._api_client.run_sync(
            self._dashboard.wireless.updateNetworkWirelessSsidL7FirewallRules,
=======
<<<<<<< HEAD
        rules = await self._api_client.run_sync(
            self._dashboard.wireless.updateNetworkWirelessSsidL7FirewallRules,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return {}
        rules = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.updateNetworkWirelessSsidL7FirewallRules,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            networkId=network_id,
            number=number,
            **kwargs,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "updateNetworkWirelessSsidFirewallL7FirewallRules "
                "did not return a dict",
            )
            return {}
        return validated
