# Meraki HA Beta Release Notes (v2.2.1-beta.1)

This release focuses on camera improvements, API error handling, and performance optimizations.

## 🚀 New Features

### Camera Enhancements
*   **Stream Source Selection:** New option to choose between RTSP (local network) or Cloud (Meraki Dashboard) for camera streaming. Cloud streaming works for all camera models, including those that don't support RTSP (e.g., MV2).
*   **Snapshot Refresh Interval:** Configurable auto-refresh for camera snapshots on the dashboard. Set interval in seconds (0 = on-demand only). Cached snapshots reduce API calls and load instantly.

### API & Performance
*   **Network Filtering:** Integration now only polls networks enabled in settings, reducing unnecessary API calls and improving performance for large deployments.
*   **Web API Stream Source:** WebSocket endpoint for camera stream URL now accepts optional `stream_source` parameter ("rtsp" or "cloud").

### Frontend Panel
*   **HA Custom Panel Architecture:** Refactored to use proper Home Assistant panel integration with `hass.callWS()` for authenticated API calls.
*   **Redesigned UI:** New card-based layout with CSS variables for light/dark theme support, device status badges, and model-specific icons.
*   **Network Filtering:** Panel only displays enabled networks with auto-expand for single network setups.

## 🐛 Bug Fixes

*   **"Invalid device type" Error:** Fixed API error occurring 1,900+ times by filtering networks to only query client-capable types (wireless, appliance, switch, cellularGateway). Camera-only networks no longer cause 400 Bad Request errors.
*   **Camera Snapshot Failures:** Added retry mechanism (3 attempts with 2-second delays) for snapshot generation. Gracefully handles 202/400 responses and falls back to cached snapshots.
*   **Traffic Analysis Logging:** Informational errors (traffic analysis disabled, VLANs disabled) no longer logged at ERROR level, reducing log noise.
*   **Frontend Click Handling:** Fixed click handling for device rows and entity links.
*   **WebSocket Registration:** Fixed `async_setup_websocket_api` registration for subscription handler.

## 🔧 Under the Hood

*   **Code Quality:** Continued cleanup of linting errors and formatting updates using `ruff`.
*   **Error Handling:** Improved error propagation for informational API errors.
*   **Snapshot Caching:** Implemented in-memory caching with configurable TTL.

---

**Configuration Options (Settings → Devices & Services → Meraki HA → Configure):**
*   **Camera Stream Source:** "RTSP (Local Network)" or "Cloud (Meraki Dashboard)"
*   **Camera Snapshot Refresh Interval:** 0-3600 seconds (0 = on-demand only)

**Testing Instructions:**
1. Test camera streaming with both RTSP and Cloud options
2. Set snapshot interval to 30-60 seconds and verify auto-refresh on dashboard
3. Confirm API errors in logs have significantly decreased
4. Verify only enabled networks are polled (check debug logs)
