"""Auditor for staging tests."""

import logging
from src.staging_test.ha_client import MerakiHaClient

_LOGGER = logging.getLogger(__name__)

class Auditor:
    """Consolidated auditor for staging test states."""

    def __init__(self, ha_url: str, ha_token: str) -> None:
        self.client = MerakiHaClient(ha_url, ha_token)

    async def run_audit(self, allowed_states: list[str]) -> tuple[list[dict], list[dict]]:
        """Run audit against HA states."""
        await self.client.connect()
        try:
            states = await self.client.get_states()
        finally:
            await self.client.close()

        failures = []
        warnings = []

        for entity in states:
            entity_id = entity.get("entity_id", "")
            state = entity.get("state", "")
            domain = entity_id.split(".")[0]

            if "meraki" in entity_id and state in allowed_states:
                if domain == "button" and state == "unknown":
                    continue

                if domain in ["sensor", "binary_sensor", "switch"]:
                    warnings.append(entity)
                else:
                    failures.append(entity)
        
        return failures, warnings
