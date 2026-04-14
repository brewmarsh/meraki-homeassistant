# Phase 4: Advanced Control & Selective Stats - Research

**Researched:** 2026-04-14
**Domain:** Meraki Control API, Network Telemetry, MV Sense Analytics
**Confidence:** HIGH

## Summary

Phase 4 focuses on advanced management capabilities and granular telemetry. While several "Advanced Control" entities (SSID toggles, Content Filtering, Client Blocking) exist in the codebase, research identifies significant reliability and feature gaps.

**Primary recommendation:** Refactor client blocking from IP-based firewall rules to MAC-based Client Policy API, and expand telemetry to include loss/latency and real-time Camera Sense events via webhooks.

## Phase Requirements

| ID      | Description                                            | Research Support                                                                                                           |
| ------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| CTRL-01 | SSID toggle control (enable/disable).                  | `MerakiSSIDEnabledSwitch` and `MerakiSSIDBroadcastSwitch` are verified in `switch/meraki_ssid_device_switch.py`.           |
| CTRL-02 | Client blocking/allowlisting (Parental Controls).      | Research confirms `PUT /networks/{networkId}/clients/{clientId}/policy` is the standard for MAC-based blocking.            |
| CTRL-03 | Content filtering profile switching.                   | `MerakiContentFilteringSelect` is verified in `meraki_select/meraki_content_filtering.py`.                                 |
| CTRL-04 | Selective bandwidth/throughput sensors (opt-in).       | `getNetworkApplianceUplinksUsageHistory` identified as the correct endpoint.                                               |
| CTRL-05 | Uplink metrics sensors (latency, jitter, packet loss). | `getDeviceLossAndLatencyHistory` and `getOrganizationDevicesUplinksLossAndLatency` identified as core telemetry endpoints. |
| CTRL-06 | MV Camera RTSP streaming and Sense analytics.          | RTSP is implemented; analytics exists via polling but lacks real-time webhook support for "Person detected".               |

## Standard Stack

### Core

| Library         | Version  | Purpose                 | Why Standard                                      |
| --------------- | -------- | ----------------------- | ------------------------------------------------- |
| `meraki`        | [latest] | Cisco Meraki Python SDK | Official SDK; handles rate limiting and async.    |
| `homeassistant` | [latest] | Integration Framework   | Native platform support (Switch, Sensor, Camera). |

### Supporting

| Library      | Version  | Purpose       | When to Use                                   |
| ------------ | -------- | ------------- | --------------------------------------------- |
| `braintrust` | [latest] | Observability | Used for tracing API calls in `MerakiClient`. |

## Architecture Patterns

### Recommended Project Structure

```
custom_components/meraki_ha/
├── sensor/
│   ├── device/
│   │   ├── appliance_uplink_metrics.py  # NEW: Latency/Loss/Jitter
│   │   └── data_usage.py               # Expand: Bandwidth usage
├── switch/
│   └── meraki_client_policy.py         # REFACTOR: MAC-based blocking
└── webhook.py                          # Expand: Camera Sense handling
```

### Pattern 1: MAC-based Client Policy

