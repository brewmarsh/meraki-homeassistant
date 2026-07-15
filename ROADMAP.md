# ROADMAP

## Phases

- [x] **Phase 1: Foundation & Discovery** - Config flow, API key validation, and hierarchical discovery.
- [x] **Phase 2: Coordinated Tracking & Monitoring** - Efficient bulk-polling for hardware status and client presence.
- [x] **Phase 3: Real-time Webhooks & Presence Optimization** - Sub-second updates and entity bloat prevention.
- [x] **Phase 4: Advanced Control & Selective Stats** - SSID/Client management and performance monitoring.
- [x] **Phase 5: Final Refinement & Stable Release** - Polish the integration for a stable release.
- [x] **Phase 6: Advanced Native Platforms** - Firmware management and maintenance services.
- [x] **Phase 7: Dual-Imager & Multi-Sensor Support** - Grouping imagers and handling Gen 3 camera features.
- [ ] **Phase 8: Refactor Staging Test Deployment** - Consolidate tests and automate intelligent issue logging.

## Phase Details

### Phase 8: Refactor Staging Test Deployment

**Goal**: Modernize staging infrastructure to provide high-fidelity feedback with automated, deduplicated issue tracking.
**Depends on**: Phase 7
**Requirements**: STG-01, STG-02, STG-03, STG-04, STG-05
**Success Criteria**:

1. Single unified Python package handles all staging health checks.
2. All API interactions use the WebSocket protocol for consistency.
3. Failures are fingerprinted and either create new GitHub issues or comment on existing ones.
4. Noise from expected staging warnings is effectively filtered out.
   **Plans**: 1-2 plans

- [ ] .planning/phases/phase-8/08-01-PLAN.md — Test Consolidation & WebSocket Migration
- [ ] .planning/phases/phase-8/08-02-PLAN.md — Intelligent Issue Automation & Fingerprinting

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
| 8. Refactor Staging Test Deployment           | 0/2            | Planned  | TBD        |
