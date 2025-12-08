
import os
import subprocess
import time
from playwright.sync_api import sync_playwright, expect

def test_sensor_status(page):
    # Navigate to localhost where the index.html is served
    page.goto("http://localhost:8000/index.html")

    # Wait for the panel to load
    # Specifically wait for the Sensors group or a device row
    # The 'meraki-panel' element contains the app
    # Inside, we expect to see devices

    # Wait for the table to appear (Sensors section)
    # We can look for text "MT10 Temp"
    expect(page.get_by_text("MT10 Temp")).to_be_visible(timeout=10000)

    # Now verify the status column values

    # MT10 Temp: Should show "20.5 °C"
    # Find row with MT10 Temp, check status column
    # Using simple text search for now
    expect(page.get_by_text("20.5 °C")).to_be_visible()

    # MT12 Water: Should show "Wet"
    expect(page.get_by_text("Wet")).to_be_visible()

    # MT14 TVOC: Should show "150 μg/m³"
    expect(page.get_by_text("150 μg/m³")).to_be_visible()

    # MT15 TVOC: Should show "300 μg/m³"
    expect(page.get_by_text("300 μg/m³")).to_be_visible()

    # MT20 Door: Should show "Closed" (open=false)
    expect(page.get_by_text("Closed")).to_be_visible()

    # MT40 Power: Should show "On" (switch is 'on')
    expect(page.get_by_text("On", exact=True)).to_be_visible()

    # MT10 Offline: Should show "Offline" (capitalized)
    expect(page.get_by_text("Offline")).to_be_visible()

    # MT10 Dormant: Should show "Dormant"
    expect(page.get_by_text("Dormant")).to_be_visible()

    # Expand the "Test Network" if needed, but the mock data structure
    # and NetworkView default expanded state logic might need checking.
    # In NetworkView, `openNetworkIds` is initialized from sessionStorage.
    # It might default to closed.
    # So we might need to click the network header.

    # Check if network header is visible
    # NetworkView renders: [Network] Test Network
    network_header = page.get_by_text("[Network] Test Network")
    if network_header.is_visible():
        # Check if expanded. The chevron icon indicates state.
        # But simpler: check if devices are visible.
        # If "MT10 Temp" is not visible, click header.
        if not page.get_by_text("MT10 Temp").is_visible():
            network_header.click()
            # Wait for expansion
            expect(page.get_by_text("MT10 Temp")).to_be_visible()

    # Take screenshot
    page.screenshot(path="verification/verification.png", full_page=True)

if __name__ == "__main__":
    # Start HTTP server in background
    # We need to serve from verification/ directory
    # But current working dir is repo root.
    # So we change dir in subprocess or just serve verification/

    # Using python -m http.server -d verification 8000
    server_process = subprocess.Popen(
        ["python3", "-m", "http.server", "8000", "--directory", "verification"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        # Give server a moment to start
        time.sleep(2)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            test_sensor_status(page)
            browser.close()

    finally:
        server_process.terminate()
