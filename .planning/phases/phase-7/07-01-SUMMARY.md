# Phase 7 Wave 1 Summary: Imager Grouping & Device Mapping

## Goal

Implement logic to group multi-sensor Meraki cameras (like MV44X and MV84X) into a single Home Assistant device while maintaining independent entities for each imager.

## Changes

### 1. Naming & Serial Utilities

- **Artifact**: `custom_components/meraki_ha/core/utils/naming_utils.py`
- **Logic**:
  - Added `MULTI_SENSOR_MODELS` registry.
  - Implemented `get_base_serial` to strip imager suffixes (`-1`, `-2`, etc.) from serial numbers for these models.
  - Updated `standardize_device_name` to strip imager suffixes from the common device name.
  - Updated `format_entity_name` to append `(Imager X)` to entity names for multi-sensor units, ensuring unique names across imagers of the same unit.

### 2. Device Registration

- **Artifact**: `custom_components/meraki_ha/helpers/device_info_helpers.py`
- **Logic**:
  - Modified `_resolve_physical_device_info` to use the base serial for the `DeviceInfo` identifiers when a multi-sensor model is detected.
  - This ensures that all imagers belonging to the same physical unit share the same `DeviceRegistry` entry in Home Assistant.

## Verification Results

### Logic Audit

- Verified that `get_base_serial("QXXX-XXXX-XXXX-1", "MV84X")` returns `"QXXX-XXXX-XXXX"`.
- Verified that `format_entity_name` for a multi-sensor camera now produces names like `"Meraki Lobby Camera (Imager 1)"`.
- Confirmed that standard single-imager models (e.g., MV63) remain unaffected.

### Tests

- Updated `tests/test_naming_standardization.py` with new test cases.

## Success Criteria Status

- [x] MV84X-1 and MV84X-2 share the same DeviceInfo identifiers.
- [x] Standard cameras (e.g., MV63) have unique DeviceInfo identifiers.
- [x] HA Device Registry shows one device for one physical multi-sensor unit.
