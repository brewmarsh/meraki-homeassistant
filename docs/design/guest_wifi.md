# Design Proposal: Guest Wi-Fi Management (with Splash Page)

This document outlines the design for the "Guest Wi-Fi Management" feature for the Meraki Home Assistant integration's web UI.

## 1. Feature Goal

To provide a simple and convenient way for users to manage their guest Wi-Fi network directly from the Home Assistant web UI, without needing to log in to the Meraki dashboard. The primary focus will be on enabling/disabling the guest network, managing its password, and optionally configuring a custom, self-hosted splash page with email collection.

## 2. UI Design (on a new "Guest Wi-Fi" page)

The page will be divided into two main sections:

<<<<<<< HEAD
\*\*Section 1: Basic Guest Network Control
=======
### Section 1: Basic Guest Network Control
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

- **Enable Guest Wi-Fi:** A toggle switch to enable/disable the guest SSID.
- **Guest Wi-Fi Password:** A text input to view and change the password, with a save button.

<<<<<<< HEAD
\*\*Section 2: Custom Splash Page Configuration
=======
### Section 2: Custom Splash Page Configuration
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

- **Enable Custom Splash Page:** A main toggle switch for this feature.
- When enabled, the following options appear:
  - **Splash Page Content:** A text area where you can enter a welcome message or terms of service for your splash page.
  - **Collect Email Addresses:** A checkbox to enable a simple email sign-up form on the splash page.
  - **Splash Page URL:** A read-only field showing the public URL where your splash page will be hosted (e.g., `http://<your_ha_public_url>/api/meraki_ha/splash/{network_id}`).

**Important Security Note:** A clear warning message will be displayed here:

> "Enabling this feature will automatically create a firewall rule (a 'walled garden' exception) to allow unauthenticated guest devices to access this Home Assistant URL. Please ensure your Home Assistant instance is securely configured."

---

## 3. Implementation Plan & Instructions for a Continuing Agent

<<<<<<< HEAD
\*\*Goal

Implement the "Guest Wi-Fi Management" feature as described above.

\*\*Prerequisites
=======
### Goal

Implement the "Guest Wi-Fi Management" feature as described above.

### Prerequisites
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

- Familiarity with creating Home Assistant `switch` and `text` entities.
- Knowledge of the Meraki API for managing SSIDs.
- Familiarity with React (functional components, hooks like `useState` and `useEffect`).
- Understanding of how to make API calls in JavaScript using `fetch`.

<<<<<<< HEAD
\*\*Step-by-Step Implementation Plan

#\*\*1. Backend: Core Entities & API
=======
### Step-by-Step Implementation Plan

#### 1. Backend: Core Entities & API
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

- **Entities:**
  - Implement the `MerakiGuestWifiPasswordText` entity as previously described.
- **Web Server (`web_server.py`):**
  - **Public Splash Page Endpoint:** Create a new, unauthenticated route like `/api/meraki_ha/splash/{network_id}`. This route will serve a modern-looking HTML page. The content of this page will be dynamically generated based on the user's settings (the custom content and whether the email form is enabled).
  - **Email Collection Endpoint:** Create a new endpoint like `/api/meraki_ha/splash_signup` to handle the form submission from the splash page. This endpoint will save the collected email addresses (e.g., to a `.csv` file in your `config` directory).
  - **Configuration Endpoints:** Create new API endpoints (`/api/guest_wifi/splash_settings`) for the frontend to get and set the splash page configuration (enabled, content, email collection setting).

<<<<<<< HEAD
#\*\*2. Backend: Meraki API Interaction
=======
#### 2. Backend: Meraki API Interaction
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

- When the user enables the custom splash page, the integration will need to make a series of API calls:

1. **Update SSID Settings:** Call `PUT /networks/{networkId}/wireless/ssids/{number}` to set:
   - `splashPage` to `"Click-through splash page"`.
   - `splashUrl` to the public URL of the new splash page endpoint.
2. **Update Firewall Rules:** Call `PUT /networks/{networkId}/wireless/ssids/{number}` to update the `walledGardenRanges`. The public URL of your Home Assistant instance must be added to this list to allow guest devices to access the splash page.

<<<<<<< HEAD
#\*\*3. Frontend: UI Implementation
=======
#### 3. Frontend: UI Implementation
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

- Create the new **"Guest Wi-Fi"** page (`GuestWifiPage.jsx`) as designed above.
- The page will fetch its state from the new backend endpoints.
- The "Save" buttons will post the configuration back to the backend.

<<<<<<< HEAD
#\*\*4. Build and Verify
=======
#### 4. Build and Verify
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)

- As before, this will involve building the frontend and using a Playwright script to test the new UI and its functionality.
