# ROADMAP

## Phases

- [x] **Phase 1: Foundation & Discovery** - Config flow, API key validation, and hierarchical discovery.
- [x] **Phase 2: Coordinated Tracking & Monitoring** - Efficient bulk-polling for hardware status and client presence.
- [x] **Phase 3: Real-time Webhooks & Presence Optimization** - Sub-second updates and entity bloat prevention.
- [x] **Phase 4: Advanced Control & Selective Stats** - SSID/Client management and performance monitoring.
- [x] **Phase 5: Final Refinement & Stable Release** - Polish the integration for a stable release.
- [x] **Phase 6: Advanced Native Platforms** - Firmware management and maintenance services.
- [x] **Phase 7: Dual-Imager & Multi-Sensor Support** - Grouping imagers and handling Gen 3 camera features.

## Phase Details

...

### Phase 7: Dual-Imager & Multi-Sensor Support

**Goal**: Properly represent multi-imager cameras (like MV44X, MV84X) in HA as single devices with multiple camera entities.
**Depends on**: Phase 6
**Requirements**: CAM-01, CAM-02, CAM-03, CAM-04, CAM-05
**Success Criteria**:

1. Multi-sensor cameras appear as a single HA device.
2. Each imager has its own camera entity and analytics sensors.
3. MV44X ultra-wide view is correctly displayed.
   **Plans**: 2 plans

- [x] .planning/phases/phase-7/07-01-PLAN.md — Imager Grouping & Device Mapping
- [x] .planning/phases/phase-7/07-02-PLAN.md — Advanced Imager Features & Analytics

## Progress Table

| Phase                                         | Plans Complete | Status   | Completed  |
| --------------------------------------------- | -------------- | -------- | ---------- |
| 1. Foundation & Discovery                     | 2/2            | Complete | 2026-04-13 |
| 2. Coordinated Tracking & Monitoring          | 3/3            | Complete | 2026-04-14 |
| 3. Real-time Webhooks & Presence Optimization | 2/2            | Complete | 2026-04-14 |
| 4. Advanced Control & Selective Stats         | 3/3            | Complete | 2026-04-16 |
| 5. Final Refinement & Stable Release          | 3/3            | Complete | 2026-04-16 |
| 6. Advanced Native Platforms                  | 3/3            | Complete | 2026-04-17 |
| 7. Dual-Imager & Multi-Sensor Support         | 2/2            | Complete | 2026-04-27 |
