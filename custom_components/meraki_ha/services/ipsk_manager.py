"""IPSK Manager for Meraki HA."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, TypedDict, cast

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import event, storage
from homeassistant.util import dt as dt_util

from custom_components.meraki_ha.const.api import DATA_CLIENT
from custom_components.meraki_ha.const.integration import from custom_components.meraki_ha.const.integration import DOMAIN

if TYPE_CHECKING:
    from ..core.api import MerakiApiClientProtocol

_LOGGER = logging.getLogger(__name__)

STORAGE_KEY = "meraki_ha_guest_keys"
STORAGE_VERSION = 1
REAP_INTERVAL = timedelta(minutes=5)


class IPSKKey(TypedDict):
    """IPSK Key stored in Home Assistant."""

    identity_psk_id: str
    network_id: str
    ssid_number: str
    name: str
    passphrase: str
    expires_at: str  # ISO formatted string
    config_entry_id: str


class IPSKManager:
    """
    Backend lifecycle manager for Meraki Identity PSKs (IPSK).

    Guarantees temporary guest keys are deleted when they expire.
    This class is intended to be a singleton within the DOMAIN.
    """

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the manager."""
        self.hass = hass
        self.store: storage.Store[dict[str, list[IPSKKey]]] = storage.Store(
            hass, STORAGE_VERSION, STORAGE_KEY
        )
        self.active_keys: list[IPSKKey] = []
        self._unsub_reap_task: event.UnsubscribeFunc | None = None

    async def async_setup(self) -> None:
        """Set up the manager and load existing keys."""
        await self.async_load()
        self._unsub_reap_task = event.async_track_time_interval(
            self.hass, self.async_check_expirations, REAP_INTERVAL
        )
        _LOGGER.debug("IPSKManager set up with %d active keys", len(self.active_keys))

    async def async_load(self) -> None:
        """Load existing keys from storage."""
        stored_data = await self.store.async_load()
        if stored_data:
            self.active_keys = stored_data.get("keys", [])

    async def _save(self) -> None:
        """Save current keys to storage."""
        await self.store.async_save({"keys": self.active_keys})

    async def create_guest_key(
        self,
        config_entry_id: str,
        network_id: str,
        ssid_number: str,
        duration_minutes: int,
        name: str,
        passphrase: str | None = None,
        group_policy_id: str | None = None,
    ) -> IPSKKey:
        """Create a guest IPSK on Meraki and track it in HA."""
        client = self._get_client(config_entry_id)
        if not client:
            raise ValueError(
                f"Meraki client not found for config entry {config_entry_id}"
            )

        result = await client.wireless.create_identity_psk(
            network_id,
            ssid_number,
            name,
            group_policy_id,
            passphrase,
        )

        if not result or "id" not in result:
            _LOGGER.error("Failed to create Identity PSK: %s", result)
            raise ValueError("Failed to create Identity PSK on Meraki Dashboard")

        expires_at = dt_util.utcnow() + timedelta(minutes=duration_minutes)

        new_key: IPSKKey = {
            "identity_psk_id": str(result["id"]),
            "network_id": network_id,
            "ssid_number": str(ssid_number),
            "name": name,
            "passphrase": result.get("passphrase", passphrase or ""),
            "expires_at": expires_at.isoformat(),
            "config_entry_id": config_entry_id,
        }

        self.active_keys.append(new_key)
        await self._save()

        _LOGGER.info(
            "Created guest IPSK '%s' for network %s, expires at %s",
            name,
            network_id,
            expires_at,
        )

        return new_key

    async def remove_guest_key(
        self, identity_psk_id: str, save_after: bool = True
    ) -> bool:
        """
        Remove a guest IPSK from Meraki and stop tracking it.

        Args:
            identity_psk_id: The ID of the PSK to remove.
            save_after: Whether to save the store after removal.

        Returns
        -------
            True if removed from tracking (either succeeded or not found/deleted),
            False if deletion failed due to transient error.
        """
        key_to_remove = next(
            (k for k in self.active_keys if k["identity_psk_id"] == identity_psk_id),
            None,
        )

        if not key_to_remove:
            _LOGGER.debug(
                "IPSK %s not found in tracking, nothing to remove", identity_psk_id
            )
            return True

        client = self._get_client(key_to_remove["config_entry_id"])
        if client:
            try:
                await client.wireless.delete_identity_psk(
                    key_to_remove["network_id"],
                    key_to_remove["ssid_number"],
                    key_to_remove["identity_psk_id"],
                )
                _LOGGER.info(
                    "Deleted guest IPSK '%s' (ID: %s) from Meraki Dashboard",
                    key_to_remove["name"],
                    identity_psk_id,
                )
            except Exception as e:
                # If error is not 404, we don't remove it from tracking yet.
                # If the PSK doesn't exist, we should remove from tracking.
                error_msg = str(e).lower()
                if "404" in error_msg or "not found" in error_msg:
                    _LOGGER.debug(
                        "IPSK %s not found on Meraki, removing from tracking",
                        identity_psk_id,
                    )
                else:
                    _LOGGER.error(
                        "Failed to delete IPSK %s from Meraki: %s", identity_psk_id, e
                    )
                    return False
        else:
            _LOGGER.warning(
                "Cannot delete IPSK %s from Meraki: Client unavailable for entry %s",
                identity_psk_id,
                key_to_remove["config_entry_id"],
            )
            # If entry is gone, we can't delete it anyway, so remove from tracking
            # to avoid cluttering storage.

        self.active_keys.remove(key_to_remove)
        if save_after:
            await self._save()
        return True

    def get_active_keys(
        self, config_entry_id: str | None = None, network_id: str | None = None
    ) -> list[IPSKKey]:
        """
        Return currently tracked active guest keys.

        Args:
            config_entry_id: Optional filter for a specific config entry.
            network_id: Optional filter for a specific network.
        """
        keys = self.active_keys
        if config_entry_id:
            keys = [k for k in keys if k["config_entry_id"] == config_entry_id]
        if network_id:
            keys = [k for k in keys if k["network_id"] == network_id]
        return keys

    async def async_check_expirations(self, _now: datetime | None = None) -> None:
        """Check for and reap expired keys."""
        now = dt_util.utcnow()
        to_reap: list[str] = []

        for key in self.active_keys:
            expires_at = dt_util.parse_datetime(key["expires_at"])
            if expires_at and expires_at <= now:
                to_reap.append(key["identity_psk_id"])

        if not to_reap:
            return

        _LOGGER.info("Reaping %d expired guest IPSKs", len(to_reap))
        reaped_any = False
        for psk_id in to_reap:
            # Pass save_after=False to avoid multiple I/O operations
            if await self.remove_guest_key(psk_id, save_after=False):
                reaped_any = True

        if reaped_any:
            await self._save()

    def _get_client(self, config_entry_id: str) -> MerakiApiClientProtocol | None:
        """Retrieve Meraki API client for a config entry."""
        if DOMAIN not in self.hass.data:
            return None
        if config_entry_id not in self.hass.data[DOMAIN]:
            return None
        return cast(
            "MerakiApiClientProtocol",
            self.hass.data[DOMAIN][config_entry_id].get(DATA_CLIENT),
        )

    @callback
    def async_unload(self) -> None:
        """Stop the background reaping task."""
        if self._unsub_reap_task:
            self._unsub_reap_task()
            self._unsub_reap_task = None
