"""Device data coordinator for the Meraki Home Assistant integration.

This module defines `MerakiDeviceCoordinator`, which is responsible
for fetching device-specific information from the Meraki API,
processing it, and ensuring devices are correctly registered in the
Home Assistant device registry.
"""
import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional  # Added List, Optional

from homeassistant.config_entries import ConfigEntry  # For self.config_entry hint
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..const import DOMAIN  # Assuming DOMAIN is defined
# Import the mapping function for device types
from .meraki_device_types import map_meraki_model_to_device_type

_LOGGER = logging.getLogger(__name__)

# Define MERAKI_API_URL if it's not available from const.py or
# another central place
MERAKI_API_BASE_URL = "https://api.meraki.com/api/v1"


class MerakiDeviceCoordinator(DataUpdateCoordinator[Dict[str, List[Dict[str, Any]]]]):
    """Coordinator to fetch and manage device data from the Meraki API.

    This coordinator handles fetching all devices across all networks
    within an organization, enriching device data (e.g., client counts
    for APs), and registering/updating these devices in the Home
    Assistant device registry.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        device_name_format: str,
        config_entry: ConfigEntry,  # Added config_entry for device registry
    ) -> None:
        """Initialize the Meraki device coordinator.

        Args:
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            org_id: The Meraki Organization ID.
            scan_interval: The interval at which to update device data.
            device_name_format: The format string for device names (e.g.,
                "prefix", "suffix", "omitted").
            config_entry: The config entry associated with this
                coordinator, used for device registry operations.
        """
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} Devices ({org_id})",  # More specific name
            update_interval=scan_interval,
        )
        self.api_key: str = api_key
        self.org_id: str = org_id
        self.device_name_format: str = device_name_format
        # Stored by superclass as update_interval
        # self.scan_interval: timedelta = scan_interval
        self.config_entry: ConfigEntry = config_entry
        # Ensure self.data is initialized as per DataUpdateCoordinator's
        # generic type
        self.data: Dict[str, List[Dict[str, Any]]] = {"devices": []}

    async def _async_update_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch, process, and register device data from the Meraki API.

        Retrieves all networks for the organization, then fetches devices
        for each. For wireless APs (MR/GR models), it also fetches the
        count of connected clients. Finally, it ensures each device is
        correctly represented in the Home Assistant device registry.

        Returns:
            A dictionary containing a list of processed device data,
            e.g., `{"devices": [...]}`.

        Raises:
            UpdateFailed: If there's a critical error in fetching data or
                interacting with the device registry that prevents an update.
        """
        device_registry = dr.async_get(self.hass)
        # Local import to avoid potential circular dependencies at module
        # load time. MerakiApiDataFetcher is quite central; ensure its
        # definition is stable.
        from .api_data_fetcher import MerakiApiDataFetcher, MerakiApiError

        # The api_fetcher instance in MerakiDeviceCoordinator seems to be
        # used for direct _fetch_data calls rather than its higher-level
        # methods. The second argument to MerakiApiDataFetcher was 'self'
        # (the coordinator), which is unusual. It should typically be
        # org_id or specific coordinators.
        # Assuming it needs api_key and org_id for its operations.
        api_fetcher = MerakiApiDataFetcher(
            api_key=self.api_key, org_id=self.org_id
        )

        try:
            _LOGGER.debug(
                "Fetching all networks for organization: %s", self.org_id
            )
            networks_url = (
                f"{MERAKI_API_BASE_URL}/organizations/{self.org_id}/networks"
            )
            networks: Optional[
                List[Dict[str, Any]]
            ] = await api_fetcher._fetch_data(networks_url)

            all_devices_raw: List[Dict[str, Any]] = []
            if networks:
                for network in networks:
                    network_id = network.get("id")
                    if not network_id:
                        _LOGGER.warning(
                            "Network found without an ID: %s", network
                        )
                        continue
                    _LOGGER.debug(
                        "Fetching devices for network ID: %s (Name: %s)",
                        network_id,
                        network.get("name", "N/A"),
                    )
                    device_url = (
                        f"{MERAKI_API_BASE_URL}/networks/{network_id}/devices"
                    )
                    try:
                        network_devices: Optional[
                            List[Dict[str, Any]]
                        ] = await api_fetcher._fetch_data(device_url)
                        if network_devices:
                            all_devices_raw.extend(network_devices)
                        else:
                            # Changed to debug as it can be normal for some
                            # networks
                            _LOGGER.debug(
                                "No devices found in network %s, or failed to fetch.",
                                network_id,
                            )
                    except MerakiApiError as e:
                        _LOGGER.warning(
                            "Failed to fetch devices from network %s: %s",
                            network_id,
                            e,
                        )
            else:
                _LOGGER.warning(
                    "No networks found for organization %s, cannot fetch devices.",
                    self.org_id,
                )

            _LOGGER.debug(
                "Total raw devices fetched for org %s: %d",
                self.org_id,
                len(all_devices_raw),
            )

            processed_devices_list: List[Dict[str, Any]] = []
            for device_raw in all_devices_raw:
                serial = device_raw.get("serial")
                if not serial:
                    _LOGGER.warning(
                        "Device found without serial number: %s", device_raw
                    )
                    continue

                # Basic processing: ensure no None keys if possible, though
                # API should be consistent. Original code to filter None keys
                # is generally not necessary if device_raw from json.loads().
                # Copying to avoid modifying the raw dict.
                device_processed = device_raw.copy()

                # Enrich MR/GR (Access Point) devices with client count
                model = device_processed.get("model", "")
                if isinstance(model, str) and (
                    model.upper().startswith("MR")
                    or model.upper().startswith("GR")
                ):
                    network_id = device_processed.get("networkId")
                    if network_id:
                        try:
                            # Using device serial to fetch clients connected
                            # to this specific AP
                            clients_url = (
                                f"{MERAKI_API_BASE_URL}/networks/{network_id}"
                                f"/clients?perPage=1000&timespan=86400"
                                f"&serials[]={serial}"
                            )
                            _LOGGER.debug(
                                "Fetching clients for AP %s (Serial: %s) in network %s",
                                device_processed.get("name", serial),
                                serial,
                                network_id,
                            )
                            clients_data: Optional[
                                List[Dict[str, Any]]
                            ] = await api_fetcher._fetch_data(clients_url)

                            # API with `serials[]` param should ideally return
                            # only clients for that serial. If not, further
                            # filtering might be needed. Assuming API returns
                            # relevant clients.
                            device_processed["connected_clients"] = (
                                len(clients_data) if clients_data else 0
                            )
                        except MerakiApiError as e:
                            _LOGGER.warning(
                                "Failed to fetch clients for AP %s (Serial: %s): %s. "
                                "Setting client count to 0.",
                                device_processed.get("name", serial),
                                serial,
                                e,
                            )
                            device_processed["connected_clients"] = 0
                        except Exception as e:  # pylint: disable=broad-except
                            _LOGGER.exception(
                                "Unexpected error fetching clients for AP %s "
                                "(Serial: %s): %s. Setting client count to 0.",
                                device_processed.get("name", serial),
                                serial,
                                e,
                            )
                            device_processed["connected_clients"] = 0
                    else:
                        _LOGGER.warning(
                            "Cannot fetch clients for AP %s (Serial: %s) "
                            "due to missing networkId.",
                            device_processed.get("name", serial),
                            serial,
                        )
                        device_processed["connected_clients"] = 0
                else:
                    # For non-AP devices, connected_clients might not be
                    # applicable or is 0
                    device_processed["connected_clients"] = 0

                processed_devices_list.append(device_processed)

                # Register/Update device in Home Assistant Device Registry
                device_model = device_processed.get("model", "Unknown")
                # Fallback to serial if name is missing
                device_name_raw = device_processed.get("name", serial)

                device_type_mapped = map_meraki_model_to_device_type(
                    device_model
                )
                formatted_device_name = device_name_raw  # Default

                if self.device_name_format == "prefix" and device_type_mapped:
                    formatted_device_name = (
                        f"[{device_type_mapped}] {device_name_raw}"
                    )
                elif self.device_name_format == "suffix" and device_type_mapped:
                    formatted_device_name = (
                        f"{device_name_raw} [{device_type_mapped}]"
                    )
                # If "omitted" or no type mapped, name remains as is.

                device_registry.async_get_or_create(
                    config_entry_id=self.config_entry.entry_id,
                    identifiers={(DOMAIN, serial)},
                    manufacturer="Cisco Meraki",  # Standardized manufacturer
                    model=device_model,
                    name=str(formatted_device_name),  # Ensure name is string
                    # Ensure sw_version is string
                    sw_version=str(device_processed.get("firmware", "")),
                )
                _LOGGER.debug(
                    "Device %s (Serial: %s, Model: %s) processed and "
                    "registered/updated.",
                    formatted_device_name,
                    serial,
                    device_model,
                )
            self.data = {"devices": processed_devices_list}
            return self.data

        except MerakiApiError as e:
            _LOGGER.error("Meraki API error updating device data: %s", e)
            raise UpdateFailed(
                f"Meraki API error updating device data: {e}"
            ) from e
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected error updating device data: %s", e)
            raise UpdateFailed(
                f"Unexpected error updating device data: {e}"
            ) from e
