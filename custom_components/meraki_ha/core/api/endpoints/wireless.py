"""Meraki API endpoints for wireless devices.."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.core.utils.api import (
    handle_meraki_errors,
    validate_response,
)

from ..cache import async_timed_cache

if TYPE_CHECKING:
    from ..protocol import MerakiApiClientProtocol

_LOGGER = logging.getLogger(__name__)


class WirelessEndpoints:
    """Wireless-related endpoints."""

    def __init__(self, api_client: MerakiApiClientProtocol) -> None:
        """Initialize the endpoint."""
        self._api_client = api_client

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
        ssids = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.getNetworkWirelessSsids,
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
        settings = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.getDeviceWirelessRadioSettings,
            serial=serial,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_wireless_settings did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
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
        ssid = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.getNetworkWirelessSsid,
            networkId=network_id,
            number=number,
        )
        validated = validate_response(ssid)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_network_wireless_ssid did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
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
        ssid = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.updateNetworkWirelessSsid,
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
        profiles = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.getNetworkWirelessRfProfiles,
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
        rules = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.getNetworkWirelessSsidL7FirewallRules,
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

    def get_network_detail_tasks(
        self,
        network_id: str,
        product_types: list[str],
    ) -> dict[str, Any]:
        """
        Get tasks to fetch detailed data for a network.

        Args:
        ----
            network_id: The ID of the network.
            product_types: The product types of the network.

        Returns
        -------
            A dictionary of tasks.

        """
        tasks: dict[str, Any] = {}
        if "wireless" in product_types:
            tasks[f"ssids_{network_id}"] = self._api_client.run_with_semaphore(
                self.get_network_ssids(network_id),
            )
            tasks[f"rf_profiles_{network_id}"] = self._api_client.run_with_semaphore(
                self.get_network_wireless_rf_profiles(network_id),
            )
        return tasks

    def _process_network_ssids(
        self,
        detail_data: dict[str, Any],
        network_id: str,
        previous_data: dict[str, Any] | None,
        result: dict[str, Any],
    ) -> None:
        network_ssids_key = f"ssids_{network_id}"
        network_ssids = detail_data.get(network_ssids_key)
        if isinstance(network_ssids, list):
            for ssid in network_ssids:
                if "unconfigured ssid" not in ssid.get("name", "").lower():
                    ssid["networkId"] = network_id
                    result["ssids"].append(ssid)
        elif previous_data and network_ssids_key in previous_data:
            result["ssids"].extend(previous_data[network_ssids_key])

    def _process_network_rf_profiles(
        self,
        detail_data: dict[str, Any],
        network_id: str,
        previous_data: dict[str, Any] | None,
        result: dict[str, Any],
    ) -> None:
        network_rf_profiles_key = f"rf_profiles_{network_id}"
        network_rf_profiles = detail_data.get(network_rf_profiles_key)
        if isinstance(network_rf_profiles, list):
            result["rf_profiles"][network_id] = network_rf_profiles
        elif previous_data and network_rf_profiles_key in previous_data:
            result["rf_profiles"][network_id] = previous_data[network_rf_profiles_key]

    def process_network_detail_data(
        self,
        detail_data: dict[str, Any],
        network_id: str,
        previous_data: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """
        Process the detailed data for a network.

        Args:
        ----
            detail_data: The raw detailed data from the API.
            network_id: The ID of the network.
            previous_data: The previous data from the coordinator.

        Returns
        -------
            The processed detailed data.

        """
        result: dict[str, Any] = {
            "ssids": [],
            "rf_profiles": {},
        }

        self._process_network_ssids(detail_data, network_id, previous_data, result)
        self._process_network_rf_profiles(
            detail_data, network_id, previous_data, result
        )

        return result

    @handle_meraki_errors
    async def create_identity_psk(
        self,
        network_id: str,
        number: str,
        name: str,
        group_policy_id: str | None = None,
        passphrase: str | None = None,
    ) -> dict[str, Any]:
        """
        Create an Identity PSK.

        Args:
        ----
            network_id: The ID of the network.
            number: The SSID number.
            name: The name of the Identity PSK.
            group_policy_id: The ID of the group policy to apply.
            passphrase: The passphrase for the Identity PSK.

        Returns
        -------
            The created Identity PSK.

        """
        if self._api_client.dashboard is None:
            return {}

        # Construct payload manually to avoid Python library's strict
        # positional argument
        payload: dict[str, Any] = {
            "name": name,
        }

        if group_policy_id is not None:
            payload["groupPolicyId"] = group_policy_id

        if passphrase:
            payload["passphrase"] = passphrase

        _LOGGER.debug(
            "Calling createNetworkWirelessSsidIdentityPsk with networkId=%s, "
            "number=%s, payload=%s",
            network_id,
            number,
            {k: v if k != "passphrase" else "***" for k, v in payload.items()},
        )

        metadata = {
            "tags": ["wireless", "configure", "ssids", "identityPsks"],
            "operation": "createNetworkWirelessSsidIdentityPsk",
        }
        resource = f"/networks/{network_id}/wireless/ssids/{number}/identityPsks"

        psk = await self._api_client.run_sync(
            self._api_client.dashboard.wireless._session.post,
            metadata,
            resource,
            payload,
        )
        validated = validate_response(psk)
        if not isinstance(validated, dict):
            _LOGGER.warning("create_identity_psk did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def delete_identity_psk(
        self,
        network_id: str,
        number: str,
        identity_psk_id: str,
    ) -> None:
        """
        Delete an Identity PSK.

        Args:
        ----
            network_id: The ID of the network.
            number: The SSID number.
            identity_psk_id: The ID of the Identity PSK to delete.

        """
        if self._api_client.dashboard is None:
            return
        await self._api_client.run_sync(
            self._api_client.dashboard.wireless.deleteNetworkWirelessSsidIdentityPsk,
            networkId=network_id,
            number=number,
            identityPskId=identity_psk_id,
        )

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
        rules = await self._api_client.run_sync(
            self._api_client.dashboard.wireless.updateNetworkWirelessSsidL7FirewallRules,
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
