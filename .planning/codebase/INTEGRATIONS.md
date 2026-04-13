# External Integrations

**Analysis Date:** 2024-05-23

## APIs & External Services

**Networking:**

- Cisco Meraki Dashboard API (v1) - Primary source of data for devices, networks, and organizations.
  - SDK/Client: `meraki` Python SDK (wrapped by `MerakiApiClient` in `custom_components/meraki_ha/core/api/client.py`).
  - Auth: `CONF_MERAKI_API_KEY` (Stored in config entry data).

**Observability:**

- Braintrust - Used for logging, tracing, and AI-assisted observability.
  - SDK/Client: `braintrust`
  - Auth: `BRAINTRUST_API_KEY` (Loaded from environment via `python-dotenv`).

## Data Storage

**Databases:**

- Home Assistant State Machine - Stores real-time states of all Meraki devices as entities.
- Home Assistant Config Entries - Stores integration configuration and credentials.

**File Storage:**

- DiskCache - Local persistent storage for API response caching.
  - Location: `custom_components/meraki_ha/cache` (indicated by `diskcache` usage).

**Caching:**

- In-memory `MerakiApiCache` - Prevents the "thundering herd" problem with `asyncio.Lock`.
  - Implementation: `custom_components/meraki_ha/core/api/shared_cache.py`.

## Authentication & Identity

**Auth Provider:**

- Custom Config Flow - Implemented in `custom_components/meraki_ha/config_flow.py` for API key and Organization ID setup.

## Monitoring & Observability

**Error Tracking:**

- Braintrust Traces - Used in `MerakiClient.run_sync` for detailed API error tracking.
- Home Assistant Logger - Native logging with the domain `meraki_ha`.

**Logs:**

- Standard Python logging with tiered verbosity (e.g., debug logs for API calls).

## CI/CD & Deployment

**Hosting:**

- Self-hosted on Home Assistant.

**CI Pipeline:**

- GitHub Actions - Configured in `.github/workflows/` for testing and linting.

## Environment Configuration

**Required env vars:**

- `BRAINTRUST_API_KEY` - Optional, for observability.
- `HASS_URL`, `HASS_TOKEN` - For testing/automation scripts.

**Secrets location:**

- Home Assistant standard secrets storage (`secrets.yaml` or encrypted config entries).

## Webhooks & Callbacks

**Incoming:**

- Meraki Post-Registration Webhooks - Receives real-time alerts and configuration changes from Meraki Dashboard.
  - Endpoints: `http[s]://<HASS_URL>/api/webhook/<WEBHOOK_ID>`.
  - Registered in `custom_components/meraki_ha/webhook.py`.

**Outgoing:**

- Webhook Registration - Automatically registers Home Assistant as a webhook destination on the Meraki Dashboard.
  - API: `createNetworkWebhooksHttpServer`.

---

_Integration audit: 2024-05-23_
