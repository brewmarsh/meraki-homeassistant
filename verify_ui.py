import asyncio
import http.server
import os
import socketserver
import sys
import threading

from playwright.async_api import async_playwright

PORT = 8080


async def main():
    """Verify the UI with mock data."""
    original_main_tsx = ""

    # Change to the www directory to serve files
    os.chdir("custom_components/meraki_ha/www")

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print(f"Serving at port {PORT}")

        # 1. Temporarily modify main.tsx to render App with mock data
        with open(os.path.join("src", "main.tsx")) as f:
            original_main_tsx = f.read()

        mock_app_tsx = """
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const mockHass = {
  connection: {
    sendMessagePromise: async (message: any) => {
      console.log('Mock sendMessagePromise called with:', message);
      return Promise.resolve({
        networks: [
            { id: 'net-1', name: 'Marshmallow Home' },
            { id: 'net-2', name: 'Shenanibarn' }
        ],
        devices: [
          {
            networkId: 'net-1',
            name: 'Living Room AP',
            model: 'MR33',
            serial: 'Q2JD-XXXX-YYYY',
            status: 'online',
            lanIp: '192.168.1.1'
          },
          {
            networkId: 'net-2',
            name: 'Barn Camera',
            model: 'MV12',
            serial: 'Q2LD-XXXX-ZZZZ',
            status: 'online',
            lanIp: '10.0.0.1'
          },
        ],
      });
    }
  },
  themes: {
    darkMode: true,
  },
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App hass={mockHass} config_entry_id="mock-entry-id" />
  </React.StrictMode>
);
"""
        with open(os.path.join("src", "main.tsx"), "w") as f:
            f.write(mock_app_tsx)

        # 2. Re-build the panel with the mock data
        print("Building frontend with mock data...")
        build_result = os.system("npm run build")
        if build_result != 0:
            print("Build failed. Aborting verification.", file=sys.stderr)
            sys.exit(1)
        print("Build successful.")

        # 3. Create a temporary index.html to host the panel
        with open("index.html", "w") as f:
            f.write("""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <title>Meraki Panel Test</title>
                    <link rel="stylesheet" href="style.css">
                </head>
                <body>
                    <div id="root"></div>
                    <script type="module" src="meraki-panel.js"></script>
                </body>
                </html>
            """)

        # 4. Use Playwright to take a screenshot
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))

            print(f"Navigating to http://localhost:{PORT}")
            await page.goto(f"http://localhost:{PORT}", wait_until="networkidle")

            print("Waiting for selector...")
            await page.wait_for_selector('text="Meraki Integration Control"')
            print("Selector found!")

            screenshot_path = "../../verification_screenshot.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            await browser.close()

    finally:
        httpd.shutdown()
        server_thread.join()
        # Restore original main.tsx and rebuild
        if original_main_tsx:
            print("Restoring original main.tsx...")
            with open(os.path.join("src", "main.tsx"), "w") as f:
                f.write(original_main_tsx)
            print("Rebuilding frontend...")
            os.system("npm run build")
            print("Frontend restored.")

        # Change back to the root directory
        os.chdir("../../..")


if __name__ == "__main__":
    asyncio.run(main())
