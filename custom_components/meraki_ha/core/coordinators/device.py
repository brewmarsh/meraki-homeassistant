"""Coordinator for Meraki device data."""

import logging
from typing import Any, Dict, List, Optional

from homeassistant.helpers.update_coordinator import UpdateFailed

from .base import BaseMerakiCoordinator
from ..utils import map_meraki_model_to_device_type

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceCoordinator(BaseMerakiCoordinator):
    """Coordinator to handle Meraki device data."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the device coordinator."""
        super().__init__(*args, **kwargs)
        self._devices: List[Dict[str, Any]] = []

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch device data from Meraki.

        Fetches all devices and enhances their data with product type mapping
        and additional device-specific information like client counts for wireless
        devices, port statuses for switches, uplink information and traffic data
        for appliances, and sensor readings for MT sensors.

        Returns:
            Dict containing device data

        Raises:
            UpdateFailed: If update fails
        """
        try:
            devices = await self.api_client.organization.get_organization_devices()
            processed_devices = []

            # Fetch clients and count them per device
            client_counts = {}
            networks = await self.api_client.organization.get_organization_networks()
            _LOGGER.debug(f"Found {len(networks)} networks")
            for network in networks:
                clients = await self.api_client.network.get_network_clients(
                    network["id"]
                )
                _LOGGER.debug(f"Found {len(clients)} clients in network {network['id']}")
                if clients:
                    _LOGGER.debug(f"First client data: {clients[0]}")
                for client in clients:
                    if client.get("status") == "Online":
                        serial = client.get("recentDeviceSerial")
                        if serial:
                            client_counts[serial] = client_counts.get(serial, 0) + 1
            _LOGGER.debug(f"Final client counts: {client_counts}")

            statuses = (
                await self.api_client.organization.get_organization_device_statuses()
            )
            for device in devices:
                for status in statuses:
                    if status.get("serial") == device.get("serial"):
                        device["status"] = status.get("status")
                        break
                # Skip devices without required attributes
                if not all(key in device for key in ["serial", "model"]):
                    _LOGGER.warning("Device missing required attributes: %s", device)
                    continue

                # Add product type based on model
                model = device.get("model", "")
                device["productType"] = map_meraki_model_to_device_type(model)

                # Add connected clients count
                device["connected_clients_count"] = client_counts.get(
                    device["serial"], 0
                )

                # Fetch additional data for wireless devices
                if device["productType"] == "wireless":
                    try:
                        # These would be actual API calls in your implementation
                        device["radio_settings"] = {
                            "status": "unknown",
                            "24": {"channel": 0, "power": 0},
                            "5": {"channel": 0, "power": 0},
                        }
                    except Exception as err:
                        _LOGGER.warning(
                            "Error fetching wireless data for device %s: %s",
                            device.get("serial"),
                            err,
                        )
                # Fetch additional data for camera devices
                if device["productType"] == "camera":
                    try:
                        device[
                            "sense_settings"
                        ] = await self.api_client.camera.get_camera_sense_settings(
                            device["serial"]
                        )
                        device[
                            "video_settings"
                        ] = await self.api_client.camera.get_camera_video_settings(
                            device["serial"]
                        )
                        video_link = (
                            await self.api_client.camera.get_device_camera_video_link(
                                device["serial"]
                            )
                        )
                        device["video_settings"].update(video_link)
                    except Exception as err:
                        _LOGGER.warning(
                            "Error fetching camera data for device %s: %s",
                            device.get("serial"),
                            err,
                        )

                # Fetch additional data for appliance devices
                if device["productType"] == "appliance":
                    try:
                        device[
                            "ports"
                        ] = await self.api_client.appliance.get_appliance_ports(
                            device["networkId"]
                        )
                        device[
                            "uplinks"
                        ] = await self.api_client.appliance.get_device_appliance_uplinks_settings(
                            device["serial"]
                        )
                        device[
                            "traffic"
                        ] = await self.api_client.network.get_network_appliance_traffic(
                            device["networkId"]
                        )
                    except Exception as err:
                        _LOGGER.warning(
                            "Error fetching appliance data for device %s: %s",
                            device.get("serial"),
                            err,
                        )
                # Fetch additional data for switch devices
                if device["productType"] == "switch":
                    try:
                        device[
                            "port_statuses"
                        ] = await self.api_client.switch.get_device_switch_ports_statuses(
                            device["serial"]
                        )
                    except Exception as err:
                        _LOGGER.warning(
                            "Error fetching switch data for device %s: %s",
                            device.get("serial"),
                            err,
                        )
                # Fetch additional data for sensor devices
                # if device["productType"] == "sensor":
                #     try:
                #         device["readings"] = (
                #             await self.api_client.get_device_sensor_command(
                #                 device["serial"]
                #             )
                #         )
                #     except Exception as err:
                #         _LOGGER.warning(
                #             "Error fetching sensor data for device %s: %s",
                #             device.get("serial"),
                #             err,
                #         )
                processed_devices.append(device)
            firmware_upgrades = (
                await self.api_client.organization.get_organization_firmware_upgrades()
            )
            for device in processed_devices:
                for upgrade in firmware_upgrades:
                    if upgrade.get("serial") == device.get("serial"):
                        device["firmware_upgrades"] = upgrade
                        break

            self._devices = processed_devices
            return {"devices": processed_devices}

        except Exception as err:
            _LOGGER.error("Error fetching device data: %s", err)
            raise UpdateFailed(f"Error fetching device data: {err}")

    def get_device_by_serial(self, serial: str) -> Optional[Dict[str, Any]]:
        """Get a device by its serial number.

        Args:
            serial: Device serial number

        Returns:
            Device data dictionary or None if not found
        """
        for device in self._devices:
            if device.get("serial") == serial:
                return device
        return None
