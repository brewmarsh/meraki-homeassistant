import time
from playwright.sync_api import sync_playwright, expect
import http.server
import socketserver
import threading
import os

# Set up a simple HTTP server to serve the verification.html
PORT = 8080
DIRECTORY = "custom_components/meraki_ha/www"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_server():
    # Allow reusing address
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def verify_frontend():
    # Start the server in a separate thread
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()

    # Give the server a moment to start
    time.sleep(2)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Capture console logs
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))

        try:
            # Go to the verification page
            page.goto(f"http://localhost:{PORT}/verification.html")

            # Wait for the network card to appear
            # The mock data has network name "Main Office"
            # The header text format is "[Network] Main Office"
            network_header = page.locator("text=[Network] Main Office")
            network_header.wait_for(timeout=5000)

            # Click to expand
            print("Clicking network header to expand...")
            network_header.click()

            # Wait for the device table to load
            # The mock data in App.tsx has 'Living Room AP'
            page.wait_for_selector("text=Living Room AP", timeout=5000)
            print("Device table loaded.")

            # Verify MR icon (mdi:wifi) for MR33
            mr_icon = page.locator("tr:has-text('MR33') ha-icon")
            expect(mr_icon).to_have_attribute("icon", "mdi:wifi")
            print("Verified MR icon is mdi:wifi")

            # Verify MS icon (mdi:lan) for MS220-8P
            ms_icon = page.locator("tr:has-text('MS220-8P') ha-icon")
            expect(ms_icon).to_have_attribute("icon", "mdi:lan")
            print("Verified MS icon is mdi:lan")

            # Verify MV icon (mdi:cctv) for MV12
            mv_icon = page.locator("tr:has-text('MV12') ha-icon")
            expect(mv_icon).to_have_attribute("icon", "mdi:cctv")
            print("Verified MV icon is mdi:cctv")

            # Verify Details button exists
            details_btn = page.locator("tr:has-text('MR33') button[title='View Details']")
            expect(details_btn).to_be_visible()
            print("Verified Details button exists")

            os.makedirs("verification", exist_ok=True)
            screenshot_path = os.path.abspath("verification/verification.png")
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/error.png")
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    verify_frontend()
