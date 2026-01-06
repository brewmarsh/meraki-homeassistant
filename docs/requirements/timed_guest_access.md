# Feature Specification: Meraki Timed Guest Access via IPSK

**Objective:** Add functionality to Home Assistant to generate a temporary, self-expiring Wi-Fi password (Identity PSK) for a specific Meraki SSID. This allows users to grant timed access (e.g., "Kids Wi-Fi for 30 mins") without permanent configuration changes.

### 1\. Backend / API Implementation

The integration must interact with the **Meraki Dashboard API v1**.

**A. API Endpoints Required**

  * **Create Key:** `POST /networks/{networkId}/wireless/ssids/{number}/identityPsks`
  * **Delete Key:** `DELETE /networks/{networkId}/wireless/ssids/{number}/identityPsks/{identityPskId}`
  * **Fetch Policies (For UI):** `GET /networks/{networkId}/groupPolicies`

**B. New Service Definition**
Create a new service (e.g., `meraki_ha.create_timed_access`) with the following parameters:

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `ssid_number` | Integer | **Yes** | The SSID index (0-14) where the key will be created. |
| `duration` | Integer | **Yes** | Duration in minutes before the key is auto-deleted. |
| `name` | String | No | Name for the key (e.g., "Guest-iPad"). Default: "HA-Guest-[Timestamp]". |
| `passphrase` | String | No | If empty, auto-generate a secure 8-char alphanumeric string. |
| `group_policy_id` | String | No | **Selection only.** The ID of an *existing* Meraki Group Policy to apply (e.g., for content filtering). |

**C. Data Payload Example (Create)**

```json
{
    "name": "HA-Guest-User",
    "passphrase": "SecretPassword123",
    "groupPolicyId": "101" // Optional: ID from existing policy list
}
```

### 2\. Logic & State Management (Crucial)

**Persistence Requirement:**
Home Assistant automations/delays do not survive a system restart. The integration must manage the "timer" internally to ensure keys are deleted even if HA reboots during the active session.

1.  **Storage:** Store active guest keys in `core.restore_state` or a local JSON registry containing:
      * `identity_psk_id`
      * `network_id`
      * `ssid_number`
      * `expires_at` (UTC timestamp)
2.  **Startup Routine:** On `async_setup`:
      * Load the list of tracked keys.
      * **Check:** If `expires_at` \< `current_time` -\> **Delete Key Immediately**.
      * **Check:** If `expires_at` \> `current_time` -\> Start a background timer for the remaining duration.
3.  **Expiration Action:** When the timer ends, call the `DELETE` API endpoint. This forces Meraki to disconnect any client using that specific key.

### 3\. Frontend / UI Implementation

(Applies if building a custom Lovelace card or Config Panel)

**Inputs:**

1.  **SSID Selector:** Dropdown of available SSIDs. *Ideally filter for SSIDs where `authMode` is `ipsk-without-radius`.*
2.  **Policy Selector:** Dropdown populated by `GET /groupPolicies`. Options should include "None" (default) and any named policies found (e.g., "Kids", "Throttled").
3.  **Duration:** Presets (30m, 1h, 4h) or custom input.
4.  **Generate Button:** Triggers the service.

**Outputs (Active Keys List):**

1.  **Display:** Table showing `Name` | `Passphrase` | `Time Remaining`.
2.  **QR Code:** Display a standard Wi-Fi QR code for easy joining:
    `WIFI:T:WPA;S:MyNetworkSSID;P:GeneratedPassword;;`
3.  **Revoke Button:** "End Now" button that triggers the delete function immediately.

### 4\. Constraints & Error Handling

  * **WPA3 Incompatibility:** IPSK without RADIUS does not support WPA3. If the target SSID is WPA3, the API call may fail or the client will fail to connect. Log a warning if `encryptionMode` \!= `wpa2`.
  * **Key Limits:**
      * Firmware MR 30.1+: Limit 5,000 keys.
      * Older Firmware: Limit 50 keys.
      * **Logic:** Check key count before creation. If full, return error: "Max IPSK limit reached."
  * **No Policy Creation:** The integration should **not** create new Group Policies for these sessions. It should only reference existing IDs to prevent dashboard clutter.

### 5\. Helpful Resources

  * **Meraki Documentation:** [IPSK Authentication without RADIUS](https://documentation.meraki.com/Wireless/Design_and_Configure/Configuration_Guides/Encryption_and_Authentication/IPSK_Authentication_without_RADIUS)
  * **Visual Reference:** [Creating Identity PSKs in Meraki Dashboard (Video)](https://www.google.com/search?q=https://www.youtube.com/watch%3Fv%3DkKHjk9VjgBs) – *Useful to visualize the fields being mapped in the API.*
