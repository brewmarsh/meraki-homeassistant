# Success Criteria

This document defines the observable behaviors that confirm a phase is complete and successful.

## Phase 1: Foundation & Discovery

**Goal**: Users can connect their Meraki account and see their hardware hierarchy in Home Assistant.

1. **Successful Authentication**: User can complete the config flow using a valid API key without errors.
2. **Hierarchy Discovery**: Meraki Organizations, Networks, and Devices appear correctly as "Devices" within the Home Assistant device registry.
3. **Async Stability**: Home Assistant logs are free of "Event loop blocked" warnings during initial discovery and setup.

## Phase 2: Coordinated Tracking & Monitoring

**Goal**: Users have reliable, near real-time visibility into hardware status and client presence using efficient polling.

1. **Hardware Monitoring**: Access Point, Switch, and Security Appliance status (Online/Offline) updates correctly in Home Assistant within the configured polling interval.
2. **Client Tracking**: Connected wireless clients appear as `device_tracker` entities and correctly reflect their connection state.
3. **Rate Limit Resilience**: The integration operates without triggering Meraki API rate limits (429 errors), even in environments with multiple networks or many clients.

## Phase 3: Real-time Webhooks & Presence Optimization

**Goal**: Users experience sub-second presence updates without entity registry bloat from guest devices.

1. **Real-time Updates**: Client "join" and "leave" events are reflected in Home Assistant within 2 seconds via the Meraki Webhook integration.
2. **Entity Registry Cleanliness**: The entity registry does not become cluttered with transient MAC addresses from devices using MAC randomization (Guest isolation).
3. **Webhook Security**: The integration successfully validates the Meraki shared secret for all incoming webhook payloads, rejecting unauthenticated requests.

## Phase 4: Advanced Control & Selective Stats

**Goal**: Users can manage their network configuration and view detailed performance metrics from Home Assistant.

1. **Configuration Control**: Users can enable or disable SSIDs and switch content filtering profiles directly from the Home Assistant UI or via service calls.
2. **Parental Controls**: Users can block or unblock specific clients from the network using Home Assistant services.
3. **Performance Metrics**: High-value metrics like uplink latency, jitter, and optional bandwidth stats are available as sensors without causing significant database or API overhead.
