#!/usr/bin/env python3
"""
Connect to a Home Assistant instance and check the health of the meraki_ha integration.

This script connects to the Home Assistant WebSocket API to perform the
following checks:
1. Verifies that the `meraki_ha` integration domain is loaded.
2. Fetches all entities and identifies those belonging to `meraki_ha`.
3. Checks if any of these entities have a state of `unavailable` or `unknown`.

Exemptions:
- 'button' entities are allowed to be 'unknown' (stateless).
- 'sensor', 'binary_sensor', and 'switch' entities in 'unknown' or 'unavailable'
  states log as WARNINGS but do not fail the build (common in staging).

The script exits with a status code of 1 if any non-exempt checks fail, and 0 otherwise.
Configuration is provided via environment variables:
- `HA_URL`: The URL of the Home Assistant instance (e.g., `ws://localhost:8123/api/websocket`).
- `HA_TOKEN`: A long-lived access token for Home Assistant.
- `ALLOWED_STAGING_STATES`: Comma-separated list of states to tolerate in staging (default: unknown,unavailable).
"""

import asyncio
import os
import sys

from homeassistant_ws import HomeAssistantClient

# Action 2: Staging allowance list
ALLOWED_STAGING_STATES = os.environ.get(
    "ALLOWED_STAGING_STATES", "unknown,unavailable"
).split(",")


async def main():
    """Perform the staging test."""
    ha_url = os.environ.get("HA_URL")
    ha_token = os.environ.get("HA_TOKEN")

    if not ha_url or not ha_token:
        print("HA_URL and HA_TOKEN environment variables must be set.", file=sys.stderr)
        sys.exit(1)

    try:
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
                entity
                for entity in entity_registry
                if entity["platform"] == "meraki_ha"
            ]

            states = await client.get_states()
            failures = []
            warnings = []

            for entity in meraki_entities:
                entity_id = entity["entity_id"]
                domain = entity_id.split(".")[0]

                # Find the state for this entity
                state_obj = next(
                    (s for s in states if s["entity_id"] == entity_id), None
                )
                if not state_obj:
                    # Entity exists in registry but not in states
                    state = "unknown"
                else:
                    state = state_obj["state"]

                if state in ALLOWED_STAGING_STATES:
                    # Action 1: Button exemption (ANY button entity)
                    if domain == "button" and state == "unknown":
                        continue

                    # Action 2: Staging allowance for sensors, binary_sensors, and switches
                    if domain in ["sensor", "binary_sensor", "switch"]:
                        warnings.append(f"{entity_id} is {state} (expected in staging)")
                    else:
                        failures.append(f"{entity_id} is {state}")

            if warnings:
                print("=== ENTITY STATE WARNINGS (Expected in Staging) ===")
                for w in warnings:
                    print(f"WARNING: {w}")
                print("====================================================")

            if failures:
                print(
                    f"Found {len(failures)} critical meraki_ha entity failures:",
                    file=sys.stderr,
                )
                for f in failures:
                    print(f"FAILURE: {f}", file=sys.stderr)
                sys.exit(1)

            print(
                "Audit complete. All meraki_ha entities are healthy or matched staging exemptions."
            )
            sys.exit(0)
    except Exception as err:
        print(f"Error during audit: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