**What:** Use the Client Policy API instead of L3 Firewall rules.
**When to use:** For all client blocking/allowing (Parental Controls).
**Source:** [Cisco Meraki API Docs](https://developer.cisco.com/meraki/api-v1/#!update-network-client-policy)

### Anti-Patterns to Avoid

- **IP-based Blocking:** Avoid using IP addresses for blocking as they change via DHCP; always prefer MAC-based identification.
- **High-Frequency Polling for Camera:** Avoid polling `/analytics/recent` faster than 1 minute; use Webhooks for real-time person detection.

## Don't Hand-Roll

| Problem          | Don't Build       | Use Instead           | Why                                                                            |
| ---------------- | ----------------- | --------------------- | ------------------------------------------------------------------------------ |
| Client Blocking  | L3 Firewall Rules | Client Policy API     | IP volatility makes firewall rules unreliable for clients.                     |
| Throughput Calc  | Custom counters   | `UplinksUsageHistory` | Meraki already calculates these metrics; rolling custom ones causes API bloat. |
| Motion Detection | Pixel analysis    | MV Sense              | Meraki MV does edge-based person/vehicle detection.                            |

## Common Pitfalls

### Pitfall 1: Track-by-IP Network Settings

**What goes wrong:** Client policy API fails or applies to the wrong device.
**Why it happens:** Some networks are configured to "Track-by-IP" instead of MAC.
**How to avoid:** Detect network settings or warn user that MAC-based tracking is required for reliable control.

### Pitfall 2: MX NAT for MR Clients

**What goes wrong:** Blocking a wireless client on the MX fails.
**Why it happens:** If using MR NAT mode, the MX only sees the AP's MAC/IP.
**How to avoid:** Policies should ideally be applied at the Organization or Network level where Meraki handles the hierarchy.

## Code Examples

### MAC-based Client Policy Update

```python
# Source: Meraki API Documentation
await dashboard.networks.updateNetworkClientPolicy(
    networkId,
    clientMac,
    devicePolicy='Blocked' # or 'Normal', 'Whitelisted'
)
```

### Uplink Loss & Latency

```python
# Source: Meraki API Documentation
performance = await dashboard.appliance.getNetworkApplianceUplinksLossAndLatency(
    networkId,
    timespan=60
)
# Returns list of {uplink, ip, timeSeries: [{latencyMs, lossPercent}]}
```

## Assumptions Log

| #   | Claim                                                                   | Section      | Risk if Wrong                                    |
| --- | ----------------------------------------------------------------------- | ------------ | ------------------------------------------------ |
| A1  | `updateNetworkClientPolicy` works for clients not currently connected.  | Architecture | Policy might fail if client has never been seen. |
| A2  | "Person detected" webhooks include necessary metadata for state update. | CTRL-06      | If payload is too sparse, we still need polling. |

## Environment Availability

| Dependency | Required By | Available | Version | Fallback          |
| ---------- | ----------- | --------- | ------- | ----------------- |
| Meraki SDK | Core API    | ✓         | 1.48.0  | —                 |
| public_url | Webhooks    | ✓         | —       | Polling-only mode |

## Validation Architecture

### Test Framework

| Property          | Value                                               |
| ----------------- | --------------------------------------------------- |
| Framework         | pytest                                              |
| Config file       | pytest.ini                                          |
| Quick run command | `pytest tests/switch/test_meraki_client_blocker.py` |

### Phase Requirements → Test Map

| Req ID  | Behavior       | Test Type | Automated Command                                       | File Exists?        |
| ------- | -------------- | --------- | ------------------------------------------------------- | ------------------- |
| CTRL-01 | SSID Toggle    | unit      | `pytest tests/switch/test_meraki_ssid_device_switch.py` | ✅                  |
| CTRL-02 | Client Policy  | unit      | `pytest tests/switch/test_meraki_client_blocker.py`     | ✅ (Needs Refactor) |
| CTRL-05 | Uplink Metrics | unit      | `pytest tests/sensor/test_uplink_performance.py`        | ✅ (Partial)        |

## Security Domain

### Applicable ASVS Categories

| ASVS Category       | Applies | Standard Control                     |
| ------------------- | ------- | ------------------------------------ |
| V5 Input Validation | yes     | Voluptuous schemas in `services/`    |
| V6 Cryptography     | yes     | Shared Secret for Webhook validation |

### Known Threat Patterns for Meraki

| Pattern          | STRIDE                 | Standard Mitigation                 |
| ---------------- | ---------------------- | ----------------------------------- |
| Webhook Spoofing | Spoofing               | Validate `sharedSecret` in payload. |
| API Key Leak     | Information Disclosure | Store in HA Secrets / Config Entry. |

## Sources

### Primary (HIGH confidence)

- Meraki API Documentation (Clients, Appliance Uplinks, MV Sense).
- Existing codebase (`custom_components/meraki_ha/`).

### Secondary (MEDIUM confidence)

- Community forum discussions on Meraki MQTT vs Webhooks.

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH - Using official SDK.
- Architecture: HIGH - Patterns align with existing integration structure.
- Pitfalls: MEDIUM - Dependent on specific Meraki dashboard configurations.

**Research date:** 2026-04-14
**Valid until:** 2026-05-14
