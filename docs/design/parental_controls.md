# Updated Design and Implementation Plan: Parental Controls & Content Filtering

## 1. Product Vision & Scope

The goal is to empower users with an intuitive and responsive interface to manage parental controls on their home network via Home Assistant, leveraging the power of their Meraki MX Security Appliance. This plan prioritizes **simplicity and safety** to ensure the integration is reliable and does not negatively impact existing network configurations.

This plan will focus on two core features:

- **Network-wide content filtering via policy selection.**
- **On-demand device-level internet blocking ("time-out").**

---

### **2. Core Features & User Stories**

- **Content Filtering Policy Selection:** \* **User Story:** As a parent, I want to quickly switch my network’s content filtering policy from "school" to "gaming" to "bedtime" directly from Home Assistant, so I can easily manage my family's internet access throughout the day.
  - **Implementation:** A `select` entity will be exposed for each Meraki network, allowing the user to choose from a list of predefined content filtering policies from the Meraki dashboard.

- **On-Demand Device Internet "Time-Out":**
  - **User Story:** As a parent, I want to instantly disable internet access for my child's device, so I can enforce a "time-out" when they're not listening.
  - **Implementation:** A `switch` entity will be created for each detected client device. Toggling this switch will create or remove a device-specific Layer 7 (L7) firewall rule, blocking all internet traffic for that client.

---

### **3. Technical Design**

#### **3.1. Home Assistant Entities**

- **Entity 1: Content Filtering `select` Entity**
  - **Entity ID:** `select.meraki_content_filtering_policy_<network_name_slug>`
  - **Function:** This entity will pull the list of available content filtering policies from the Meraki dashboard. The agent must handle the retrieval of these policy names, including the default categories (`Block all`, `Adult themes`, etc.) and any custom policies.
  - **API Calls:** \* `GET /networks/{networkId}/appliance/contentFiltering` (for initial state)
    - `PUT /networks/{networkId}/appliance/contentFiltering` (for state change)

- **Entity 2: Client `switch` Entity**
  - **Entity ID:** `switch.meraki_client_internet_access_<client_mac_address_slug>`
  - **Function:** This entity's state will reflect the internet access status for a specific device. Toggling the switch will create or delete a specific L7 firewall rule for that device.
  - **API Calls:**
    - `GET /networks/{networkId}/clients` (to get a list of clients and their MAC/IP)
    - `GET /networks/{networkId}/appliance/firewall/l7FirewallRules` (to check for existing rules)
    - `PUT /networks/{networkId}/appliance/firewall/l7FirewallRules` (to add/remove rules)

#### **3.2. Meraki API Interaction**

- **Content Filtering:** The API endpoints are correctly identified. The agent should be aware that the `PUT` request to update content filtering requires the entire object, including the `allowedUrlPatterns` and `blockedUrlPatterns`. It should **read the current state first, update only the policy, and then write the complete object back**.
- **Client Firewall Rules:** This is the most critical part of the implementation. The agent must:

1. Use a unique comment to identify its rules. **Suggestion:** `{"comment": "Managed by Home Assistant Meraki Parental Controls"}`. This is essential to prevent conflicts with manually created rules.
2. When a switch is toggled **on** (to block), the agent will add a new L7 firewall rule with the specific client's IP address.
   - **Rule Type:** Deny
   - **Protocol:** Any
   - **Port:** Any
   - **URL Pattern:** `*`
   - **Client IP:** The IP of the device. The agent will need to get the IP address from the `/networks/{networkId}/clients` endpoint.
3. When a switch is toggled **off** (to allow), the agent will find the rule with the unique comment and the matching client IP and remove it from the list of rules before sending the `PUT` request.
4. **Important:** The Meraki API has an endpoint to get a client's IP address (`GET /networks/{networkId}/clients/{clientId}/status`). The agent should use this to get the IP, as the `/networks/{networkId}/clients` endpoint might not always have the most up-to-date IP address.

#### **3.3. State Management & Polling**

- The integration must poll the Meraki API at a reasonable interval (e.g., every 3-5 minutes) to update the state of the Home Assistant entities.
- The `select` entity's state should reflect the current Meraki network policy.
- The `switch` entities' states should reflect the presence or absence of the corresponding L7 firewall rules. This ensures the Home Assistant UI stays in sync with the Meraki configuration, even if changes are made outside of Home Assistant.

---

### **4. Risks & Mitigations**

- **Risk:** Overwriting user-defined firewall rules.
  - **Mitigation:** The plan to use a unique comment is the correct approach. The agent **must only modify rules that contain this specific comment**. All other rules must be preserved.

- **Risk:** Meraki API rate limiting.
  - **Mitigation:** The agent should implement a delay or a queue for multiple API calls (e.g., when a user rapidly toggles several switches). Polling intervals should be carefully considered to avoid hitting the API too frequently.

- **Risk:** The Meraki device loses connection or the API key is invalid.
  - **Mitigation:** The integration should use robust error handling. If an API call fails, the entity state should be set to `unavailable`, and an error message should be logged in Home Assistant.

---

### **5. Additional & Optional Features**

Based on the capabilities of Meraki devices, here are a few more advanced features that would significantly enhance the user experience and create a more robust parental controls solution.

- **Scheduled Access (Time-based Rules):**
  - **Concept:** Instead of just an on/off switch, allow users to set schedules for internet access. This could be exposed as a **Home Assistant schedule helper entity**.
  - **How it works:** The integration would manage L7 firewall rules that are only active during specific times (e.g., blocking social media from 9 PM to 7 AM). The Meraki API supports time-of-day-based rules.
  - **Value:** Automates a common use case for parental controls, reducing the need for manual intervention.

- **Application & URL Blocking:**
  - **Concept:** Provide a user interface to block specific applications (e.g., "YouTube," "Fortnite") or custom URLs for a device.
  - **How it works:** Meraki's L7 firewall rules support blocking by application, application category, and URL. The integration could expose a new entity or a service call in Home Assistant for this.
  - **Value:** Offers more granular control than simple on/off. Parents could block specific games or websites without disabling all internet access.

- **Client Information & Monitoring:**
  - **Concept:** Expose more information about client devices as sensors in Home Assistant.
  - **How it works:** Create sensors for **data usage (downlink/uplink)**, **current IP address**, and **connected wireless network name/SSID**.
  - **Value:** Provides a single-pane-of-glass view for monitoring network activity, which is a key part of parental controls. This leverages Meraki's powerful network visibility features.
