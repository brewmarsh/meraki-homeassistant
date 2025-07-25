"""Base data update coordinator for the Meraki Home Assistant integration."""

import asyncio
import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from ..api.meraki_api import MerakiAPIClient, MerakiApiError
from ..const import DOMAIN, ERASE_TAGS_WARNING
from .helpers.utils import format_device_name
from .meraki_api_data_fetcher import MerakiApiDataFetcher
from .meraki_data_aggregator import MerakiDataAggregator
from .meraki_data_processor import MerakiDataProcessor
from .tag_eraser_coordinator import TagEraserCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiDataUpdateCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Manages fetching and processing of Meraki data for Home Assistant."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        org_id: str,
        scan_interval: timedelta,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki data update coordinator."""
        self.hass = hass
        self.api_key: str = api_key
        self.org_id: str = org_id
        self.config_entry: ConfigEntry = config_entry
        self.erase_tags: bool = config_entry.options.get("erase_tags", False)

        self.meraki_client = MerakiAPIClient(api_key=api_key, org_id=org_id)
        self.api_fetcher = MerakiApiDataFetcher(meraki_client=self.meraki_client)
        self.data_aggregator = MerakiDataAggregator(self)
        self.data_processor = MerakiDataProcessor(self)

        self.tag_eraser_coordinator: Optional[TagEraserCoordinator] = None
        if self.erase_tags:
            self.tag_eraser_coordinator = TagEraserCoordinator(
                hass, api_key, org_id
            )
            _LOGGER.warning(ERASE_TAGS_WARNING)

        self.device_data: List[Dict[str, Any]] = []
        self.org_name: Optional[str] = None
        self.formatted_org_display_name: Optional[str] = None
        self._is_available = True

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} (Org: {org_id})",
            update_interval=scan_interval,
        )

    @property
    def device_name_format(self) -> str:
        """Return the device name format option."""
        return self.config_entry.options.get("device_name_format", "omitted")

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch, process, and aggregate data from the Meraki API."""
        try:
            await self.meraki_client.initialize()
            all_data = await self.api_fetcher.fetch_all_data(self.hass)
        except (MerakiApiError, asyncio.TimeoutError) as e:
            if self._is_available:
                _LOGGER.error(f"Error fetching Meraki data for org {self.org_id}: {e}")
                self._is_available = False
            raise UpdateFailed(f"Failed to fetch data: {e}") from e
        except Exception as e:
            if self._is_available:
                _LOGGER.exception(f"Unexpected error fetching data for org {self.org_id}: {e}")
                self._is_available = False
            raise UpdateFailed(f"Unexpected error: {e}") from e

        if not all_data:
            raise UpdateFailed("No data received from Meraki API")

        if not self._is_available:
            _LOGGER.info(f"Connection to Meraki API restored for org {self.org_id}")
            self._is_available = True

        self.org_name = all_data.get("org_name")
        self.device_data = all_data.get("devices", [])
        await self._register_devices(all_data.get("networks", []), self.device_data)

        network_client_counts = self.data_processor.process_network_client_counts(
            all_data.get("clients", [])
        )
        combined_data = self.data_aggregator.aggregate_data(
            devices=self.device_data,
            ssids=all_data.get("ssids", []),
            networks=all_data.get("networks", []),
            clients_list=all_data.get("clients", []),
            network_client_counts=network_client_counts,
            clients_on_ssids=all_data.get("clients_on_ssids", 0),
            clients_on_appliances=all_data.get("clients_on_appliances", 0),
            clients_on_wireless=all_data.get("clients_on_wireless", 0),
        )

        self.data = combined_data
        if self.erase_tags and self.tag_eraser_coordinator:
            await self._erase_device_tags()

        await self._device_registry_cleanup()
        return self.data

    async def _register_devices(
        self, networks: List[Dict[str, Any]], devices: List[Dict[str, Any]]
    ) -> None:
        """Register networks and devices with Home Assistant."""
        device_registry = dr.async_get(self.hass)
        for network_info in networks:
            self._register_network_device(device_registry, network_info)
        for device_info in devices:
            self._register_physical_device(device_registry, device_info)

    def _register_network_device(
        self, device_registry: dr.DeviceRegistry, network_info: Dict[str, Any]
    ) -> None:
        """Register a network as a device."""
        network_id = network_info.get("id")
        if not network_id:
            _LOGGER.warning("Network with missing ID: %s", network_info)
            return

        network_name = format_device_name(
            network_info.get("name", f"Meraki Network {network_id}"),
            "Network",
            self.device_name_format,
            is_org_device=False,
        )
        device_registry.async_get_or_create(
            config_entry_id=self.config_entry.entry_id,
            identifiers={(DOMAIN, network_id)},
            name=network_name,
            model=f"Network (ID: {network_id})",
            manufacturer="Cisco Meraki",
        )

    def _register_physical_device(
        self, device_registry: dr.DeviceRegistry, device_info: Dict[str, Any]
    ) -> None:
        """Register a physical device."""
        serial = device_info.get("serial")
        if not serial:
            _LOGGER.warning("Device without serial: %s", device_info)
            return

        device_name = format_device_name(
            device_info.get("name", serial),
            device_info.get("model", "Unknown"),
            self.device_name_format,
            is_org_device=False,
        )
        mac_address = device_info.get("mac")
        connections = {(dr.CONNECTION_NETWORK_MAC, mac_address)} if mac_address else None

        device_registry.async_get_or_create(
            config_entry_id=self.config_entry.entry_id,
            identifiers={(DOMAIN, serial)},
            manufacturer="Cisco Meraki",
            model=device_info.get("model", "Unknown"),
            name=device_name,
            sw_version=device_info.get("firmware"),
            connections=connections,
        )

    async def _erase_device_tags(self) -> None:
        """Erase tags from devices if configured."""
        _LOGGER.warning("Erasing tags for org %s", self.org_id)
        for device in self.device_data:
            serial = device.get("serial")
            if serial and self.tag_eraser_coordinator:
                try:
                    await self.tag_eraser_coordinator.async_erase_device_tags(serial)
                except (MerakiApiError, asyncio.TimeoutError) as e:
                    _LOGGER.error(f"Failed to erase tags for device {serial}: {e}")
                except Exception as e:
                    _LOGGER.exception(f"Unexpected error erasing tags for {serial}: {e}")

    async def async_register_organization_device(self, hass: HomeAssistant) -> None:
        """Register the Meraki Organization as a device in Home Assistant."""
        if not self.org_id:
            _LOGGER.error("Org ID not available for device registration.")
            return

        raw_org_name = self.org_name or f"Meraki Organization {self.org_id}"
        formatted_org_name = format_device_name(
            raw_org_name, "Organization", self.device_name_format, is_org_device=True
        )
        self.formatted_org_display_name = formatted_org_name

        device_registry = dr.async_get(hass)
        device_registry.async_get_or_create(
            config_entry_id=self.config_entry.entry_id,
            identifiers={(DOMAIN, self.org_id)},
            name=formatted_org_name,
            model="Organization",
            manufacturer="Cisco Meraki",
        )
        # _LOGGER.debug(
        #     "Organization device registration attempt complete for %s.", self.org_id
        # ) # Corrected: Removed stray parenthesis here

    async def _device_registry_cleanup(self) -> None:
        """Remove stale devices from the device registry."""
        device_registry = dr.async_get(self.hass)
        current_devices = {
            (DOMAIN, device["serial"])
            for device in self.data.get("devices", [])
            if "serial" in device
        }
        for device in dr.async_entries_for_config_entry(
            device_registry, self.config_entry.entry_id
        ):
            if not any(
                identifier in current_devices for identifier in device.identifiers
            ):
                device_registry.async_remove_device(device.id)

    async def _async_shutdown(self) -> None:
        """Clean up resources when the coordinator is shut down.

        This method is called by Home Assistant when the integration or
        config entry is being unloaded. It should close any open connections,
        such as the Meraki API client session.
        """
        # Close the Meraki API client session.
        if hasattr(self, "meraki_client") and self.meraki_client:
            try:
                await self.meraki_client.close()
            except (asyncio.TimeoutError, ConnectionError) as e:
                _LOGGER.warning(
                    "Network error while closing Meraki API client session for org %s: %s",
                    self.org_id,
                    str(e),
                )
            except Exception as e:
                _LOGGER.error(
                    "Unexpected error closing Meraki API client session for org %s: %s. Error type: %s",
                    self.org_id,
                    str(e),
                    type(e).__name__,
                )

        # Call superclass shutdown for any base class cleanup.
        await super()._async_shutdown()

    async def async_config_entry_first_refresh(self) -> None:
        """Handle the first data refresh for the config entry.

        This is called by Home Assistant after the config entry has been
        set up to perform an initial data fetch. It ensures that data is
        available before entities are created and added to Home Assistant.
        """
        await super().async_config_entry_first_refresh()
