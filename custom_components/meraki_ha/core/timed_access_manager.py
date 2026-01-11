"""Timed Access Manager for managing Identity PSKs."""

from datetime import timedelta
from typing import Any

from homeassistant.util import dt as dt_util

from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.helpers.logging_helper import MerakiLoggers

_LOGGER = MerakiLoggers.MAIN


class TimedAccessManager:
    """Manager for creating and managing timed access keys (Identity PSKs)."""

    def __init__(self, api_client: MerakiAPIClient) -> None:
        """Initialize the TimedAccessManager."""
        self._api_client = api_client

    async def create_timed_access_key(
        self,
        network_id: str,
        ssid_number: str,
        name: str,
        passphrase: str,
        duration_hours: int,
        group_policy_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a new timed access key.

        Args:
        ----
            network_id: The ID of the network.
            ssid_number: The SSID number (e.g. '1', '2').
            name: The name for the IPSK.
            passphrase: The passphrase for the IPSK.
            duration_hours: How long the key should be valid for.
            group_policy_id: Optional group policy ID to apply.

        Returns
        -------
            The created IPSK data.

        """
        # Calculate expiration time
        expires_at = dt_util.utcnow() + timedelta(hours=duration_hours)
        expires_at_str = expires_at.isoformat()

        if not group_policy_id:
            # Default to "Normal" policy if none is provided.
            # This is required because the underlying API call expects a positional arg.
            group_policy_id = "Normal"

        wireless = self._api_client.wireless
        return await wireless.create_network_wireless_ssid_identity_psk(
            network_id=network_id,
            number=ssid_number,
            name=name,
            group_policy_id=group_policy_id,
            passphrase=passphrase,
            expiresAt=expires_at_str,
        )
