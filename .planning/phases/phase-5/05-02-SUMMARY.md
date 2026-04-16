# Phase 5 Plan 02 Summary: Robust Error Handling

## Goal

Refine error handling across all coordinators to use the standard Home Assistant `UpdateFailed` exception, ensuring entities correctly indicate they are "Unavailable" during API outages.

## Changes

### 1. Centralized Error Handling in Main Coordinator

- **Artifact**: `custom_components/meraki_ha/coordinators/main.py`
- **Logic**: Updated `_async_update_data` to raise `UpdateFailed` instead of returning stale data on exception. Added specific handling for 429 rate limits.

### 2. Consistency across Sub-Coordinators

- **Artifact**: `custom_components/meraki_ha/core/coordinators/ssid_firewall_coordinator.py`
- **Logic**: Updated `_async_update_data` to raise `UpdateFailed` if any network fetch fails, ensuring firewall rules and client policies are not served as stale data.
- **Artifact**: `custom_components/meraki_ha/discovery/coordinator.py`
- **Logic**: Updated to raise `UpdateFailed` on discovery failures, preventing hierarchical mapping issues during API downtime.

## Verification Results

### Code Audit

- Verified that all `_async_update_data` implementations now properly use `raise UpdateFailed` for terminal errors.

### Linting

- All files passed `ruff` and `ruff-format` (E501 line length issues resolved).

## Success Criteria Status

- [x] Terminal API errors lead to UpdateFailed.
- [x] Entities show as unavailable during outages.
