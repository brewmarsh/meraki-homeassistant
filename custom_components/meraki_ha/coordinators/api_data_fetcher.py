"""API Data Fetcher for the Meraki Home Assistant integration.

This module provides the `MerakiApiDataFetcher` class, responsible for
making API calls to the Meraki Dashboard API to retrieve information
about networks, devices (including tags), SSIDs, and device-specific details
like client counts and radio settings for MR devices, using the Meraki SDK.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import UpdateFailed
from meraki.exceptions import APIError as MerakiSDKAPIError

from custom_components.meraki_ha.meraki_api import MerakiAPIClient

# Obsolete imports for MerakiApiException and related custom exceptions are removed
# as MerakiSDKAPIError from meraki.exceptions is used directly.

_LOGGER = logging.getLogger(__name__)

# MERAKI_API_URL is no longer needed as SDK handles URLs.
# Custom exceptions like MerakiApiError, MerakiApiConnectionError, etc.,
# are replaced by meraki.exceptions.APIError or handled directly.


class MerakiApiDataFetcher:
    """Class to fetch data from the Meraki API using the Meraki SDK.

    This class handles communication with the Meraki API to retrieve
    networks, devices (with tags), SSIDs, and for MR devices, client counts
    and radio settings. It uses an instance of `MerakiAPIClient` for all
    API interactions.
    """

    def __init__(
        self,
        meraki_client: MerakiAPIClient,
    ) -> None:
        """Initialize the MerakiApiDataFetcher.

        Args:
            meraki_client: An instance of the SDK-based `MerakiAPIClient`.
        """
        self.meraki_client: MerakiAPIClient = meraki_client
        self.org_id: str = meraki_client.org_id  # Organization ID from the client

    async def fetch_all_data(
        self,
        hass: HomeAssistant,  # pylint: disable=unused-argument
        # hass is retained for potential future use or context.
        # Other parameters like org_id, scan_interval, device_name_format
        # are no longer passed here as org_id comes from self.org_id
        # and others are not directly used in this method's revised logic.
    ) -> Dict[str, Any]:
        """Fetch all necessary data from the Meraki API for the organization.

        This method orchestrates calls to retrieve networks, devices (including their tags),
        SSIDs. For MR (wireless access point) devices, it additionally fetches the
        connected client count and wireless radio settings using concurrent tasks.

        Args:
            hass: The Home Assistant instance (currently unused but common pattern).

        Returns:
            A dictionary containing lists of devices, networks, and SSIDs.
            Example: `{"devices": [...], "networks": [...], "ssids": [...]}`.
            The 'devices' list includes tags, and for MR devices, it also includes
            `connected_clients_count` and `radio_settings`.

        Raises:
            UpdateFailed: If essential data like networks or devices cannot
                          be fetched after retries/error handling within helper methods,
                          preventing a meaningful update.
            MerakiSDKAPIError: For underlying API communication issues from the SDK
                               that are not handled by individual fetch methods and
                               escalate to this level.
        """
        _LOGGER.debug(
            "Fetching all data for organization ID: %s using SDK", self.org_id
        )

        # Step 1: Fetch all networks for the organization.
        # `async_get_networks` handles its own exceptions and returns None on failure.
        networks: Optional[List[Dict[str, Any]]] = None
        try:
            networks = await self.async_get_networks(self.org_id)
        except (
            MerakiSDKAPIError
        ) as e:  # Should be caught by async_get_networks, but as a safeguard
            _LOGGER.error(
                "Critical error fetching networks for org %s: %s. "
                "This should have been handled by async_get_networks.",
                self.org_id,
                e,
            )
            # networks remains None

        if networks is None:
            _LOGGER.error(
                "Could not fetch Meraki networks for org ID: %s. Aborting update.",
                self.org_id,
            )
            raise UpdateFailed(
                f"Could not fetch Meraki networks for org {self.org_id}."
            )

        # Step 2: Fetch all devices for the organization.
        # `async_get_organization_devices` handles its own exceptions.
        devices: Optional[List[Dict[str, Any]]] = None
        try:
            devices = await self.async_get_organization_devices(self.org_id)
        except MerakiSDKAPIError as e:  # Safeguard
            _LOGGER.error(
                "Critical error fetching devices for org %s: %s. "
                "This should have been handled by async_get_organization_devices.",
                self.org_id,
                e,
            )
            # devices remains None

        if devices is None:
            _LOGGER.error(
                "Could not fetch Meraki devices for org ID: %s. Aborting update.",
                self.org_id,
            )
            raise UpdateFailed(f"Could not fetch Meraki devices for org {self.org_id}.")

        # Step 2.1: Fetch Device Statuses
        device_statuses_map = {}
        if devices:  # Only fetch statuses if we have devices
            try:
                _LOGGER.debug(
                    "MERAKI_DEBUG_FETCHER: Fetching device statuses for org ID: %s",
                    self.org_id,
                )
                statuses_data = await self.meraki_client.organizations.getOrganizationDevicesStatuses(
                    organizationId=self.org_id, total_pages="all"
                )
                if statuses_data:
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: Received %d status entries.",
                        len(statuses_data),
                    )
                    for status_entry in statuses_data:
                        if status_entry.get("serial"):
                            device_statuses_map[status_entry["serial"]] = status_entry
                else:
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: No status data returned from getOrganizationDeviceStatuses."
                    )
            except MerakiSDKAPIError as e:
                _LOGGER.warning(
                    "MERAKI_DEBUG_FETCHER: SDK API error fetching device statuses for org %s: "
                    "Status %s, Reason: %s. Device statuses may be incomplete.",
                    self.org_id,
                    e.status,
                    e.reason,
                )
            except Exception as e:
                _LOGGER.exception(
                    "MERAKI_DEBUG_FETCHER: Unexpected error fetching device statuses for org %s: %s. "
                    "Device statuses may be incomplete.",
                    self.org_id,
                    e,
                )

        # Step 2.2: Merge Statuses into Devices
        if devices and device_statuses_map:
            for device in devices:
                serial = device.get("serial")
                if serial and serial in device_statuses_map:
                    status_update_data = device_statuses_map[serial]
                    original_product_type = device.get("productType") 

                    device.update(status_update_data)

                    current_product_type_after_merge = device.get("productType")
                    status_provided_product_type = status_update_data.get("productType")

                    if current_product_type_after_merge is None and original_product_type is not None:
                        _LOGGER.debug(
                            "MERAKI_DEBUG_FETCHER: Restoring original productType '%s' for device %s (Serial: %s) "
                            "as status update data had productType: %s (Type: %s).",
                            original_product_type,
                            device.get('name', 'Unknown'),
                            serial,
                            status_provided_product_type,
                            type(status_provided_product_type).__name__
                        )
                        device["productType"] = original_product_type
                    elif original_product_type is not None and \
                         status_provided_product_type is not None and \
                         original_product_type != status_provided_product_type:
                        _LOGGER.warning(
                            "MERAKI_DEBUG_FETCHER: productType for device %s (Serial: %s) was changed from '%s' to '%s' "
                            "by status update data. This is unexpected if original was valid. Using new value from status.",
                            device.get('name', 'Unknown'),
                            serial,
                            original_product_type,
                            current_product_type_after_merge
                        )
                elif serial:
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: No specific status entry found for device %s. It may retain a prior status or have none.",
                        serial,
                    )
        elif devices:
            _LOGGER.debug(
                "MERAKI_DEBUG_FETCHER: No device statuses were successfully mapped, skipping merge."
            )
        
        firmware_upgrade_data = {}
        _LOGGER.debug(
            "MERAKI_DEBUG_FETCHER: Fetching firmware upgrade data for org ID: %s",
            self.org_id,
        )
        try:
            firmware_upgrade_data = await self.meraki_client.organizations.getOrganizationFirmwareUpgrades(
                organizationId=self.org_id
            )
            _LOGGER.debug(
                "MERAKI_DEBUG_FETCHER: Successfully fetched firmware upgrade data." 
            )
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "MERAKI_DEBUG_FETCHER: SDK API error fetching firmware upgrade data for org %s: "
                "Status %s, Reason: %s. Firmware data may be incomplete.",
                self.org_id,
                e.status,
                e.reason,
            )
            firmware_upgrade_data = {} 
        except Exception as e:
            _LOGGER.exception(
                "MERAKI_DEBUG_FETCHER: Unexpected error fetching firmware upgrade data for org %s: %s. "
                "Firmware data may be incomplete.",
                self.org_id,
                e,
            )
            firmware_upgrade_data = {} 

        additional_device_detail_tasks = []
        if devices:
            for device in devices:
                device_model_upper = device.get("model", "").upper()
                serial = device.get("serial") 

                if not serial: 
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: Device %s (MAC: %s) has no serial, skipping additional detail tasks.",
                        device.get("name", "N/A"),
                        device.get("mac", "N/A"),
                    )
                    continue

                if device_model_upper.startswith("MR"):
                    additional_device_detail_tasks.append(
                        self._async_get_mr_device_details(device, serial)
                    )
                elif device_model_upper.startswith("MX"):
                    additional_device_detail_tasks.append(
                        self._async_get_mx_device_uplink_settings(device, self.meraki_client)
                    )
                    additional_device_detail_tasks.append(
                        self._async_get_mx_lan_dns_settings(device, self.meraki_client)
                    )

        if additional_device_detail_tasks:
            await asyncio.gather(*additional_device_detail_tasks)

        if devices: 
            if not isinstance(firmware_upgrade_data, list):
                _LOGGER.warning(
                    "MERAKI_DEBUG_FETCHER: firmware_upgrade_data is not a list (type: %s), "
                    "cannot process firmware status for devices. Value: %s",
                    type(firmware_upgrade_data).__name__,
                    str(firmware_upgrade_data)[:200] 
                )
                for device in devices:
                    device["firmware_up_to_date"] = False
                    device["latest_firmware_version"] = device.get("firmware", "N/A")
            elif not firmware_upgrade_data:
                _LOGGER.debug(
                    "MERAKI_DEBUG_FETCHER: firmware_upgrade_data is an empty list. "
                    "No specific upgrade information available."
                )
                for device in devices:
                    device["firmware_up_to_date"] = True 
                    device["latest_firmware_version"] = device.get("firmware", "N/A")
            else:
                _LOGGER.debug("MERAKI_DEBUG_FETCHER: Starting to process firmware data list for devices.")
                if _LOGGER.isEnabledFor(logging.DEBUG): 
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: Sample firmware_upgrade_data item: %s",
                        str(firmware_upgrade_data[0])[:300] 
                    )

                for device in devices:
                    device_serial = device.get("serial")
                    device_model = device.get("model", "")
                    current_device_firmware = device.get("firmware")
                    is_up_to_date_bool = False 
                    latest_known_version = current_device_firmware if current_device_firmware else "N/A"
                    found_specific_info_for_device = False

                    for upgrade_item in firmware_upgrade_data:
                        if not isinstance(upgrade_item, dict):
                            _LOGGER.warning(
                                "MERAKI_DEBUG_FETCHER: Skipping non-dictionary item in firmware_upgrade_data list: %s",
                                str(upgrade_item)[:200]
                            )
                            continue
                        item_serial = upgrade_item.get("serial")
                        if item_serial and item_serial == device_serial:
                            _LOGGER.debug("MERAKI_DEBUG_FETCHER: Found firmware info by serial for %s", device_serial)
                            next_upgrade_info = upgrade_item.get("nextUpgrade")
                            if isinstance(next_upgrade_info, dict):
                                to_version_info = next_upgrade_info.get("toVersion")
                                if isinstance(to_version_info, dict):
                                    latest_known_version = to_version_info.get("version", latest_known_version)
                                    is_up_to_date_bool = False 
                                else: 
                                    item_status = str(upgrade_item.get("status", "")).lower()
                                    if item_status == "up-to-date":
                                        is_up_to_date_bool = True
                                        latest_known_version = current_device_firmware if current_device_firmware else "N/A"
                                    elif item_status == "has-newer-stable-version":
                                        is_up_to_date_bool = False
                                        available_versions = upgrade_item.get("availableVersions")
                                        if isinstance(available_versions, list) and available_versions:
                                            latest_known_version = available_versions[0].get("version", latest_known_version)
                            else: 
                                item_status = str(upgrade_item.get("status", "")).lower()
                                if item_status == "up-to-date":
                                    is_up_to_date_bool = True
                                    latest_known_version = current_device_firmware if current_device_firmware else "N/A"
                                elif upgrade_item.get("latestVersion"): 
                                     latest_known_version = upgrade_item.get("latestVersion")
                            if current_device_firmware and current_device_firmware == latest_known_version:
                                is_up_to_date_bool = True
                            found_specific_info_for_device = True
                            break 
                    if not found_specific_info_for_device and not firmware_upgrade_data: 
                        is_up_to_date_bool = True
                        latest_known_version = current_device_firmware if current_device_firmware else "N/A"
                    elif not found_specific_info_for_device:
                        _LOGGER.debug("MERAKI_DEBUG_FETCHER: No specific firmware upgrade info found for device %s by serial.", device_serial)
                        if current_device_firmware:
                            is_up_to_date_bool = (current_device_firmware == latest_known_version)
                    device["firmware_up_to_date"] = is_up_to_date_bool
                    device["latest_firmware_version"] = latest_known_version
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: Device %s (Model: %s, Current FW: %s): Up-to-date: %s, Latest Known: %s",
                        device_serial, device_model, current_device_firmware, is_up_to_date_bool, latest_known_version,
                    )
        else: 
            _LOGGER.debug("MERAKI_DEBUG_FETCHER: No devices available to process firmware data for.")

        ssids: List[Dict[str, Any]] = []
        for network in networks: 
            network_id: str = network["id"]  
            try:
                _LOGGER.debug("Fetching SSIDs for network ID: %s", network_id)
                ssid_data_for_network = None 
                try:
                    ssid_data_for_network = await self.async_get_network_ssids(network_id)
                except MerakiSDKAPIError as e: 
                    _LOGGER.warning(
                        "Error fetching SSIDs for network %s was not handled by async_get_network_ssids: %s. Status: %s, Reason: %s. Skipping.",
                        network_id, e, e.status, e.reason,
                    )
                if ssid_data_for_network:
                    for ssid_obj in ssid_data_for_network:
                        if isinstance(ssid_obj, dict):
                            if ssid_obj.get("networkId") is None: 
                                ssid_obj["networkId"] = network_id
                                _LOGGER.debug(f"Added/updated networkId '{network_id}' for SSID '{ssid_obj.get('name')}' (Number: {ssid_obj.get('number')})")
                        else:
                            _LOGGER.warning(f"Found non-dict item in ssid_data_for_network: {ssid_obj}")
                    ssids.extend(ssid_data_for_network)
                elif ssid_data_for_network is None:
                    _LOGGER.info(
                        "SSID data result was None for network %s, SSIDs for this network will be skipped.",
                        network_id,
                    )
            except Exception as e: 
                _LOGGER.exception(
                    "Unexpected error processing network %s for SSID data: %s. Skipping this network's SSIDs.",
                    network_id, e,
                )
        all_clients: List[Dict[str, Any]] = []
        if networks: 
            for network in networks:
                network_id = network["id"]
                try:
                    _LOGGER.debug("Fetching clients for network ID: %s", network_id)
                    network_clients_data = (
                        await self.meraki_client.networks.getNetworkClients(
                            network_id, timespan=300 
                        )
                    )
                    if network_clients_data:
                        for client_data in network_clients_data:
                            ap_serial = (
                                client_data.get("recentDeviceSerial")
                                or client_data.get("recentDeviceMac")
                                or client_data.get("deviceSerial")
                            ) 
                            client_entry = {
                                "mac": client_data["mac"], "ip": client_data.get("ip"),
                                "description": client_data.get("description"),
                                "status": client_data.get("status", "Online"),
                                "networkId": network_id, "ap_serial": ap_serial,
                                "usage": client_data.get("usage"), "vlan": client_data.get("vlan"),
                                "switchport": client_data.get("switchport"), "ip6": client_data.get("ip6"),
                                "manufacturer": client_data.get("manufacturer"), "os": client_data.get("os"),
                                "user": client_data.get("user"), "firstSeen": client_data.get("firstSeen"),
                                "lastSeen": client_data.get("lastSeen"), "ssid": client_data.get("ssid"),
                            }
                            all_clients.append(client_entry)
                        _LOGGER.debug(
                            "Fetched %d clients for network %s", len(network_clients_data), network_id,
                        )
                    else:
                        _LOGGER.debug(
                            "No clients found for network %s in the given timespan.", network_id,
                        )
                except MerakiSDKAPIError as e:
                    _LOGGER.warning(
                        "Meraki SDK API error fetching clients for network %s: %s. Status: %s, Reason: %s. Skipping this network's clients.",
                        network_id, e, e.status, e.reason,
                    )
                except Exception as e: 
                    _LOGGER.exception(
                        "Unexpected error fetching clients for network %s: %s. Skipping this network's clients.",
                        network_id, e,
                    )
        else:
            _LOGGER.warning("No networks available to fetch clients from.")
        return {
            "devices": devices, "networks": networks, "ssids": ssids, "clients": all_clients,
        }

    async def _async_get_mr_device_details(
        self, device: Dict[str, Any], serial: str
    ) -> None:
        """Asynchronously fetch and store client count and radio settings for an MR device."""
        try:
            clients_data = await self.meraki_client.devices.getDeviceClients(serial=serial)
            device["connected_clients_count"] = len(clients_data) if clients_data else 0
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "Failed to fetch client count for MR device %s (Serial: %s): API Error %s - %s. Setting client count to 0.",
                device.get("name", "Unknown"), serial, e.status, e.reason,
            )
            device["connected_clients_count"] = 0
        except Exception as e: 
            _LOGGER.exception(
                "Unexpected error fetching client count for MR device %s (Serial: %s): %s. Setting client count to 0.",
                device.get("name", "Unknown"), serial, e,
            )
            device["connected_clients_count"] = 0
        try:
            radio_settings = await self.meraki_client.wireless.getDeviceWirelessRadioSettings(serial=serial)
            device["radio_settings"] = radio_settings
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "Failed to fetch radio settings for MR device %s (Serial: %s): API Error %s - %s. Setting radio settings to None.",
                device.get("name", "Unknown"), serial, e.status, e.reason,
            )
            device["radio_settings"] = None
        except Exception as e: 
            _LOGGER.exception(
                "Unexpected error fetching radio settings for MR device %s (Serial: %s): %s. Setting radio settings to None.",
                device.get("name", "Unknown"), serial, e,
            )
            device["radio_settings"] = None

    async def async_get_networks(self, org_id: str) -> Optional[List[Dict[str, Any]]]:
        """Fetch all networks for a Meraki organization using the SDK."""
        _LOGGER.debug("Fetching networks for org ID: %s using SDK", org_id)
        try:
            _LOGGER.debug("Executing async_get_networks with organizations.getOrganizationNetworks(organizationId=%s).", org_id)
            org_networks = await self.meraki_client.organizations.getOrganizationNetworks(organizationId=org_id)
            if org_networks is None: 
                _LOGGER.warning("Call to organizations.getOrganizationNetworks for org ID %s returned None.", org_id)
                return None
            if not org_networks:
                _LOGGER.warning("No networks found for organization ID %s using organizations.getOrganizationNetworks.", org_id)
                return None
            _LOGGER.debug("Successfully fetched %d networks for org ID %s using organizations.getOrganizationNetworks.", len(org_networks), org_id)
            return org_networks
        except MerakiSDKAPIError as e:
            _LOGGER.warning("SDK API error during getNetworks or filtering for org %s: Status %s, Reason: %s. Returning None.", org_id, e.status, e.reason)
            return None
        except Exception as e: 
            _LOGGER.exception("Unexpected error during getNetworks or filtering for org %s: %s. Returning None.", org_id, e)
            return None

    async def async_get_organization_devices(
        self, org_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Get all devices in the Meraki organization using the SDK."""
        _LOGGER.debug("MERAKI_DEBUG_FETCHER: Fetching organization devices for org ID: %s using SDK", org_id)
        try:
            devices_data = await self.meraki_client.organizations.getOrganizationDevices(org_id)
            if devices_data:
                _LOGGER.debug("MERAKI_DEBUG_FETCHER: Received %d devices from SDK.", len(devices_data))
            else:
                _LOGGER.debug("MERAKI_DEBUG_FETCHER: Received no devices_data from SDK (None or empty list).")
            return devices_data
        except MerakiSDKAPIError as e:
            _LOGGER.warning("MERAKI_DEBUG_FETCHER: SDK API error fetching devices for org %s: Status %s, Reason: %s. Returning None.", org_id, e.status, e.reason)
            return None
        except Exception as e: 
            _LOGGER.exception("MERAKI_DEBUG_FETCHER: Unexpected error fetching devices for org %s: %s. Returning None.", org_id, e)
            return None

    async def async_get_network_ssids(
        self, network_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch all SSIDs for a specific Meraki network using the SDK."""
        _LOGGER.debug("Fetching SSIDs for network ID: %s using SDK", network_id)
        try:
            return await self.meraki_client.wireless.getNetworkWirelessSsids(networkId=network_id)
        except MerakiSDKAPIError as e:
            if e.status == 404:
                _LOGGER.info("SSID resource not found for network %s (likely no wireless capabilities or SSIDs configured). Returning empty list.", network_id)
                return [] 
            _LOGGER.warning("SDK API error fetching SSIDs for network %s: Status %s, Reason: %s. Returning None for this network's SSIDs.", network_id, e.status, e.reason)
            return None
        except Exception as e: 
            _LOGGER.exception("Unexpected error fetching SSIDs for network %s: %s. Returning None.", network_id, e)
            return None

    async def _async_get_mx_device_uplink_settings(
        self, device: Dict[str, Any], client: MerakiAPIClient
    ) -> None:
        """Asynchronously fetch and store uplink settings for an MX device."""
        serial = device.get("serial")
        if not serial:
            _LOGGER.warning("MERAKI_DEBUG_FETCHER: Cannot fetch uplink settings for MX device %s: missing serial.", device.get("name", "Unknown"))
            return

        _LOGGER.debug("MERAKI_DEBUG_FETCHER: Fetching uplink settings for MX device %s (Serial: %s)", device.get("name", "Unknown"), serial)
        
        # Initialize DNS server lists for the device to ensure they always exist
        device["wan1_dns_servers"] = []
        device["wan2_dns_servers"] = []
        # Add other WANs here if needed, e.g., device["wan3_dns_servers"] = []

        try:
            uplink_settings = await client.appliance.getDeviceApplianceUplinksSettings(serial=serial)
            _LOGGER.debug("MERAKI_DEBUG_FETCHER: Raw uplink settings for %s: %s", serial, uplink_settings)

            if uplink_settings:
                interfaces = uplink_settings.get("interfaces", {})
                wan_interface_keys = ["wan1", "wan2"] 

                for interface_name in wan_interface_keys:
                    current_wan_dns_ips = []
                    interface_settings = interfaces.get(interface_name, {})

                    if interface_settings:
                        svis_data = interface_settings.get("svis")
                        if isinstance(svis_data, dict): 
                            ipv4_data = svis_data.get("ipv4")
                            if isinstance(ipv4_data, dict):
                                nameservers_list = ipv4_data.get("nameservers")
                                if isinstance(nameservers_list, list):
                                    for ns_entry in nameservers_list:
                                        if isinstance(ns_entry, dict) and isinstance(ns_entry.get("addresses"), list):
                                            for ip_addr in ns_entry.get("addresses", []):
                                                if isinstance(ip_addr, str) and ip_addr not in current_wan_dns_ips:
                                                    current_wan_dns_ips.append(ip_addr)
                        
                        if not current_wan_dns_ips: 
                            dns_servers_field = interface_settings.get("dnsServers") 
                            if isinstance(dns_servers_field, list):
                                for dns_entry in dns_servers_field:
                                    if isinstance(dns_entry, str):
                                        if '.' in dns_entry or ':' in dns_entry: 
                                            if dns_entry not in current_wan_dns_ips:
                                                current_wan_dns_ips.append(dns_entry)
                            elif isinstance(dns_servers_field, str): 
                                if '.' in dns_servers_field or ':' in dns_servers_field:
                                     if dns_servers_field not in current_wan_dns_ips:
                                        current_wan_dns_ips.append(dns_servers_field)

                    if not current_wan_dns_ips:
                        primary_dns_key = f"{interface_name}PrimaryDns" 
                        secondary_dns_key = f"{interface_name}SecondaryDns" 
                        primary_dns = device.get(primary_dns_key)
                        if primary_dns and isinstance(primary_dns, str) and primary_dns not in current_wan_dns_ips:
                            current_wan_dns_ips.append(primary_dns)
                        secondary_dns = device.get(secondary_dns_key)
                        if secondary_dns and isinstance(secondary_dns, str) and secondary_dns not in current_wan_dns_ips:
                            current_wan_dns_ips.append(secondary_dns)
                    
                    device[f"{interface_name}_dns_servers"] = current_wan_dns_ips
                    _LOGGER.debug(
                        "MERAKI_DEBUG_FETCHER: Populated %s_dns_servers for %s: %s",
                        interface_name, serial, device[f"{interface_name}_dns_servers"]
                    )
            else: 
                _LOGGER.debug(
                    "MERAKI_DEBUG_FETCHER: No uplink settings data returned for MX device %s (Serial: %s). "
                    "DNS server lists will remain default (empty or from device status).",
                    device.get("name", "Unknown"), serial,
                )
        except MerakiSDKAPIError as e:
            _LOGGER.warning(
                "MERAKI_DEBUG_FETCHER: Failed to fetch uplink settings for MX device %s (Serial: %s): "
                "API Error %s - %s. DNS server info will be unavailable.",
                device.get("name", "Unknown"), serial, e.status, e.reason,
            )
            # Defaults are already set at the beginning of the try block
        except Exception as e:  
            _LOGGER.exception(
                "MERAKI_DEBUG_FETCHER: Unexpected error fetching uplink settings for MX device %s (Serial: %s): %s. "
                "DNS server info will be unavailable.",
                device.get("name", "Unknown"), serial, e,
            )
            # Defaults are already set

    async def _async_get_mx_lan_dns_settings(
        self, device: Dict[str, Any], client: MerakiAPIClient
    ) -> None:
        """Asynchronously fetch and store LAN DNS settings for an MX device's VLANs."""
        network_id = device.get("networkId")
        serial = device.get("serial", "N/A") 
        device_name = device.get("name", "Unknown")

        if not network_id:
            _LOGGER.debug(
                "MERAKI_DEBUG_FETCHER: Cannot fetch LAN DNS settings for MX device %s (Serial: %s): missing networkId.",
                device_name, serial,
            )
            device["lan_dns_settings"] = {} 
            return

        _LOGGER.debug(
            "MERAKI_DEBUG_FETCHER: Fetching LAN DNS (VLAN settings) for MX device %s (Serial: %s, Network: %s)",
            device_name, serial, network_id,
        )
        
        lan_dns_by_vlan: Dict[str, Any] = {}
        try:
            vlan_settings_list = await client.appliance.getNetworkApplianceVlansSettings(networkId=network_id)

            if vlan_settings_list and isinstance(vlan_settings_list, list):
                _LOGGER.debug("MERAKI_DEBUG_FETCHER: Received %d VLAN entries for network %s.", len(vlan_settings_list), network_id)
                for vlan_data in vlan_settings_list:
                    if not isinstance(vlan_data, dict):
                        _LOGGER.warning("Skipping non-dictionary item in VLAN settings list for network %s: %s", network_id, vlan_data)
                        continue
                    vlan_id = vlan_data.get("id")
                    vlan_name = vlan_data.get("name", "Unnamed VLAN")
                    dns_nameservers_setting = vlan_data.get("dnsNameservers")
                    custom_dns_servers = vlan_data.get("customDnsServers", [])
                    vlan_key = f"VLAN {vlan_id} ({vlan_name})"

                    if dns_nameservers_setting == "custom_servers":
                        if custom_dns_servers:
                            lan_dns_by_vlan[vlan_key] = custom_dns_servers
                            _LOGGER.debug("MERAKI_DEBUG_FETCHER: VLAN %s on %s using custom DNS: %s", vlan_key, serial, custom_dns_servers)
                        else:
                            lan_dns_by_vlan[vlan_key] = [] 
                            _LOGGER.debug("MERAKI_DEBUG_FETCHER: VLAN %s on %s set to 'custom_servers' but no IPs provided.", vlan_key, serial)
                    elif dns_nameservers_setting:
                        lan_dns_by_vlan[vlan_key] = dns_nameservers_setting 
                        _LOGGER.debug("MERAKI_DEBUG_FETCHER: VLAN %s on %s using preset DNS: %s", vlan_key, serial, dns_nameservers_setting)
                    else:
                        lan_dns_by_vlan[vlan_key] = "Not configured" 
                        _LOGGER.debug("MERAKI_DEBUG_FETCHER: VLAN %s on %s has no explicit DNS configuration.", vlan_key, serial)
            elif vlan_settings_list is None: 
                 _LOGGER.debug("MERAKI_DEBUG_FETCHER: No VLANs configured or endpoint not applicable for network %s (Serial: %s).", network_id, serial)
            else: 
                _LOGGER.warning(
                    "MERAKI_DEBUG_FETCHER: Unexpected response type for VLAN settings for network %s (Serial: %s): %s",
                    network_id, serial, type(vlan_settings_list).__name__
                )
        except MerakiSDKAPIError as e:
            if e.status == 404:
                _LOGGER.debug(
                    "MERAKI_DEBUG_FETCHER: No VLAN settings found for network %s (Serial: %s) (404 Error). "
                    "This may be normal if no VLANs are configured or device is not an appliance.",
                    network_id, serial,
                )
            else:
                _LOGGER.warning(
                    "MERAKI_DEBUG_FETCHER: Failed to fetch LAN DNS settings for MX device %s (Serial: %s, Network: %s): "
                    "API Error %s - %s. LAN DNS settings will be unavailable.",
                    device_name, serial, network_id, e.status, e.reason,
                )
        except Exception as e:  
            _LOGGER.exception(
                "MERAKI_DEBUG_FETCHER: Unexpected error fetching LAN DNS settings for MX device %s (Serial: %s, Network: %s): %s. "
                "LAN DNS settings will be unavailable.",
                device_name, serial, network_id, e,
            )
        device["lan_dns_settings"] = lan_dns_by_vlan
        _LOGGER.debug("MERAKI_DEBUG_FETCHER: Final LAN DNS settings for %s (Serial: %s): %s", device_name, serial, lan_dns_by_vlan)
