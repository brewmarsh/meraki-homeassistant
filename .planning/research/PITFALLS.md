# Domain Pitfalls

**Domain:** Network Device Hubs
**Researched:** February 2025

## Critical Pitfalls

Mistakes that cause rewrites or major stability issues.

### Pitfall 1: Event Loop Blocking via SDK

**What goes wrong:** Meraki's Python SDK is synchronous (blocking).
**Why it happens:** Using standard `import meraki` and calling `api.clients.getNetworkClients()` directly in an `async` function.
**Consequences:** Home Assistant's UI freezes; other integrations time out.
**Prevention:** Use `hass.async_add_executor_job` for all SDK calls or use an `aiohttp` based custom wrapper.

### Pitfall 2: Entity Bloat (MAC Randomization)

**What goes wrong:** Modern smartphones use random MAC addresses.
**Why it happens:** Every time a new "device" connects to a guest network, HA creates a new entity.
**Consequences:** Thousands of useless entities in the registry and database.
**Prevention:** Disable "Track new devices" by default. Implement a "Known Clients" filter.

### Pitfall 3: API Rate Limiting (429 Errors)

**What goes wrong:** The integration starts failing after some time.
**Why it happens:** Multiple organizations/networks being polled too frequently or without batching.
**Consequences:** Entities go unavailable; data gaps.
**Prevention:** Centralized `MerakiHub` with rate-limiting aware semaphore; 5 requests/sec limit for Meraki.

## Moderate Pitfalls

### Pitfall 1: Stale Presence Data

**What goes wrong:** A client leaves the network but remains "home" in HA.
**Why it happens:** Polling interval too long (e.g. 5 mins).
**Prevention:** Use Webhooks for "leaves" or implement a "disappearance" timeout in the coordinator.

## Minor Pitfalls

### Pitfall 1: Inconsistent Device Names

**What goes wrong:** Meraki Dashboard has names, but HA shows "mac_1234".
**Prevention:** Sync device metadata during discovery and refresh periodically.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall         | Mitigation                                                         |
| ----------- | ---------------------- | ------------------------------------------------------------------ |
| Discovery   | Timeout for large orgs | Implement chunked discovery or multi-step config flow.             |
| Presence    | High event churn       | Use `async_write_ha_state` only on value change; debounce updates. |
| Webhooks    | Port forwarding issues | Provide clear documentation and health checks for webhook receipt. |

## Sources

- [Meraki API Best Practices](https://developer.cisco.com/meraki/api-v1/best-practices/)
- [Home Assistant Integration: Device Tracker Docs](https://developers.home-assistant.io/docs/core/entity/device-tracker/)
