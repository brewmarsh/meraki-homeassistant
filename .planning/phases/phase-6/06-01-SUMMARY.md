# Phase 6 Wave 1 Summary: Native Firmware Management

## Goal

Implement the Home Assistant `update` entity to surface available Meraki firmware versions and allow users to trigger upgrades directly from the HA UI.

## Changes

### 1. Data Fetching

- **Artifact**: `custom_components/meraki_ha/core/coordinator_helpers/data_fetcher.py`
- **Logic**: Added `get_organization_firmware_upgrades` to the slow poll cycle (every 10 minutes).
- **Mapping**: Implemented logic to map organization-wide firmware upgrade data to individual devices based on `networkId` and `productType`.

### 2. Update Platform Implementation

- **Artifact**: `custom_components/meraki_ha/update.py`
- **Feature**: Created `MerakiUpdateEntity` which supports:
  - **Installed Version**: Taken from `device.firmware`.
  - **Latest Version**: Extracted from `availableVersions` in the firmware upgrade data.
  - **Release Notes**: Surfaced from the Meraki API.
  - **Installation**: Implemented `async_install` using the `createNetworkFirmwareUpgradesRollout` API.

### 3. API & Discovery

- **Artifact**: `custom_components/meraki_ha/core/api/endpoints/network.py`
- **Logic**: Added `create_network_firmware_upgrades_rollout` to `NetworkEndpoints`.
- **Artifact**: `custom_components/meraki_ha/discovery/handlers/universal.py`
- **Logic**: Registered the `update` capability and mapped it to `MerakiUpdateEntity` for all devices.
- **Artifact**: `custom_components/meraki_ha/const/platform.py`
- **Logic**: Added `PLATFORM_UPDATE` to the supported platforms list.
- **Artifact**: `custom_components/meraki_ha/const/device.py`
- **Logic**: Added `update` capability to all major device capability lists and `DEFAULT_CAPS`.

## Verification Results

### Code Audit

- Verified that all `update` entity properties correctly map to the Meraki data model.
- Confirmed that discovery logic correctly instantiates the entity for all devices.

### Linting

- All files passed `ruff` (E501 line length issues resolved).

## Success Criteria Status

- [x] Users can see and trigger firmware updates natively in the HA UI.
- [x] Release notes (if available) are surfaced in the entity.
