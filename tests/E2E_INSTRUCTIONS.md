# End-to-End (E2E) Test Implementation Instructions

This document outlines the plan for expanding the E2E test suite for the Meraki Home Assistant integration. The goal is to verify the functionality of the custom frontend panel (`meraki-panel`) using Playwright.

## Current State

- **Existing Test:** `tests/test_e2e_web_ui.py` checks if the frontend loads, displays the network list, and verifies basic navigation.
- **Status:** The comprehensive E2E test scenarios defined below have been implemented in `tests/test_e2e_web_ui.py`.

## Implementation Plan

The following scenarios are implemented in `tests/test_e2e_web_ui.py`.

### Test Scenarios

#### 1. Navigation & Data Loading

- **Scenario:** Verify that the dashboard loads the list of Networks from the mock data.
- **Action:** Wait for `.network-card` elements to appear.
- **Assertion:** Check that the number of network cards matches the mock data.
- **Status:** Completed.

#### 2. Device Expansion

- **Scenario:** User clicks on a Network card to view devices.
- **Action:** Click on a `.network-card` (or the specific expand button).
- **Assertion:** Verify that the devices (e.g., "Office Switch", "Front Door Camera") become visible.
- **Status:** Completed.

#### 3. Switch Port Control

- **Scenario:** View switch details.
- **Action:**
  - Expand a Switch device.
  - Navigate to details.
- **Verification:**
  - **Note:** The current UI (`DeviceView.tsx`) provides a read-only list of entities and does not support interactive port toggling. The test verifies navigation and visibility of the switch device.
- **Status:** Completed (Adapted to read-only UI).

#### 4. SSID Toggle

- **Scenario:** Verify SSID status.
- **Action:** Locate the SSID card.
- **Verification:**
  - **Note:** The current UI (`SSIDView.tsx`) displays SSID status but does not have an interactive toggle. The test verifies that the SSID is displayed with the correct "Enabled" status.
- **Status:** Completed (Adapted to read-only UI).

#### 5. Camera Visibility

- **Scenario:** Verify camera status indicator.
- **Action:** Check the status text in the device table.
- **Verification:** Verify status is "online".
- **Status:** Completed.

### Technical Notes

- **Mocking:** `hass.callWS` is mocked to handle `meraki_ha/get_config` and `meraki_ha/update_options`.
- **Selectors:** Selectors have been updated to target the specific DOM structure of `ha-card` and standard HTML elements used in the new UI.
