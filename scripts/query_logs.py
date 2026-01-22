#!/usr/bin/env python3
"""
Query the Better Stack Logs API for recent error logs from the `meraki_ha` integration.

This script queries the Better Stack API for any "error" level logs containing
"meraki_ha" that occurred in the last 5 minutes. If found,
it prints them to stderr and exits with a status code of 1; otherwise, it exits with 0.
it prints them to stderr and exits with a status code of 1. Otherwise, it exits with 0.

Configuration is provided via environment variables:
- `BETTER_STACK_API_TOKEN`: An API token for the Better Stack Logs API.
"""

import os
import sys
from datetime import datetime, timedelta, timezone

import requests


def main():
    """Query the logs."""
    api_token = os.environ.get("BETTER_STACK_API_TOKEN")

    if not api_token:
        print(
            "BETTER_STACK_API_TOKEN environment variable must be set.", file=sys.stderr
        )
        sys.exit(1)

    headers = {"Authorization": f"Bearer {api_token}"}
    url = "https://logs.betterstack.com/api/v1/query"

    now = datetime.now(timezone.utc)
    five_minutes_ago = now - timedelta(minutes=5)

    query = f"SELECT * FROM logs WHERE level = 'error' AND message LIKE '%meraki_ha%' AND to_timestamp(dt) >= '{five_minutes_ago.isoformat()}'"  # nosec

    response = requests.post(
        url, headers=headers, json={"query": query}, timeout=30
    )

    if response.status_code != 200:
        print(
            f"Error querying Better Stack API: {response.status_code}",
            file=sys.stderr,
        )
        print(response.text, file=sys.stderr)
        sys.exit(1)

    logs = response.json().get("data", [])
    if logs:
        print(f"Found {len(logs)} error logs in the last 5 minutes:", file=sys.stderr)
        for log in logs:
            print(log, file=sys.stderr)
        sys.exit(1)

    print("No error logs found for meraki_ha in the last 5 minutes.")
    sys.exit(0)


if __name__ == "__main__":
    main()
