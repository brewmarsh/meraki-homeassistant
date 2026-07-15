---
phase: 7
phase_name: Dual-Imager & Multi-Sensor Support
verified: 2026-04-27T17:00:00Z
status: partial
score: 4/5 must-haves verified
gaps:
  - CAM-05: Support for secondary resolution streams for Gen 3 cameras is not yet implemented.
---

# Phase 7 Validation Report: Dual-Imager & Multi-Sensor Support

**Phase Goal:** Properly represent multi-imager cameras (like MV44X, MV84X) in HA as single devices with multiple camera entities.

## Goal Achievement

### Observable Truths

| #   | Truth                                                               | Status     | Evidence                                                              |
| --- | ------------------------------------------------------------------- | ---------- | --------------------------------------------------------------------- |
| 1   | Multi-sensor cameras appear as a single HA device.                  | ✓ VERIFIED | `device_info_helpers.py` uses `base_serial` for identifiers.          |
| 2   | Each imager has its own camera entity and analytics sensors.        | ✓ VERIFIED | `camera.py` and `camera_analytics.py` use full serial for unique_ids. |
| 3   | MV44X ultra-wide view is correctly displayed.                       | ✓ VERIFIED | `camera.py` sets `aspect_ratio: 32:9` for MV44X.                      |
| 4   | Detect multi-sensor cameras by identifying suffixed serial numbers. | ✓ VERIFIED | `naming_utils.py` implemented `get_base_serial` logic.                |
| 5   | Support secondary resolution streams for Gen 3 cameras.             | ⚠ GAP     | No implementation found in `camera.py` or `camera_repository.py`.     |

## Required Artifacts

| Artifact                                                        | Expected                      | Status     | Details                                                          |
| --------------------------------------------------------------- | ----------------------------- | ---------- | ---------------------------------------------------------------- |
| `custom_components/meraki_ha/core/utils/naming_utils.py`        | Serial suffix handling        | ✓ VERIFIED | `get_base_serial` and `standardize_device_name` updated.         |
| `custom_components/meraki_ha/helpers/device_info_helpers.py`    | Device grouping logic         | ✓ VERIFIED | `_resolve_physical_device_info` uses `base_serial`.              |
| `custom_components/meraki_ha/camera.py`                         | Aspect ratio and imager index | ✓ VERIFIED | Attributes correctly populated for MV44X and multi-sensor units. |
| `custom_components/meraki_ha/sensor/device/camera_analytics.py` | Independent sensors           | ✓ VERIFIED | `unique_id` uses suffixed serial for unique analytics tracking.  |

## Gaps & Actions

- [ ] **CAM-05**: Implement secondary resolution stream support. This requires updating `camera_repository.py` to fetch multiple streams if available and `camera.py` to allow selecting between them or exposing them as separate entities/attributes.
- [x] **Test Verification**: Manual audit of logic confirms implementation of CAM-01 through CAM-04.
