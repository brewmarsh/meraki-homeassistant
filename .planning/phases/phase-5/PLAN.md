# Phase 5: Final Refinement & Stable Release Plan

## Overview

This final phase focuses on stabilizing the integration, standardizing versioning, improving diagnostic security, and expanding test coverage for a production-ready v1.0 release.

### Tasks

## Plan 05-01: Standardized Versioning & Diagnostic Redaction

**Wave**: 1

1. **Versioning**: Standardize the version to `v1.0.0` in `manifest.json`, `pyproject.toml`, and all internal constants.
2. **PII Redaction**: Update `diagnostics.py` to redact sensitive info (Organization IDs, Serial numbers, MAC addresses) using standard HA helper methods.

## Plan 05-02: Robust Error Handling

**Wave**: 1

1. **UpdateFailed Refactor**: Ensure all coordinators raise `homeassistant.exceptions.UpdateFailed` on API errors to provide clear "Unavailable" states in the UI.

## Plan 05-03: Quality Assurance & Test Coverage

**Wave**: 2

1. **Coverage Expansion**: Increase unit test coverage for `camera.py` and `appliance_port.py` to >90%.
2. **Doc Audit**: Perform a final audit of `README.md` and `docs/` to ensure all new features (Webhooks, Control services) are documented.

---

## Success Criteria

1. Version 1.0.0 is consistently reported project-wide.
2. Diagnostics do not contain unredacted PII.
3. All platform coordinators handle API outages gracefully.
4. Test coverage meets the target for critical modules.
