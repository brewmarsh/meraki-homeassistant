# Integration and Web UI Testing Plan

This document outlines the validation steps for the `meraki_ha` integration, covering both the initial Home Assistant setup flow and the self-hosted web interface.

## P0: Critical Path Tests (Setup & Core UI)

### **Test Case: SETUP-P0-01 - Initial Configuration Flow**

* **Priority:** P0
* **Description:** Validates that a user can successfully link their Meraki account via API Key and Org ID.
* **Steps:**
1. Initiate the "Add Integration" flow for Meraki in Home Assistant.
2. Enter a valid API Key and a numeric Organization ID.
3. Click "Submit."


* **Expected Result:**
* The `DATA_SCHEMA` validates the inputs without "extra keys" or "unable to convert" errors.
* The integration successfully calls the Meraki API to verify credentials.
* A new Config Entry is created, and the sidebar "Meraki" icon appears.



### **Test Case: SETUP-P0-02 - Error Handling & Localized Strings**

* **Priority:** P0
* **Description:** Ensures the UI correctly communicates setup failures to the user.
* **Steps:**
1. Attempt setup with an invalid/expired API key.
2. Attempt setup with an Organization ID that is already configured.


* **Expected Result:**
* **Invalid Key:** UI displays the "Invalid Authentication" error (mapped from `strings.json`).
* **Duplicate:** UI displays the "Already Configured" error and prevents a second entry.



### **Test Case: UI-P0-01 - View Dashboard with Data**

* **Priority:** P0
* **Description:** Ensures the web UI displays populated network and client data.
* **Preconditions:** Integration is configured; Web UI enabled on port 9988.
* **Steps:**
1. Navigate to `http://<home-assistant-ip>:9988`.
2. Observe the "Networks" and "Clients" cards.


* **Expected Result:**
* Page loads without console errors.
* Data matches the backend coordinator's current state.



---

## P1: High Priority Tests (Navigation & Configuration)

### **Test Case: UI-P1-01 - Navigate to Detail Views**

* **Priority:** P1
* **Description:** Ensures deep-linking to specific networks or clients works correctly.
* **Steps:**
1. Click a network card; verify URL changes to `/networks/<id>`.
2. Click a client card; verify URL changes to `/clients/<mac>`.


* **Expected Result:** Detail pages load with specific data relevant only to that entity.

### **Test Case: UI-P1-02 - UI Toggle and Port Re-mapping**

* **Priority:** P1
* **Description:** Validates that Home Assistant Options correctly control the web server.
* **Steps:**
1. Disable "Enable Web UI" in options; verify 9988 is unreachable.
2. Change port to 9989; verify the UI migrates to the new port.



---

## P2: Maintenance & Edge Cases

### **Test Case: UI-P2-01 - Dashboard with Empty Data**

* **Priority:** P2
* **Description:** Ensures the UI doesn't crash if the Meraki API returns 0 items.
* **Expected Result:** The cards display "0" and an empty state message rather than a loading spinner or error.

### **Test Case: SETUP-P2-01 - Static Asset Loading (2026.1)**

* **Priority:** P2
* **Description:** Verifies that the `.js` panel is served correctly under the new async requirements.
* **Expected Result:** Navigating to `/local/meraki_ha/meraki-panel.js` returns the file with the `application/javascript` MIME type.
