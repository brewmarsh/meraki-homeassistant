# Configuration

This page details the configuration options and setup instructions for the Meraki Home Assistant Integration.

## Obtaining Meraki API Credentials

To use this integration, you will need a Meraki API key and your Organization ID.

1.  **Log in to the Meraki Dashboard:** Go to [https://dashboard.meraki.com/](https://dashboard.meraki.com/).
2.  **Enable API Access:**
    *   Navigate to **Organization** > **Settings**.
    *   Under the **Dashboard API access** section, ensure API access is enabled.
3.  **Generate API Key:**
    *   Go to your **Profile** (click your name/email in the top right) > **My profile**.
    *   Scroll down to the **API access** section.
    *   Click **Generate new API key**.
    *   **Important:** Copy the generated API key and store it securely. You will not be able to see it again after navigating away from this page.
4.  **Find Organization ID:**
    *   The Organization ID is not directly visible in an obvious "Org ID" field.
    *   One way to find it is to look at the URL when you are viewing your organization dashboard. It might be part of the URL structure (e.g., `nXX...`).
    *   Alternatively, you can often find it by making a simple API call (e.g., using `curl` or Postman) to the `/organizations` endpoint with your API key. The response will list your accessible organizations and their IDs.

    ```bash
    curl -L -H 'X-Cisco-Meraki-API-Key: <your_api_key>' -H 'Content-Type: application/json' 'https://api.meraki.com/api/v1/organizations'
    ```

## Setting up the Integration

1.  Navigate to **Settings** > **Devices & Services** in your Home Assistant UI.
2.  Click the **+ ADD INTEGRATION** button in the bottom right.
3.  Search for "Meraki" and select it.
4.  Follow the on-screen prompts to enter your API Key and Organization ID.

## Configuration Options

The following options can be configured in the options flow for the integration:

*   **Scan Interval:** The interval in seconds at which the integration will poll the Meraki API for data updates. The default is 60 seconds.
*   **Webhook URL (Optional):** A custom URL for Meraki webhooks. If left blank, the integration will use the default Home Assistant webhook URL.
