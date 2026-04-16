# Phase 2: Coordinated Tracking & Monitoring Plan

## Overview

This phase focuses on consolidating the current fragmented polling architecture into a unified `DataUpdateCoordinator` system, implementing a dedicated `device_tracker` platform for wireless clients, and enhancing API resilience through centralized rate-limiting.

### Requirement Coverage

- **MON-01**: Centralized bulk-polling using `DataUpdateCoordinator`.
- **MON-02**: `device_tracker` for wireless clients with MAC-based identification.
- **MON-03**: `binary_sensor` for hardware health (AP, Switch, MX connectivity).
- **MON-04**: Async-safe SDK wrapping via `hass.async_add_executor_job`.
- **MON-05**: Rate limiting and async semaphore for API calls.

---

## Plan 02-01: Coordinator Unification & Rate Limiting

**Wave**: 1
**Requirements**: MON-01, MON-04, MON-05

### Tasks

1. **Consolidate Coordinators**: Refactor `custom_components/meraki_ha/coordinators/` to use a tiered polling strategy within `MerakiMainCoordinator`. Fast poll (30s) for device/client status, Slow poll (10m) for configuration and static metadata.
2. **Centralized Throttling**: Update `MerakiClient` in `core/api/client.py` to use a more robust semaphore and implement a priority queue for API requests to ensure real-time updates (like webhooks) aren't blocked by bulk polls.
3. **Async Safety Audit**: Ensure all Meraki SDK calls are strictly wrapped in `async_add_executor_job` or use the `aio` SDK exclusively with proper error handling for 429 and 5xx responses.

---

## Plan 02-02: Device Tracker Platform & Client Migration

**Wave**: 2
**Depends on**: 02-01
**Requirements**: MON-02

### Tasks

1. **Initialize Platform**: Create `custom_components/meraki_ha/device_tracker.py` and register `PLATFORM_DEVICE_TRACKER` in `const/platform.py`.
2. **Client Migration**: Migrate the MAC-based client tracking logic from `sensor/client_tracker.py` to the new `device_tracker` platform. Implement `SeeCallback` or direct entity state management using the unified coordinator data.
3. **Discovery Wiring**: Update `discovery/service.py` to correctly route discovered wireless clients to the `device_tracker` platform instead of creating sensors.

---

## Plan 02-03: Hardware Connectivity Binary Sensors

**Wave**: 2
**Depends on**: 02-01
**Requirements**: MON-03

### Tasks

1. **Status Sensors**: Implement `MerakiConnectivityBinarySensor` in `binary_sensor/device/status.py`. This sensor will map Meraki device status (`online`, `alerting`, `offline`) to HA binary states (`on`/`off`).
2. **Mass Registration**: Update `discovery/service.py` to ensure every discovered Meraki hardware device (AP, MS, MX) receives a connectivity sensor.
3. **State Verification**: Add unit tests in `tests/binary_sensor/test_device_status.py` to verify that state changes in the coordinator data correctly reflect in the binary sensor state and availability.

---

## Success Criteria

1. Integration uses a single primary polling loop with tiered intervals.
2. Wireless clients appear as `device_tracker` entities with correct MAC and IP attributes.
3. Every Meraki hardware device has a reliable "Connectivity" binary sensor.
4. No 429 "Too Many Requests" errors occur during a standard 100-client stress test.
