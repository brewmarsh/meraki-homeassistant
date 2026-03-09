"""Intents for the Meraki HA integration."""

from __future__ import annotations

import logging
from typing import Any

from baml_client import b
from baml_client.types import MerakiIntent
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent

from .const.integration import DOMAIN

_LOGGER = logging.getLogger(__name__)

INTENT_MERAKI_SMART_COMMAND = "MerakiSmartCommand"


async def async_setup_intents(hass: HomeAssistant) -> None:
    """Set up the Meraki intents."""
    intent.async_register(hass, MerakiSmartCommandHandler())


class MerakiSmartCommandHandler(intent.IntentHandler):
    """Handle Meraki smart commands."""

    intent_type = INTENT_MERAKI_SMART_COMMAND
    slot_schema = {intent.vol.Required("command"): intent.cv.string}

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        """Handle the intent."""
        slots = self.async_validate_slots(intent_obj.slots)
        user_text = slots.get("command", {}).get("value")

        if not user_text:
            response = intent_obj.create_response()
            response.async_set_speech("I didn't receive a command to process.")
            return response

        _LOGGER.debug("Received Meraki smart command: %s", user_text)

        # Pass to BAML
        try:
            baml_response = await b.RouteMerakiIntent(user_command=user_text)
        except Exception as err:
            _LOGGER.error("BAML routing failed: %s", err)
            response = intent_obj.create_response()
            response.async_set_speech(
                "I'm sorry, I had trouble processing that network command."
            )
            return response

        _LOGGER.debug("BAML response: %s", baml_response)

        response = intent_obj.create_response()

        if baml_response.intent == MerakiIntent.Unknown:
            response.async_set_speech(
                "I'm not sure how to help with that Meraki command."
            )
            return response

        # Execute the command
        speech = await self._async_execute_intent(intent_obj.hass, baml_response)
        response.async_set_speech(speech)
        return response

    async def _async_execute_intent(
        self, hass: HomeAssistant, baml_response: Any
    ) -> str:
        """Execute the parsed intent."""
        if baml_response.intent == MerakiIntent.RebootDevice:
            return await self._async_handle_reboot(hass, baml_response)
        if baml_response.intent == MerakiIntent.GenerateGuestAccess:
            return await self._async_handle_guest_access(hass, baml_response)
        if baml_response.intent == MerakiIntent.GetNetworkStatus:
            return await self._async_handle_network_status(hass, baml_response)
        if baml_response.intent == MerakiIntent.CycleSwitchPort:
            return "Power cycling switch ports via voice is not yet implemented."

        return "Command recognized but execution is not yet supported."

    async def _async_handle_reboot(self, hass: HomeAssistant, baml_response: Any) -> str:
        """Handle reboot device intent."""
        target = baml_response.target_device
        if not target:
            return "I need to know which device you want to reboot."

        # Find device
        device_data = self._find_device_by_name(hass, target)
        if not device_data:
            return f"I couldn't find a Meraki device named {target}."

        entry_id, serial = device_data
        device_control_service = hass.data[DOMAIN][entry_id]["device_control_service"]

        try:
            await device_control_service.async_reboot(serial)
            return f"Restarting {target} now."
        except Exception as err:
            _LOGGER.error("Failed to reboot %s: %s", target, err)
            return f"I encountered an error while trying to reboot {target}."

    async def _async_handle_guest_access(
        self, hass: HomeAssistant, baml_response: Any
    ) -> str:
        """Handle generate guest access intent."""
        network_name = baml_response.network_name
        guest_name = baml_response.guest_name or "Guest"
        duration = baml_response.duration_minutes or 60

        # Find network
        network_data = self._find_network_by_name(hass, network_name)
        if not network_data:
            if network_name:
                return f"I couldn't find a Meraki network named {network_name}."
            return "I need to know which network to create guest access for."

        entry_id, network_id = network_data
        ipsk_manager = hass.data[DOMAIN].get("ipsk_manager")

        if not ipsk_manager:
            return "Guest access management is not available right now."

        # We need an SSID to use. For now, let's assume SSID 1 or try to find a suitable one.
        # Ideally BAML or the intent should specify.
        # Defaulting to SSID 1 for now as a placeholder.
        ssid_number = "1"

        try:
            key = await ipsk_manager.create_guest_key(
                config_entry_id=entry_id,
                network_id=network_id,
                ssid_number=ssid_number,
                duration_minutes=duration,
                name=guest_name,
            )
            return (
                f"Generated guest access for {guest_name}. "
                f"The password is {key['passphrase']}."
            )
        except Exception as err:
            _LOGGER.error("Failed to generate guest access: %s", err)
            return "I couldn't create the guest password at this time."

    async def _async_handle_network_status(
        self, hass: HomeAssistant, baml_response: Any
    ) -> str:
        """Handle network status intent."""
        network_name = baml_response.network_name
        network_data = self._find_network_by_name(hass, network_name)

        if not network_data:
            if network_name:
                return f"I couldn't find a Meraki network named {network_name}."
            return "I'm not sure which network you're asking about."

        entry_id, network_id = network_data
        network_control_service = hass.data[DOMAIN][entry_id]["network_control_service"]
        main_coordinator = hass.data[DOMAIN][entry_id]["main_coordinator"]

        # Get actual network name from coordinator for friendly response
        actual_name = main_coordinator.networks_by_id.get(network_id, {}).get(
            "name", network_name
        )
        client_count = network_control_service.get_network_client_count(network_id)

        return f"The {actual_name} network currently has {client_count} active clients."

    def _find_device_by_name(
        self, hass: HomeAssistant, name: str
    ) -> tuple[str, str] | None:
        """Find device by name in all config entries."""
        search_name = name.lower()
        for entry_id, entry_data in hass.data[DOMAIN].items():
            if not isinstance(entry_data, dict):
                continue
            main_coordinator = entry_data.get("main_coordinator")
            if not main_coordinator or not main_coordinator.devices_by_serial:
                continue

            for serial, device in main_coordinator.devices_by_serial.items():
                if device.get("name", "").lower() == search_name:
                    return entry_id, serial
        return None

    def _find_network_by_name(
        self, hass: HomeAssistant, name: str | None
    ) -> tuple[str, str] | None:
        """Find network by name in all config entries."""
        if not name:
            # If no name provided, and only one entry/network exists, return it
            all_networks = []
            for entry_id, entry_data in hass.data[DOMAIN].items():
                if not isinstance(entry_data, dict):
                    continue
                main_coordinator = entry_data.get("main_coordinator")
                if not main_coordinator or not main_coordinator.networks_by_id:
                    continue
                for net_id in main_coordinator.networks_by_id:
                    all_networks.append((entry_id, net_id))

            if len(all_networks) == 1:
                return all_networks[0]
            return None

        search_name = name.lower()
        for entry_id, entry_data in hass.data[DOMAIN].items():
            if not isinstance(entry_data, dict):
                continue
            main_coordinator = entry_data.get("main_coordinator")
            if not main_coordinator or not main_coordinator.networks_by_id:
                continue

            for net_id, network in main_coordinator.networks_by_id.items():
                if network.get("name", "").lower() == search_name:
                    return entry_id, net_id
        return None
