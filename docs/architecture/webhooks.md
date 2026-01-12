# Webhook Implementation & Monitoring

**Version:** 3.2.0
**Status:** Production Ready

This document describes the comprehensive webhook implementation for the Meraki Home Assistant integration, including real-time alerts, targeted API refresh, adaptive polling, and monitoring capabilities.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Configuration](#configuration)
5. [Monitoring & Observability](#monitoring--observability)
6. [Alert Types](#alert-types)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The webhook implementation enables real-time event notifications from the Meraki Cloud Dashboard, eliminating the need for constant polling and providing instant visibility into network changes.

### Key Benefits

- **Real-time Updates:** Instant notification of device status changes, network events, and client activity
- **API Efficiency:** 85% reduction in API calls (54 → 8 calls/hour) when webhooks are active
- **Targeted Refresh:** Single-entity API calls instead of full dataset polling
- **Adaptive Polling:** Automatic reduction of polling intervals when webhooks are healthy
- **Bidirectional Sync:** Push Home Assistant device names to Meraki Dashboard for easy identification

---

## Features

### 1. Webhook Alert Support

Handles all Meraki alert types:

- **Device Alerts:** APs/Switches/Gateways/Cameras/Sensors up/down/rebooted
- **Client Alerts:** Connectivity changes, new clients, blocked clients
- **Network Alerts:** SSID/VLAN/Firewall configuration changes
- **Security Alerts:** Rogue AP, intrusion, malware detection
- **Environmental Alerts:** MT sensor threshold alerts (temperature, humidity, water, door, power)

### 2. Auto-Configuration

Automatically registers webhooks in Meraki Dashboard:

1. Creates HTTP server endpoints per network
2. Subscribes to selected alert types
3. Handles read-only API keys with manual setup instructions

### 3. Targeted API Refresh

Instead of polling all data, webhook alerts trigger targeted refresh for only the affected entity:

- **Device Refresh:** Single device status update (5-second delay for cloud propagation)
- **Client Refresh:** Single client details update
- **Network Refresh:** Network configuration update
- **SSID Refresh:** Wireless SSID list update

**Debouncing:** Multiple alerts for the same entity within 5 seconds are consolidated into a single API call.

### 4. Adaptive Polling Reduction

When webhooks are active (received within last 15 minutes), polling intervals automatically reduce:

| Data Type | Default | With Webhooks | Reduction |
| --------- | ------- | ------------- | --------- |
| Networks  | 30 min  | 6 hours       | 12x       |
| Devices   | 10 min  | 1 hour        | 6x        |
| Clients   | 90 sec  | 10 min        | 6.7x      |
| SSIDs     | 10 min  | 1 hour        | 6x        |

**API Call Reduction:** 85% fewer calls (46 calls/hour saved)

### 5. Bidirectional Sync

Push Home Assistant device names to Meraki Dashboard:

- **Manual Sync:** `meraki_ha.sync_client_names` service
- **Auto-Sync:** Automatic sync when new clients connect (configurable)
- **Hierarchy Traversal:** Finds root device names (e.g., "SunPower Gateway" instead of "Panel A1")
- **Flexible Formatting:** Include model and/or software version in synced names

---

## Architecture

### Data Flow

```text
┌─────────────────────────────────────────────────────────────────┐
│                     MERAKI CLOUD                                │
└───────────────────────┬─────────────────────────────────────────┘
                        │
          ┌─────────────┼─────────────────┐
          ▼             ▼                 ▼
   ┌──────────┐  ┌──────────┐      ┌───────────┐
   │ Webhooks │  │ Scanning │      │ Polling   │
   │(instant) │  │   API    │      │ (reduced) │
   └────┬─────┘  └────┬─────┘      └─────┬─────┘
        │             │                  │
        │  Targeted   │ Real-time        │ Reconciliation
        │  API call   │ RSSI/Location    │ only
        │             │                  │
        └─────────────┼──────────────────┘
                      ▼
          ┌───────────────────────┐
          │  MerakiDataCoordinator │
          │  • Immediate state    │
          │  • Targeted refresh   │
          │  • Deduplication      │
          └───────────┬───────────┘
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
┌──────────┐   ┌──────────┐   ┌───────────┐
│ Entities │   │ Frontend │   │  Sync →   │
│          │   │  Panel   │   │  Meraki   │
└──────────┘   └──────────┘   └───────────┘
```

### Components

| Component                      | Location           | Purpose                                          |
| ------------------------------ | ------------------ | ------------------------------------------------ |
| **webhook.py**                 | Main handler       | Routes incoming webhooks to alert handlers       |
| **webhook_manager.py**         | Registration       | Auto-registers webhooks in Meraki Dashboard      |
| **handlers/\***                | Alert processors   | Device, client, network, security, sensor alerts |
| **meraki_data_coordinator.py** | State management   | Targeted refresh, polling reduction, metrics     |
| **helpers/sync_helper.py**     | Bidirectional sync | Device name traversal and provisioning           |

### Security

- **HTTPS Required:** Webhook URL must use HTTPS
- **Shared Secret:** All incoming webhooks validated against configured secret
- **Local Address Detection:** Rejects local/private IP addresses
- **Auto-Generated Secrets:** 32-character hex string if not provided

---

## Configuration

### Enable Webhooks

**UI Path:** Settings > Devices & Services > Meraki > Configure > Webhooks

```yaml
enable_webhooks: true
webhook_auto_register: true
webhook_polling_reduction: true
webhook_alert_types:
  - 'APs went down'
  - 'APs came up'
  - 'Switches went down'
  - 'Switches came up'
  - 'Client connectivity changed'
  - 'SSID settings changed'
  # ... select desired alert types
```

### Configuration Options

| Option                      | Default | Description                                        |
| --------------------------- | ------- | -------------------------------------------------- |
| `enable_webhooks`           | `false` | Master toggle for webhook functionality            |
| `webhook_auto_register`     | `true`  | Auto-create HTTP servers in Dashboard              |
| `webhook_polling_reduction` | `true`  | Reduce polling when webhooks active                |
| `webhook_external_url`      | (empty) | Custom webhook URL (uses HA external URL if empty) |
| `webhook_shared_secret`     | (auto)  | Secret for validation (auto-generated if empty)    |
| `webhook_alert_types`       | `[]`    | List of alert types to subscribe                   |

### Bidirectional Sync Options

| Option                 | Default | Description                          |
| ---------------------- | ------- | ------------------------------------ |
| `sync_names_to_meraki` | `false` | Enable name sync to Meraki           |
| `sync_include_model`   | `true`  | Include device model in name         |
| `sync_include_version` | `false` | Include software version in name     |
| `sync_on_new_client`   | `true`  | Auto-sync when new client discovered |

### Read-Only API Key Handling

If auto-registration fails due to read-only API key, manual setup instructions are displayed in the UI:

1. Go to Network-wide > Alerts > HTTP Servers
2. Add new server with provided URL and shared secret
3. Go to Network-wide > Alerts > Alert settings
4. Enable desired alerts and assign to your HTTP server

---

## Monitoring & Observability

### Diagnostic Entities

#### Webhook Health Sensor

**Entity:** `binary_sensor.webhook_health`
**State:** ON = Healthy (webhooks received in last 15 minutes)

**Attributes:**

- `total_received` - Total webhook count
- `last_received` - ISO timestamp of last webhook
- `webhook_freshness_seconds` - Age in seconds
- `last_received_ago` - Human-readable (e.g., "5 minutes ago")
- `registered_networks` - Number of networks with webhooks
- `polling_reduction_active` - Whether reduced polling is active
- `has_registration_errors` - Boolean error indicator
- `status_message` - Detailed status from webhook manager

#### Webhook Received Total

**Entity:** `sensor.webhook_received_total`
**State:** Total number of webhooks received (counter)

**Attributes:**

- `by_alert_type` - Breakdown of counts by alert type

#### Webhook Processing Duration

**Entity:** `sensor.webhook_processing_duration`
**State:** Average processing time in milliseconds

**Attributes:**

- `min_ms` / `max_ms` / `avg_ms` - Basic statistics
- `p50_ms` / `p95_ms` / `p99_ms` - Percentiles
- `slow_webhooks_count` - Count of webhooks >1000ms
- `slow_webhooks_percent` - Percentage of slow webhooks

#### API Targeted Refresh Total

**Entity:** `sensor.api_targeted_refresh_total`
**State:** Total targeted API refresh calls (counter)

**Attributes:**

- `by_type` - Breakdown (device/client/network/ssid)
- `success_count` / `failure_count` - Success/failure tracking
- `success_rate` - Success percentage
- `estimated_api_calls_saved_per_hour` - Efficiency metric (46)

### Automation Examples

**Health Monitoring:**

```yaml
automation:
  - alias: 'Webhook Health Alert'
    trigger:
      platform: state
      entity_id: binary_sensor.webhook_health
      to: 'off'
      for: { minutes: 15 }
    action:
      service: notify.admin
      data:
        message: 'Meraki webhooks unhealthy for 15 minutes'
```

**Performance Monitoring:**

```yaml
automation:
  - alias: 'Slow Webhook Processing'
    trigger:
      platform: numeric_state
      entity_id: sensor.webhook_processing_duration
      attribute: p95_ms
      above: 1000
      for: { minutes: 5 }
    action:
      service: persistent_notification.create
      data:
        title: 'Slow Webhook Processing'
        message: 'P95 processing time > 1 second'
```

---

## Alert Types

### Device Alerts

| Alert Type           | Trigger           | Action                                    |
| -------------------- | ----------------- | ----------------------------------------- |
| APs went down        | AP offline        | Immediate status update, targeted refresh |
| APs came up          | AP online         | Immediate status update, targeted refresh |
| Switches went down   | Switch offline    | Immediate status update, targeted refresh |
| Switches came up     | Switch online     | Immediate status update, targeted refresh |
| Gateways went down   | Appliance offline | Immediate status update, targeted refresh |
| Gateways came up     | Appliance online  | Immediate status update, targeted refresh |
| Cameras went down    | Camera offline    | Immediate status update, targeted refresh |
| Cameras came up      | Camera online     | Immediate status update, targeted refresh |
| Sensors went offline | MT sensor offline | Immediate status update, targeted refresh |
| Sensors came online  | MT sensor online  | Immediate status update, targeted refresh |
| Device rebooted      | Device restart    | Immediate status update, targeted refresh |

### Client Alerts

| Alert Type                  | Trigger                     | Action                                              |
| --------------------------- | --------------------------- | --------------------------------------------------- |
| Client connectivity changed | Client connects/disconnects | State update, debounced refresh, optional auto-sync |
| New client connected        | New device on network       | State update, debounced refresh, optional auto-sync |
| Client blocked              | Client denied access        | State update, debounced refresh                     |

### Network Configuration Alerts

| Alert Type            | Trigger               | Action                      |
| --------------------- | --------------------- | --------------------------- |
| SSID settings changed | SSID modified         | Debounced SSID list refresh |
| VLAN settings changed | VLAN modified         | Debounced network refresh   |
| Firewall rule changed | Firewall modified     | Debounced network refresh   |
| Settings changed      | Generic config change | Debounced network refresh   |

### Security Alerts

| Alert Type         | Trigger          | Action                                   |
| ------------------ | ---------------- | ---------------------------------------- |
| Rogue AP detected  | Unauthorized AP  | Fire HA event, optional targeted refresh |
| Intrusion detected | IDS/IPS trigger  | Fire HA event, optional targeted refresh |
| Malware detected   | Threat detection | Fire HA event, optional targeted refresh |

### Environmental Sensor Alerts

| Alert Type                     | Trigger                  | Action                                  |
| ------------------------------ | ------------------------ | --------------------------------------- |
| Temperature threshold exceeded | MT sensor temp alert     | Fire HA event, debounced sensor refresh |
| Humidity threshold exceeded    | MT sensor humidity alert | Fire HA event, debounced sensor refresh |
| Water detected                 | MT12 water sensor        | Fire HA event, debounced sensor refresh |
| Door opened/closed             | MT20 door sensor         | Fire HA event, debounced sensor refresh |
| Power outage detected          | MT40 power monitor       | Fire HA event, debounced sensor refresh |

---

## Testing

### E2E Integration Tests

**File:** `tests/test_webhook_e2e.py`

Comprehensive end-to-end tests covering:

- Device down webhook flow → targeted device refresh
- Client connectivity webhook → debounced client refresh
- Duplicate webhook deduplication via alertId
- SSID settings changed → network refresh
- Security alerts → HA event firing
- Invalid payload graceful handling
- Polling reduction activation

**Test Results:**

```bash
$ uv run pytest tests/test_webhook_e2e.py -v
======================== 7 passed in 0.11s ========================
```

### Test Coverage

- **Unit Tests:** `tests/test_webhook.py` - URL validation, registration, secret validation
- **Handler Tests:** `tests/handlers/test_*.py` - Individual alert type handling
- **Coordinator Tests:** `tests/test_coordinator_debounce.py` - Deduplication logic
- **Integration Tests:** `tests/test_webhook_e2e.py` - Complete flows

---

## Troubleshooting

### Webhook Health Shows "Off"

**Possible Causes:**

1. Webhooks not registered in Meraki Dashboard
2. Firewall blocking incoming webhooks
3. Invalid shared secret mismatch
4. HTTPS certificate issues
5. External URL not configured or unreachable

**Debug Steps:**

1. **Enable debug logging:**

   ```yaml
   logger:
     logs:
       custom_components.meraki_ha.alerts: debug
   ```

2. **Check webhook status attributes:**

   ```yaml
   {{ state_attr('binary_sensor.webhook_health', 'status_message') }}
   {{ state_attr('binary_sensor.webhook_health', 'registration_errors') }}
   {{ state_attr('binary_sensor.webhook_health', 'registered_networks') }}
   ```

3. **Verify webhook URL is reachable from internet:**

   - Must be HTTPS
   - Must be public (not local/private IP)
   - Valid SSL certificate

4. **Check Meraki Dashboard:**
   - Network-wide > Alerts > HTTP Servers
   - Verify server is listed and URL matches
   - Check alert subscriptions point to your server

### High Processing Duration

**Causes:**

- Network latency between Meraki Cloud and HA instance
- Slow API responses during targeted refresh
- Large number of concurrent webhooks
- Resource constraints on HA host

**Resolution:**

1. **Check percentiles:**

   ```yaml
   {{ state_attr('sensor.webhook_processing_duration', 'p95_ms') }}
   {{ state_attr('sensor.webhook_processing_duration', 'p99_ms') }}
   ```

2. **Review failure rate:**

   ```yaml
   {{ state_attr('sensor.api_targeted_refresh_total', 'success_rate') }}
   ```

3. **Increase debounce window if needed** (edit coordinator settings)

### Low API Call Savings

**Causes:**

- Webhooks not enabled for all networks
- Polling reduction disabled in settings
- Webhook freshness expired (>15 minutes since last webhook)
- Limited alert type subscriptions

**Resolution:**

1. **Verify polling reduction active:**

   ```yaml
   {{ state_attr('binary_sensor.webhook_health', 'polling_reduction_active') }}
   ```

2. **Check registered networks:**

   ```yaml
   {{ state_attr('binary_sensor.webhook_health', 'registered_networks') }}
   ```

3. **Review subscribed alert types:**

   ```yaml
   {{ state_attr('binary_sensor.webhook_health', 'subscribed_alert_types') }}
   ```

### Bidirectional Sync Not Working

**Causes:**

- Sync disabled in configuration
- No matching HA devices found (by MAC address)
- Network ID missing in client data

**Resolution:**

1. **Verify sync enabled:**
   Check Options > Data Sync > "Sync names to Meraki"

2. **Test manual sync:**

   ```yaml
   service: meraki_ha.sync_client_names
   ```

3. **Check logs for sync candidates:**
   Enable debug logging for coordinator

---

## Performance Metrics

### API Call Reduction (60-minute window)

| Metric    | Without Webhooks | With Webhooks | Reduction |
| --------- | ---------------- | ------------- | --------- |
| Networks  | 2 calls          | 0.17 calls    | 91%       |
| Devices   | 6 calls          | 1 call        | 83%       |
| Clients   | 40 calls         | 6 calls       | 85%       |
| SSIDs     | 6 calls          | 1 call        | 83%       |
| **Total** | **54 calls**     | **~8 calls**  | **85%**   |

### Memory Overhead

- **Metrics Storage:** ~40KB (last 1000 webhook duration samples)
- **Deduplication Cache:** ~10KB (300-second TTL, auto-cleanup)
- **Debounce Tracking:** ~5KB (pending refresh keys)

### CPU Overhead

- **Per Webhook:** <1ms for metrics collection
- **Targeted Refresh:** 5-second delay + API call time
- **Deduplication Check:** <0.1ms (dict lookup)

---

## Additional Resources

- **API Documentation:** [Meraki Dashboard API](https://developer.cisco.com/meraki/api-v1/)
- **Webhook Guide:** [Meraki Webhooks Overview](https://developer.cisco.com/meraki/webhooks/)
- **Alert Types:** [Meraki Alert Types Reference](https://developer.cisco.com/meraki/webhooks/#alert-types)

---

**Document Version:** 3.2.0
**Last Updated:** 2026-01-12
**Status:** Production Ready
