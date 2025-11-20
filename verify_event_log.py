import http.server
import os
import socketserver
import threading
import time

from playwright.sync_api import expect, sync_playwright

# Set up a simple HTTP server to serve the verification.html
PORT = 8080
DIRECTORY = "custom_components/meraki_ha/www"

class Handler(http.server.SimpleHTTPRequestHandler):
    """A simple HTTP request handler that serves files from a specific directory."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_server():
    """Start the HTTP server on the specified port."""
    # Allow reusing address
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def verify_event_log():
    """Run Playwright to verify the Event Log functionality."""
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
            network_header = page.locator("text=[Network] Main Office")
            network_header.wait_for(timeout=5000)

            # Click to expand the network card
            print("Clicking network header to expand...")
            network_header.click()

            # Wait for the Event Log section to appear
            # We look for "Recent Events" header which is in EventLog.tsx
            page.wait_for_selector("text=Recent Events", timeout=5000)
            print("Event Log section found.")

            # Verify mock events are displayed
            # "Client connected"
            expect(page.locator("text=Client connected")).to_be_visible()
            # "Device came online"
            expect(page.locator("text=Device came online")).to_be_visible()

            print("Mock events verified.")

            os.makedirs("verification", exist_ok=True)
            screenshot_path = os.path.abspath("verification/event_log_verification.png")
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/error.png")
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    verify_event_log()
