"""Utilities for Meraki HA WebSocket API."""

import logging
from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const.integration import DOMAIN, _LOGGER= logging.getLogger(__name__)

T = TypeVar("T")


def get_config_entry_data(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
    config_entry_id: str,
    key: str,
) -> Any | None:
    """Get data from config entry, returning None and sending error if not found."""
    if DOMAIN not in hass.data or config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return None

    data = hass.data[DOMAIN][config_entry_id].get(key)
    if data is None:
        connection.send_error(msg["id"], "not_found", f"{key} not found for entry")
        return None

    return data


def handle_ws_error(
    func: Callable[
        [HomeAssistant, websocket_api.ActiveConnection, dict[str, Any]],
        Coroutine[Any, Any, None],
    ],
) -> Callable[
    [HomeAssistant, websocket_api.ActiveConnection, dict[str, Any]],
    Coroutine[Any, Any, None],
]:
    """Handle exceptions in async WebSocket commands."""

    async def wrapper(
        hass: HomeAssistant,
        connection: websocket_api.ActiveConnection,
        msg: dict[str, Any],
    ) -> None:
        try:
            await func(hass, connection, msg)
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.exception(
                "Error handling WebSocket command %s: %s", msg.get("type"), err
            )
            connection.send_error(msg["id"], "unknown_error", str(err))

    return wrapper
