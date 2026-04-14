# Requirements

## v1.0 Milestone: Stable Release

### 1. Foundation & Discovery (FND)

| ID     | Requirement                                                            | Status   |
| ------ | ---------------------------------------------------------------------- | -------- |
| FND-01 | Config flow with API key and Organization ID validation.               | Existing |
| FND-02 | Hierarchical discovery of Meraki Organizations, Networks, and Devices. | Existing |
| FND-03 | Unified entity registry population across all platforms.               | Existing |

### 2. Monitoring & Presence (MON)

| ID     | Requirement                                                          | Status      |
| ------ | -------------------------------------------------------------------- | ----------- |
| MON-01 | Centralized bulk-polling using `DataUpdateCoordinator`.              | Existing    |
| MON-02 | `device_tracker` for wireless clients with MAC-based identification. | In Progress |
| MON-03 | `binary_sensor` for hardware health (AP, Switch, MX connectivity).   | Existing    |
| MON-04 | Async-safe SDK wrapping via `hass.async_add_executor_job`.           | Existing    |
| MON-05 | Rate limiting and async semaphore for API calls.                     | Existing    |

### 3. Real-time & Webhooks (WEB)

| ID     | Requirement                                                  | Status      |
| ------ | ------------------------------------------------------------ | ----------- |
| WEB-01 | Incoming Meraki Webhook handler for real-time presence.      | In Progress |
| WEB-02 | Automated Webhook registration with Meraki Dashboard.        | In Progress |
| WEB-03 | "Known Clients" filtering to manage MAC randomization bloat. | Planned     |
| WEB-04 | Webhook security and validation (secret verification).       | Existing    |

### 4. Control & Advanced Stats (CTRL)

| ID      | Requirement                                            | Status      |
| ------- | ------------------------------------------------------ | ----------- |
| CTRL-01 | SSID toggle control (enable/disable).                  | In Progress |
| CTRL-02 | Client blocking/allowlisting (Parental Controls).      | In Progress |
| CTRL-03 | Content filtering profile switching.                   | In Progress |
| CTRL-04 | Selective bandwidth/throughput sensors (opt-in).       | Planned     |
| CTRL-05 | Uplink metrics sensors (latency, jitter, packet loss). | In Progress |
| CTRL-06 | MV Camera RTSP streaming and Sense analytics.          | In Progress |

## Traceability

| Requirement | Phase   | Status  |
| ----------- | ------- | ------- |
| FND-01      | Phase 1 | Pending |
| FND-02      | Phase 1 | Pending |
| FND-03      | Phase 1 | Pending |
| MON-01      | Phase 2 | Pending |
| MON-02      | Phase 2 | Pending |
| MON-03      | Phase 2 | Pending |
| MON-04      | Phase 2 | Pending |
| MON-05      | Phase 2 | Pending |
| WEB-01      | Phase 3 | Pending |
| WEB-02      | Phase 3 | Pending |
| WEB-03      | Phase 3 | Pending |
| WEB-04      | Phase 3 | Pending |
| CTRL-01     | Phase 4 | Pending |
| CTRL-02     | Phase 4 | Pending |
| CTRL-03     | Phase 4 | Pending |
| CTRL-04     | Phase 4 | Pending |
| CTRL-05     | Phase 4 | Pending |
| CTRL-06     | Phase 4 | Pending |
