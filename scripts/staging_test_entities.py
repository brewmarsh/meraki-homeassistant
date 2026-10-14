#!/usr/bin/env python3
"""Entry point for staging audits using consolidated Auditor."""

import asyncio
import os
import sys

from src.staging_test.auditor import Auditor


async def main() -> None:
    ha_url = os.environ.get("HA_URL")
    ha_token = os.environ.get("HA_TOKEN")
    allowed_states = os.environ.get(
        "ALLOWED_STAGING_STATES", "unknown,unavailable"
    ).split(",")

    if not ha_url or not ha_token:
        print("Missing HA_URL or HA_TOKEN")
        sys.exit(1)

    auditor = Auditor(ha_url, ha_token)
    failures, warnings = await auditor.run_audit(allowed_states)

    if warnings:
        print(f"Found {len(warnings)} warnings.")

    if failures:
        print(f"Found {len(failures)} failures.")
        sys.exit(1)

    print("Success.")


if __name__ == "__main__":
    asyncio.run(main())
