"""Utility functions for Meraki flows."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.core import HomeAssistant

from ..const_conf import CONF_MERAKI_API_KEY, CONF_MERAKI_ORG_ID
from ..core.errors import MerakiAuthenticationError, MerakiConnectionError

if TYPE_CHECKING:
    from ..coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


def get_network_options(data: dict[str, Any]) -> list[dict[str, str]]:
    """Get network options from coordinator data."""
    network_options = []
    networks = data.get("networks", [])
    for network in networks:
        name = getattr(network, "name", None)
        if name is None and isinstance(network, dict):
            name = network.get("name")

        net_id = getattr(network, "id", None)
        if net_id is None and isinstance(network, dict):
            net_id = network.get("id")

        if name and net_id:
            network_options.append({"label": name, "value": net_id})
    return network_options


def has_cameras(data: dict[str, Any]) -> bool:
    """Check if cameras are present in coordinator data."""
    devices = data.get("devices", [])
    for device in devices:
        p_type = ""
        model = ""
        if isinstance(device, dict):
            p_type = device.get("productType") or device.get("product_type", "")
            model = device.get("model", "")
        else:
            p_type = getattr(device, "product_type", "") or ""
            model = getattr(device, "model", "") or ""

        if "camera" in p_type.lower() or (model and model.startswith("MV")):
            return True
    return False


async def validate_credentials(
    hass: HomeAssistant,
    user_input: dict[str, Any],
) -> tuple[dict[str, str], dict[str, Any] | None]:
    """Validate Meraki credentials and return errors and validation result."""
    from ..authentication import validate_meraki_credentials

    errors: dict[str, str] = {}
    validation_result: dict[str, Any] | None = None

    try:
        api_key = user_input[CONF_MERAKI_API_KEY]
        org_id = user_input[CONF_MERAKI_ORG_ID]
        validation_result = await validate_meraki_credentials(
            hass,
            api_key,
            org_id,
        )
    except MerakiAuthenticationError:
        errors["base"] = "invalid_auth"
    except MerakiConnectionError:
        errors["base"] = "cannot_connect"
    except Exception:
        _LOGGER.exception("Unexpected exception")
        errors["base"] = "unknown"

    return errors, validation_result
