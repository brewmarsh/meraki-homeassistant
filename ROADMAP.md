# ROADMAP

## Phases

- [ ] **Phase 1: Foundation & Discovery** - Config flow, API key validation, and hierarchical discovery.
- [ ] **Phase 2: Coordinated Tracking & Monitoring** - Efficient bulk-polling for hardware status and client presence.
- [ ] **Phase 3: Real-time Webhooks & Presence Optimization** - Sub-second updates and entity bloat prevention.
- [ ] **Phase 4: Advanced Control & Selective Stats** - SSID/Client management and performance monitoring.
- [ ] **Phase 5: Final Refinement & Stable Release** - Polish the integration for a stable release.

## Phase Details

### Phase 1: Foundation & Discovery

**Goal**: Establish secure connectivity and map the Meraki cloud hierarchy to local Home Assistant devices.
**Depends on**: None
**Requirements**: FND-01, FND-02, FND-03
**Success Criteria**:

1. User can successfully complete the config flow using a valid API key.
2. Meraki Organizations and Networks appear correctly as Devices in Home Assistant.
3. Integration setup does not block the Home Assistant event loop.
   **Plans**: 2 plans

- [ ] .planning/phases/01-foundation-discovery/01-01-PLAN.md — Core Async & Multi-step Flow
- [ ] .planning/phases/01-foundation-discovery/01-02-PLAN.md — Integration Lifecycle & Discovery Coordinator
      **UI hint**: yes

### Phase 2: Coordinated Tracking & Monitoring

**Goal**: Provide core monitoring value using a resilient polling architecture.
**Depends on**: Phase 1
**Requirements**: MON-01, MON-02, MON-03, MON-04, MON-05
**Success Criteria**:

1. Hardware status (Online/Offline) updates within 30 seconds of a change.
2. Wireless clients are correctly tracked as `device_tracker` entities.
3. API rate limiting is handled gracefully without 429 errors.
   **Plans**: TBD

### Phase 3: Real-time Webhooks & Presence Optimization

**Goal**: Upgrade presence detection to real-time and ensure registry stability.
**Depends on**: Phase 2
**Requirements**: WEB-01, WEB-02, WEB-03, WEB-04
**Success Criteria**:

1. Client presence events reflect in HA within 2 seconds via webhooks.
2. "Known Clients" filter prevents entity bloat from randomized MAC addresses.
3. Webhook listener securely validates incoming Meraki payloads.
   **Plans**: TBD
   **UI hint**: yes

### Phase 4: Advanced Control & Selective Stats

**Goal**: Enable network management capabilities and high-resolution performance data.
**Depends on**: Phase 3
**Requirements**: CTRL-01, CTRL-02, CTRL-03, CTRL-04, CTRL-05, CTRL-06
**Success Criteria**:

1. User can toggle SSIDs and manage content filtering from the HA UI.
2. Client blocking/unblocking services work reliably.
3. Bandwidth and uplink metrics provide actionable data without performance degradation.
   **Plans**: 3 plans

- [ ] 04-01-PLAN.md — Advanced Management Controls (SSID & Client Policy)
- [ ] 04-02-PLAN.md — Network Performance Telemetry (Uplink Metrics & Usage)
- [ ] 04-03-PLAN.md — Camera Sense Webhook Integration
      **UI hint**: yes

### Phase 5: Final Refinement & Stable Release

**Goal**: Polish the integration for a stable release.
**Depends on**: Phase 4
**Requirements**: STB-01, STB-02, STB-03
**Success Criteria**:

1. Standardized versioning to v1.0.0 across all manifests and configs.
2. Implement PII redaction in diagnostics.py.
3. Improve test coverage for camera.py and appliance_port.py.
4. Refine error handling in coordinators to use standard Home Assistant UpdateFailed.
   **Plans**: 3 plans

- [ ] 05-01-PLAN.md — Stable v1.0.0 & Secure Diagnostics
- [ ] 05-02-PLAN.md — Resilient Coordinator Error Handling
- [ ] 05-03-PLAN.md — Quality Scale Coverage Optimization

## Progress Table

| Phase                                         | Plans Complete | Status      | Completed |
| --------------------------------------------- | -------------- | ----------- | --------- |
| 1. Foundation & Discovery                     | 0/2            | In Progress | -         |
| 2. Coordinated Tracking & Monitoring          | 0/1            | Not started | -         |
| 3. Real-time Webhooks & Presence Optimization | 0/1            | Not started | -         |
| 4. Advanced Control & Selective Stats         | 0/3            | Not started | -         |
| 5. Final Refinement & Stable Release          | 0/3            | Not started | -         |
