# Phase 3: Real-time Webhooks & Presence Optimization Plan

## Overview

This phase focuses on enabling sub-second presence updates via Meraki Webhooks and location scanning, while implementing filtering to prevent entity bloat from randomized MAC addresses.

### Requirement Coverage

- **WEB-01**: Incoming Meraki Webhook handler for real-time presence.
- **WEB-02**: Automated Webhook registration with Meraki Dashboard.
- **WEB-03**: "Known Clients" filtering to manage MAC randomization bloat.
- **WEB-04**: Webhook security and validation (secret verification).

---

## Plan 03-01: Webhook Infrastructure & Automation

**Wave**: 1
**Requirements**: WEB-01, WEB-02, WEB-04

### Tasks

1. **Dual-Mode Handler**: Update `webhook.py` to support `GET` (validator challenge) and `POST` (alert/scanning data) requests.
2. **Automated Registration**: Implement logic in `networks/alerts/settings` and `networks/locationScanning` to automatically register the Home Assistant webhook URL.
3. **Security Validation**: Ensure all incoming payloads are validated against the shared secret stored in the config entry.

---

## Plan 03-02: Presence Optimization & Integration

**Wave**: 2
**Depends on**: 03-01
**Requirements**: WEB-03

### Tasks

1. **MAC Filtering**: Implement the "Known Clients" filter in `device_tracker.py` using IEEE standards (second character check) to ignore randomized MACs.
2. **Real-time Integration**: Map incoming "Client connectivity changed" and Scanning API v3 events directly to `device_tracker` entity states.
3. **State Synthesis**: Implement logic to reconcile webhook events with polling data to prevent state oscillation.

---

## Success Criteria

1. Webhook validator challenge is successfully answered (HTTP 200 with challenge string).
2. Presence state updates in HA within 2 seconds of a Meraki connectivity alert.
3. "Passerby" devices with randomized MACs do not create persistent entities.
