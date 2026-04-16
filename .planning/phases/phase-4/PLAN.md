# Phase 4: Advanced Control & Selective Stats Plan (Consolidated)

## Overview

Phase 4 focuses on active management capabilities (SSID/Client Control) and high-resolution telemetry (MX Uplinks, Camera Sense). This plan refines existing draft plans to ensure robust state management and real-time responsiveness via webhooks.

### Requirement Coverage

- **CTRL-01**: SSID toggle control (enable/disable).
- **CTRL-02**: Client blocking/allowlisting (Parental Controls).
- **CTRL-03**: Content filtering profile switching.
- **CTRL-04**: Selective bandwidth/throughput sensors (opt-in).
- **CTRL-05**: Uplink metrics sensors (latency, jitter, packet loss).
- **CTRL-06**: MV Camera RTSP streaming and Sense analytics.

---

## Wave 1: Reliable Management Controls

**Plan**: 04-01-PLAN.md
**Requirements**: CTRL-01, CTRL-02, CTRL-03

### Tasks

1. **Refactor Client Blocking State**:
   - Update `SsidFirewallCoordinator` to fetch current client policies or use the `MainCoordinator` data.
   - Ensure `MerakiClientBlockerSwitch` accurately reflects the "Blocked" vs "Normal" state from the API.
2. **SSID Management Hardening**:
   - Ensure `MerakiSSIDBaseSwitch` handles API timeouts and errors gracefully.
   - Implement state reversal on failure and verify state after successful updates.
3. **Content Filtering Profiles**:
   - Finalize `MerakiContentFilteringSelect` to support robust profile switching via category groups.

---

## Wave 2: Telemetry & Performance (Telemetry)

**Plan**: 04-02-PLAN.md
**Requirements**: CTRL-04, CTRL-05

### Tasks

1. **Optimize Uplink Performance**:
   - Ensure `getNetworkApplianceUplinksLossAndLatency` is the primary source for latency, jitter, and packet loss.
   - Handle timeseries data to provide the most recent high-resolution metrics.
2. **Verify Bandwidth Throughput**:
   - Confirm `MerakiBandwidthSensor` correctly calculates Mb/s from byte counts over a 60s window.
   - Ensure sensors are disabled by default (opt-in) to minimize database impact.

---

## Wave 3: Camera Webhook Integration (Real-time)

**Plan**: 04-03-PLAN.md
**Requirements**: CTRL-06

### Tasks

1. **Convert Camera Motion to Webhook-driven**:
   - Refactor `MerakiMotionSensor` to stop polling and instead react to `last_motion_event` from the coordinator.
2. **Add "Person Detected" Sensor**:
   - Implement `MerakiPersonSensor` for real-time person detection alerts via webhooks.
3. **Enhance Webhook Dispatching**:
   - Ensure `webhook.py` correctly updates the device models in the coordinator and triggers state refreshes.

---

## Success Criteria

1. Client blocking/unblocking works reliably and reflects state within 30s (or immediately on control).
2. SSID toggling is robust and self-corrects on failure.
3. MX Uplink performance metrics are accurate and updated via history endpoints.
4. Camera motion and person detection sensors update in real-time (<2s) via webhooks.
