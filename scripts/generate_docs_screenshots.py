"""
Automated Documentation Screenshot Generator for Meraki HA.

Uses Playwright to pierce Shadow DOM and capture specific Lovelace card states.
"""

import os
import sys
import time

from playwright.sync_api import sync_playwright


def generate_screenshots():
    # 1. Environment Configuration
    url = os.environ.get("HA_URL")
    username = os.environ.get("HA_USERNAME")
    password = os.environ.get("HA_PASSWORD")

    if not all([url, username, password]):
        print("Error: HA_URL, HA_USERNAME, and HA_PASSWORD must be set in environment.")
        sys.exit(1)

    output_dir = "docs/images"
    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        # Launch browser (headless for CI/CD, change to False for debugging)
        browser = p.chromium.launch(headless=True)
        # Set a standard desktop viewport
        context = browser.new_context(viewport={"width": 1280, "height": 1080})
        page = context.new_page()

        print(f"Connecting to {url}...")
        page.goto(url)

        # 2. Authentication
        print("Logging in...")
        page.get_by_label("Username").fill(username)
        page.get_by_label("Password").fill(password)
        page.get_by_role("button", name="Log in").click()

        # Wait for the main UI to render
        page.wait_for_selector("home-assistant-main", timeout=30000)
        print("Login successful.")

        # 3. Navigation to Meraki View
        # Standard HA sidebar links are accessible via role 'link'
        print("Navigating to Meraki dashboard...")
        page.get_by_role("link", name="meraki", exact=False).click()

        # Initial wait for the dashboard frame
        page.wait_for_load_state("networkidle")

        # 4. Static Card Screenshots
        # We use locators that pierce Shadow DOM automatically
        static_cards = {
            "Network Status": "card_network_status.png",
            "Wi-Fi Access": "card_wifi_access.png",
            "Meraki Content Filter": "card_content_filter.png",
        }

        for header, filename in static_cards.items():
            print(f"Capturing static card: {header}...")
            card = page.locator("ha-card", has_text=header).first
            # Ensure it's rendered and scrolled into view
            card.scroll_into_view_if_needed()
            card.screenshot(path=os.path.join(output_dir, filename))

        # 5. Interactive Card (Guest Access) with Delayed Render Handling
        print("Waiting for 'Cisco Meraki Guest Access' card (max 45s)...")
        guest_card = page.locator("ha-card", has_text="Cisco Meraki Guest Access").first

        # CRITICAL: Wait for background data fetching to complete and the card to appear
        try:
            guest_card.wait_for(state="visible", timeout=45000)
        except Exception as e:
            print(f"Error: Guest Access card did not appear within 45s. {e}")
            browser.close()
            sys.exit(1)

        print("Interacting with Guest Access card...")
        # Open SSID Dropdown (Home Assistant forms typically use ha-select)
        # Locating by internal text labels is robust in HA
        guest_card.locator("ha-select", has_text="SSID").click()

        # Select the specific guest network
        page.get_by_text("LeftyGuest", exact=True).click()

        # Take "Before" screenshot
        print("Saving guest_access_before.png")
        guest_card.screenshot(
            path=os.path.join(output_dir, "card_guest_access_before.png")
        )

        # Trigger generation
        print("Clicking Generate Access Key...")
        generate_btn = guest_card.get_by_role("button", name="Generate Access Key")
        generate_btn.click()

        # Wait for the success UI state (typically shows 'Guest access key created')
        # We look for the success message text inside the card
        page.get_by_text("created successfully", exact=False).wait_for(
            state="visible", timeout=20000
        )

        # Brief pause for animations/QR code rendering
        time.sleep(1)

        # Take "After" screenshot
        print("Saving guest_access_after.png")
        guest_card.screenshot(
            path=os.path.join(output_dir, "card_guest_access_after.png")
        )

        print(f"Workflow complete. Screenshots saved to {output_dir}")
        browser.close()


if __name__ == "__main__":
    generate_screenshots()
