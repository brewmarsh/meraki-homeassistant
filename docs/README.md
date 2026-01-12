# Meraki Home Assistant Integration Documentation

Welcome to the central documentation for the Meraki Home Assistant Integration. This collection of documents provides information on the requirements, design, and architecture of the integration.

## Documentation Sections

Please explore the different sections to find the information you need:

- **[Requirements](./requirements/README.md)**
  Functional and technical requirements for the integration across device types.

- **[Design](./design/README.md)**
  High-level design documents (event log viewer, guest Wi‑Fi, more).

- **[Architecture & Development](./architecture/README.md)**
  Architecture overviews, refactoring plans, and developer setup guides.

- **[Testing](./testing/testing_plan.md)**
  Testing strategy and plans to ensure quality and reliability.

## Webhooks & Real-Time Updates

The integration supports comprehensive webhook alerts for real-time monitoring. Key features:

- **Real-Time Alerts:** Instant notifications for device status, client connectivity, configuration changes, and security events
- **API Efficiency:** 85% reduction in API calls when webhooks are active
- **Targeted Refresh:** Smart updates for only affected entities
- **Adaptive Polling:** Automatic interval reduction when webhooks are healthy
- **Monitoring:** Health sensors and Prometheus-style metrics for observability

For complete webhook documentation, see **[Architecture > Webhooks](./architecture/webhooks.md)**.

### Quick Setup

1. **Enable Webhooks:** Settings > Devices & Services > Meraki > Configure > Webhooks
2. **Auto-Register:** Enable `webhook_auto_register` to automatically configure Meraki Dashboard
3. **Select Alerts:** Choose which alert types to subscribe (device, client, network, security, sensor)
4. **Configure External URL:** Set your public HTTPS URL (or use HA's external URL)

**Note:** Webhooks require HTTPS and a public URL. Read-only API keys require manual setup in Meraki Dashboard.
