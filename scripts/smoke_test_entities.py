#!/usr/bin/env python3
"""Smoke test script for unknown/unavailable Meraki entities in HA."""

import json
import os
import sys
import urllib.request
from typing import Any


def create_github_issue(
    repository: str,
    token: str,
    release_tag: str,
    broken_entities: list[dict[str, Any]],
) -> None:
    """Create a GitHub issue with the broken entities report."""
    url = f"https://api.github.com/repos/{repository}/issues"

    report_lines = [
        "The following Meraki entities were found in an unknown or unavailable "
        "state during the post-deployment smoke test.",
        "",
        "| Entity ID | State | Friendly Name |",
        "|-----------|-------|---------------|",
    ]

    for entity in broken_entities:
        entity_id = entity.get("entity_id", "N/A")
        state = entity.get("state", "N/A")
        friendly_name = entity.get("attributes", {}).get("friendly_name", "N/A")
        report_lines.append(f"| {entity_id} | {state} | {friendly_name} |")

    report_lines.append("")
    report_lines.append("Ping @maintainers")

    body = "\n".join(report_lines)
    title = f"⚠️ Smoke Test Failed: Unknown Entities in {release_tag}"

    issue_data = {
        "title": title,
        "body": body,
        "labels": ["bug", "release-blocker"],
    }
    data = json.dumps(issue_data).encode("utf-8")

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        # Bandit B310: Audit url open for permitted schemes.
        # We use https:// in the URL construction above.
        with urllib.request.urlopen(req) as response:  # nosec B310
            if response.status == 201:
                print(f"Successfully created GitHub issue: {title}")
            else:
                print(f"Failed to create GitHub issue. Status code: {response.status}")
                sys.exit(1)
    except Exception as err:
        print(f"Error creating GitHub issue: {err}")
        sys.exit(1)


def main() -> None:
    """Run the smoke test."""
    ha_url = os.environ.get("HA_URL")
    ha_token = os.environ.get("HA_TOKEN")
    github_token = os.environ.get("GITHUB_TOKEN")
    github_repository = os.environ.get("GITHUB_REPOSITORY")
    release_tag = os.environ.get("RELEASE_TAG")

    if (
        ha_url is None
        or ha_token is None
        or github_token is None
        or github_repository is None
        or release_tag is None
    ):
        print(
            "Error: Missing required environment variables: "
            "HA_URL, HA_TOKEN, GITHUB_TOKEN, GITHUB_REPOSITORY, RELEASE_TAG"
        )
        sys.exit(1)

    # Normalize HA_URL
    ha_url = ha_url.rstrip("/")
    api_url = f"{ha_url}/api/states"

    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(api_url, headers=headers)

    try:
        # Bandit B310: Audit url open for permitted schemes.
        # HA_URL is expected to be a valid URL.
        with urllib.request.urlopen(req) as response:  # nosec B310
            if response.status != 200:
                print(f"Failed to query HA API. Status code: {response.status}")
                sys.exit(1)

            states = json.loads(response.read().decode("utf-8"))
    except Exception as err:
        print(f"Error querying Home Assistant API: {err}")
        sys.exit(1)

    broken_entities = []
    for entity in states:
        entity_id = entity.get("entity_id", "")
        state = entity.get("state", "")

        # Filter logic: Look for entities where entity_id contains "meraki"
        # and state is either "unknown" or "unavailable".
        if "meraki" in entity_id and state in ["unknown", "unavailable"]:
            broken_entities.append(entity)

    if not broken_entities:
        print("Success: No broken Meraki entities found.")
        sys.exit(0)
    else:
        print(f"Found {len(broken_entities)} broken Meraki entities.")
        create_github_issue(
            github_repository, github_token, release_tag, broken_entities
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
