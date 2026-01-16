#!/usr/bin/env python3
"""
Check the health of the meraki_ha integration in Home Assistant.

This script connects to the Home Assistant WebSocket API and performs the
following checks:
1. Verifies that the `meraki_ha` integration domain is loaded.
2. Fetches all entities and identifies those belonging to `meraki_ha`.
3. Checks if any of these entities have a state of `unavailable`.

The script exits with a status code of 1 if any of the checks fail, and 0 otherwise.
Configuration is provided via environment variables:
- `HA_URL`: The URL of the Home Assistant instance (e.g., `ws://localhost:8123/api/websocket`).
- `HA_TOKEN`: A long-lived access token for Home Assistant.
"""

import asyncio
import json
import os
import sys

from homeassistant_ws import HomeAssistantClient


async def main():
    """Perform the health check smoke test."""
    ha_url = os.environ.get("HA_URL")
    ha_token = os.environ.get("HA_TOKEN")

    if not ha_url or not ha_token:
        print("HA_URL and HA_TOKEN environment variables must be set.", file=sys.stderr)
        sys.exit(1)

    async with HomeAssistantClient(ha_url, ha_token) as client:
        # 1. Check if the meraki_ha domain is loaded
        config = await client.get_config()
        if "meraki_ha" not in config["components"]:
            print("meraki_ha integration is not loaded.", file=sys.stderr)
            sys.exit(1)

        print("meraki_ha integration is loaded.")

        # 2. Check for unavailable entities
        entity_registry = await client.get_entity_registry()
        meraki_entities = [
            entity for entity in entity_registry if entity["platform"] == "meraki_ha"
        ]

        states = await client.get_states()
        unavailable_entities = []
        for entity in meraki_entities:
            for state in states:
                entity_id_match = state["entity_id"] == entity["entity_id"]
                is_unavailable = state["state"] == "unavailable"
                if entity_id_match and is_unavailable:
                    unavailable_entities.append(state)

        if unavailable_entities:
            count = len(unavailable_entities)
            msg = f"Found {count} unavailable meraki_ha entities:"
            print(msg, file=sys.stderr)
            print(json.dumps(unavailable_entities, indent=2), file=sys.stderr)
            sys.exit(1)

        print("All meraki_ha entities are available.")
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
