# Feature Landscape

**Domain:** Network Device Hubs (Meraki, Unifi, etc.)
**Researched:** February 2025

## Table Stakes

Features users expect in a network integration.

| Feature                    | Why Expected                           | Complexity | Notes                                          |
| -------------------------- | -------------------------------------- | ---------- | ---------------------------------------------- |
| Presence Detection         | Primary use case for network trackers. | Low        | Mac-based tracking via `DeviceTrackerEntity`.  |
| Client List                | Visibility of all connected devices.   | Medium     | Needs efficient handling for 1000+ clients.    |
| Access Point/Device Status | Monitoring of network hardware.        | Low        | Simple online/offline binary sensors.          |
| Network Stats (RX/TX)      | Bandwidth monitoring.                  | Medium     | High event volume; needs selective enablement. |

## Differentiators

Features that add high value beyond simple tracking.

| Feature                   | Value Proposition                                  | Complexity | Notes                                         |
| ------------------------- | -------------------------------------------------- | ---------- | --------------------------------------------- |
| Real-time Webhooks        | Sub-second presence updates without polling.       | High       | Requires public endpoint or tunnel.           |
| SSIDs/VLAN Control        | Enabling/disabling guest networks via switch.      | Medium     | API-driven configuration change.              |
| Intelligent Rate Limiting | Handling high-volume client changes without lag.   | Medium     | Batching and throttling logic in coordinator. |
| Client Metadata Sync      | Fetching device names/types from Meraki Dashboard. | Low        | Enrichment of HA entities.                    |

## Anti-Features

Features to explicitly NOT build to maintain stability.

| Anti-Feature                     | Why Avoid                                  | What to Do Instead                                         |
| -------------------------------- | ------------------------------------------ | ---------------------------------------------------------- |
| Tracking ALL clients by default  | Guest/transient devices will bloat the DB. | Disable "Track new clients" by default.                    |
| Per-entity individual polling    | Hits API rate limits for large setups.     | Use `DataUpdateCoordinator` for bulk fetching.             |
| Real-time bandwidth charts in HA | Too much state history overhead.           | Recommend Grafana or Meraki Dashboard for granular charts. |

## Feature Dependencies

```
Core Integration → Device Discovery → Device Tracking (Presence)
Webhooks (Optional) → Real-time Presence
Config Flow → Meraki API Access → Entities Initialization
```

## MVP Recommendation

Prioritize:

1. **Core Integration**: Config flow with API key.
2. **Device Discovery**: Efficient listing of organizations/networks/devices.
3. **Presence Detection**: MAC-based `DeviceTrackerEntity` for identified clients.
4. **Hardware Status**: Binary sensors for AP/Switch connectivity.

Defer:

- **SSID Switching**: Secondary feature.
- **Advanced Stats**: High database overhead, defer to post-MVP.

## Sources

- [Home Assistant Integration: Unifi (Feature comparison)](https://www.home-assistant.io/integrations/unifi/)
- [Meraki API Capabilities](https://developer.cisco.com/meraki/api-v1/)
