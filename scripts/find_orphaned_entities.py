#!/usr/bin/env python3
"""Script to find orphaned Meraki entities in Home Assistant.

This script queries the Home Assistant API to identify entities that:
1. Have 'restored: true' in their attributes (orphaned from previous loads)
2. Are unavailable and appear to be old/unused Meraki entities

Usage:
    python scripts/find_orphaned_entities.py \
        --url http://192.168.14.50 --token YOUR_TOKEN

    Or set environment variables:
    export HA_URL=http://192.168.14.50
    export HA_TOKEN=your_long_lived_access_token
    python scripts/find_orphaned_entities.py
"""

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def get_all_states(base_url: str, token: str) -> list[dict]:
    """Fetch all entity states from Home Assistant API."""
    url = f"{base_url}/api/states"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        sys.exit(1)
    except URLError as e:
        print(f"URL Error: {e.reason}")
        sys.exit(1)


def is_meraki_entity(entity_id: str) -> bool:
    """Check if an entity is from the Meraki integration."""
    meraki_patterns = [
        "meraki",
        "ssid",
        "switch.",  # Many Meraki switches
        "sensor.camera_",
        "sensor.cellulargateway",
        "sensor.appliance_",
        "binary_sensor.port_",
    ]
    entity_lower = entity_id.lower()
    return any(pattern in entity_lower for pattern in meraki_patterns)


def find_orphaned_entities(states: list[dict]) -> dict[str, list[dict]]:
    """Find orphaned Meraki entities."""
    orphaned = {
        "restored": [],  # Entities with restored: true
        "unavailable": [],  # Unavailable Meraki entities
    }

    for state in states:
        entity_id = state.get("entity_id", "")
        state_value = state.get("state", "")
        attributes = state.get("attributes", {})

        # Skip non-Meraki entities
        if not is_meraki_entity(entity_id):
            continue

        # Check for restored entities (orphaned from previous loads)
        if attributes.get("restored") is True:
            orphaned["restored"].append(
                {
                    "entity_id": entity_id,
                    "state": state_value,
                    "friendly_name": attributes.get("friendly_name", ""),
                    "reason": "restored: true (no longer created)",
                }
            )
        # Check for unavailable entities
        elif state_value == "unavailable":
            orphaned["unavailable"].append(
                {
                    "entity_id": entity_id,
                    "state": state_value,
                    "friendly_name": attributes.get("friendly_name", ""),
                    "reason": "unavailable (may be orphaned or device offline)",
                }
            )

    return orphaned


def generate_delete_commands(entities: list[dict], base_url: str) -> list[str]:
    """Generate curl commands to delete entities."""
    commands = []
    for entity in entities:
        entity_id = entity["entity_id"]
        # Use entity registry remove endpoint
        cmd = (
            f'curl -X DELETE "{base_url}/api/config/entity_registry/{entity_id}" '
            f'-H "Authorization: Bearer $HA_TOKEN"'
        )
        commands.append(cmd)
    return commands


def main() -> None:
    """Entry point for orphaned entity finder script."""
    parser = argparse.ArgumentParser(
        description="Find orphaned Meraki entities in Home Assistant"
    )
    parser.add_argument(
        "--url",
        default=os.environ.get("HA_URL", "http://192.168.14.50"),
        help="Home Assistant URL (default: $HA_URL or http://192.168.14.50)",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("HA_TOKEN"),
        help="Long-lived access token (default: $HA_TOKEN)",
    )
    parser.add_argument(
        "--generate-delete-script",
        action="store_true",
        help="Generate a script to delete orphaned entities",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    args = parser.parse_args()

    if not args.token:
        print(
            "Error: No token provided. "
            "Use --token or set HA_TOKEN environment variable."
        )
        sys.exit(1)

    print(f"Connecting to Home Assistant at {args.url}...")
    states = get_all_states(args.url, args.token)
    print(f"Found {len(states)} total entities")

    orphaned = find_orphaned_entities(states)

    if args.json:
        print(json.dumps(orphaned, indent=2))
        return

    # Print restored entities
    print("\n" + "=" * 70)
    print("ORPHANED ENTITIES (restored: true)")
    print("These entities are no longer created by the integration.")
    print("=" * 70)

    if orphaned["restored"]:
        for entity in orphaned["restored"]:
            print(f"\n  Entity ID: {entity['entity_id']}")
            print(f"  Name: {entity['friendly_name']}")
            print(f"  State: {entity['state']}")
            print(f"  Reason: {entity['reason']}")
    else:
        print("\n  No orphaned (restored) entities found!")

    # Print unavailable entities
    print("\n" + "=" * 70)
    print("UNAVAILABLE MERAKI ENTITIES")
    print("These may be orphaned OR the device may be offline.")
    print("=" * 70)

    if orphaned["unavailable"]:
        for entity in orphaned["unavailable"]:
            print(f"\n  Entity ID: {entity['entity_id']}")
            print(f"  Name: {entity['friendly_name']}")
            print(f"  Reason: {entity['reason']}")
    else:
        print("\n  No unavailable Meraki entities found!")

    # Summary
    total_orphaned = len(orphaned["restored"])
    total_unavailable = len(orphaned["unavailable"])

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Orphaned entities (restored: true): {total_orphaned}")
    print(f"  Unavailable entities: {total_unavailable}")

    if args.generate_delete_script and orphaned["restored"]:
        print("\n" + "=" * 70)
        print("DELETE COMMANDS FOR ORPHANED ENTITIES")
        print("Review carefully before running!")
        print("=" * 70)
        print("\n# Set your token first:")
        print("export HA_TOKEN='your_token_here'")
        print()

        commands = generate_delete_commands(orphaned["restored"], args.url)
        for cmd in commands:
            print(cmd)

        # Also create a shell script
        script_path = "scripts/delete_orphaned_entities.sh"
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("# Auto-generated script to delete orphaned Meraki entities\n")
            f.write("# Review carefully before running!\n\n")
            f.write('if [ -z "$HA_TOKEN" ]; then\n')
            f.write('  echo "Error: Set HA_TOKEN environment variable first"\n')
            f.write("  exit 1\n")
            f.write("fi\n\n")
            for cmd in commands:
                f.write(f"{cmd}\n")
                deleted_name = cmd.split("/")[-1].split('"')[0]
                f.write(f'echo "Deleted: {deleted_name}"\n')

        print(f"\nScript saved to: {script_path}")
        print(
            "Run with: chmod +x scripts/delete_orphaned_entities.sh && "
            "./scripts/delete_orphaned_entities.sh"
        )


if __name__ == "__main__":
    main()
