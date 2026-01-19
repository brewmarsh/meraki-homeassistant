import asyncio
import http.server
import os
import socketserver
import subprocess
import sys
import threading

from playwright.async_api import async_playwright

PORT = 8080


async def main():
    """Verify the UI with mock data."""
    # Change to the www directory to serve files
    os.chdir("custom_components/meraki_ha/www")

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print(f"Serving at port {PORT}")

        # 1. Build the panel (App.tsx contains mock data logic for localhost)
        print("Building frontend...")
        build_result = subprocess.run(
            "npm run build", shell=True, check=False
        )  # nosec
        if build_result.returncode != 0:
            print("Build failed. Aborting verification.", file=sys.stderr)
            sys.exit(1)
        print("Build successful.")

        # 2. Create a temporary index.html to host the panel
        with open("test_index.html", "w") as f:
            f.write(
                """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <title>Meraki Panel Test</title>
                    <link rel="stylesheet" href="style.css">
                </head>
                <body>
                    <meraki-panel></meraki-panel>
                    <script type="module" src="meraki-panel.js"></script>
                    <script>
                        // Mock the panel config if needed
                        const panel = document.querySelector('meraki-panel');
                        panel.panel = { config: { config_entry_id: 'mock' } };
                    </script>
                </body>
                </html>
            """
            )

        # 3. Use Playwright to take a screenshot
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))

            print(f"Navigating to http://localhost:{PORT}/test_index.html")
            await page.goto(
                f"http://localhost:{PORT}/test_index.html", wait_until="networkidle"
            )

            print("Waiting for selector...")
            # Expecting "Meraki HA Web UI" as per App.tsx
            await page.wait_for_selector('text="Meraki HA Web UI"')
            print("Selector found!")

            screenshot_path = "../../verification_screenshot.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            await browser.close()

    finally:
        httpd.shutdown()
        server_thread.join()

        # Cleanup test_index.html
        if os.path.exists("test_index.html"):
            os.remove("test_index.html")

        # Change back to the root directory
        os.chdir("../../..")


if __name__ == "__main__":
    asyncio.run(main())
